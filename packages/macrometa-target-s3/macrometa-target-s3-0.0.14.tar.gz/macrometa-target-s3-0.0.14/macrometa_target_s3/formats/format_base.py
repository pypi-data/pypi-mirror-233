import collections
import json
import logging
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone

import inflection
from boto3 import Session
from smart_open import open

from macrometa_target_s3.constants import (
    export_errors,
    export_lag,
    fabric_label,
    region_label,
    tenant_label,
    workflow_label,
)

LOGGER = logging.getLogger("macrometa-target-s3")
DATE_GRAIN = {
    "year": 7,
    "month": 6,
    "day": 5,
    "hour": 4,
    "minute": 3,
    "second": 2,
    "microsecond": 1,
}
COMPRESSION = {}


def format_type_factory(object_type_class, *pargs, **kargs):
    """A factory for creating ObjectTypes."""
    return object_type_class(*pargs, **kargs)


class FormatBase(metaclass=ABCMeta):

    """This is the object type base class"""

    def __init__(self, config: dict, context: dict, extension: str) -> None:
        # TODO: perhaps we should do some scrubbing here?
        self.config = config

        self.format = config.get("format", None)
        assert self.format, "FormatBase.__init__: Expecting format in configuration."

        self.cloud_provider = config.get("cloud_provider", None)
        assert (
            self.cloud_provider
        ), "FormatBase.__init__: Expecting cloud provider in configuration"

        self.object_per_record: bool = self.config.get("object_per_record")
        self.context = context
        self.extension = extension
        self.compression = "gz"  # TODO: need a list of compatible compression types

        self.stream_name_path_override = config.get("stream_name_path_override", None)

        if self.cloud_provider.get("cloud_provider_type", None) == "aws":
            aws_config = self.cloud_provider.get("aws", None)
            assert aws_config, "FormatBase.__init__: Expecting aws in configuration"

            self.bucket = aws_config.get("aws_bucket", None)  # required
            self.session = Session(
                aws_access_key_id=aws_config.get("aws_access_key_id", None),
                aws_secret_access_key=aws_config.get("aws_secret_access_key", None),
                aws_session_token=aws_config.get("aws_session_token", None),
                region_name=aws_config.get("aws_region"),
                profile_name=aws_config.get("aws_profile_name", None),
            )
            self.client = self.session.client(
                "s3",
                endpoint_url=aws_config.get("aws_endpoint_override", None),
            )

        self.prefix = config.get("prefix", None)
        self.logger = context["logger"]
        self.fully_qualified_key = self.create_key()
        self.logger.info(f"batch file key: {self.fully_qualified_key}")

    @abstractmethod
    def _write(self, contents: str = None, key: str = None) -> None:
        """Execute the write to S3. (default)"""
        # TODO: create dynamic cloud
        # TODO: is there a better way to handle write contents ?
        self.logger.debug(f"Writing object: {key} to s3")
        path = (
            f"{key}.{self.extension}"
            if self.object_per_record
            else f"{self.fully_qualified_key}.{self.extension}.{self.compression}"
        )
        try:
            with open(
                f"s3://{path}",
                "w",
                transport_params={"client": self.client},
            ) as f:
                f.write(contents)
        except Exception as e:
            # Increment export_errors metric
            export_errors.labels(
                region_label, tenant_label, fabric_label, workflow_label
            ).inc()
            raise e

    @abstractmethod
    def run(self, records) -> None:
        """Execute the steps for preparing/writing records to S3. (default)"""
        self.records = records
        # prepare records for writing
        self._prepare_records()
        # calculate metrics
        export_time = datetime.now(timezone.utc)
        for r in self.records:
            lag: timedelta = export_time - r["time_extracted"]
            export_lag.labels(
                region_label, tenant_label, fabric_label, workflow_label
            ).set(lag.total_seconds())
        # write records to S3
        self._write()

    @abstractmethod
    def _prepare_records(self) -> None:
        """Execute record prep. (default)"""
        if self.config.get("include_process_date", None):
            self.records = self.append_process_date(self.records)
        if self.config.get("flatten_records", None):
            # flatten records
            self.records = list(
                map(lambda record: self.flatten_record(record), self.records)
            )

    def delete(self, records) -> None:
        """Delete objects with provided keys, from the bucket."""
        try:
            if len(records):
                response: dict = self.client.delete_objects(
                    Bucket=self.bucket, Delete={"Objects": records}
                )
                if response.get("Errors"):
                    self.logger.error(
                        f"Failed to delete objects from the bucket: {response.get('Errors')}"
                    )
                    # Increment export_errors metric
                    export_errors.labels(
                        region_label, tenant_label, fabric_label, workflow_label
                    ).inc(len(response.get("Errors")))
        except Exception as e:
            # Increment export_errors metric
            export_errors.labels(
                region_label, tenant_label, fabric_label, workflow_label
            ).inc()
            raise e

    def create_key(self, record: dict = None) -> str:
        batch_start = self.context["batch_start_time"]
        stream_name = (
            self.context["stream_name"]
            if self.stream_name_path_override is None
            else self.stream_name_path_override
        )
        folder_path = (
            f"{self.bucket}{f'/{self.prefix}' if self.prefix else ''}/{stream_name}/"
        )
        file_name = ""
        if record:
            file_name = record.get("_key", "")
        else:
            if self.config["append_date_to_filename"]:
                grain = DATE_GRAIN[self.config["append_date_to_filename_grain"].lower()]
                file_name += f"{self.create_file_structure(batch_start, grain)}"

        return f"{folder_path}{file_name}"

    def create_file_structure(self, batch_start: datetime, grain: int) -> str:
        ret = ""
        ret += f"{batch_start.year}" if grain <= DATE_GRAIN["year"] else ""
        ret += f"{batch_start.month:02}" if grain <= DATE_GRAIN["month"] else ""
        ret += f"{batch_start.day:02}" if grain <= DATE_GRAIN["day"] else ""
        ret += f"-{batch_start.hour:02}" if grain <= DATE_GRAIN["hour"] else ""
        ret += f"{batch_start.minute:02}" if grain <= DATE_GRAIN["minute"] else ""
        ret += f"{batch_start.second:02}" if grain <= DATE_GRAIN["second"] else ""
        ret += (
            f"{batch_start.microsecond}" if grain <= DATE_GRAIN["microsecond"] else ""
        )
        return ret

    def flatten_key(self, k, parent_key, sep) -> str:
        """"""
        # TODO: standardize in the SDK?
        full_key = parent_key + [k]
        inflected_key = [n for n in full_key]
        reducer_index = 0
        while len(sep.join(inflected_key)) >= 255 and reducer_index < len(
            inflected_key
        ):
            reduced_key = re.sub(
                r"[a-z]", "", inflection.camelize(inflected_key[reducer_index])
            )
            inflected_key[reducer_index] = (
                reduced_key
                if len(reduced_key) > 1
                else inflected_key[reducer_index][0:3]
            ).lower()
            reducer_index += 1

        return sep.join(inflected_key)

    def flatten_record(self, d, parent_key=[], sep="__") -> dict:
        """"""
        # TODO: standardize in the SDK?
        items = []
        for k in sorted(d.keys()):
            v = d[k]
            new_key = self.flatten_key(k, parent_key, sep)
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten_record(v, parent_key + [k], sep=sep).items())
            else:
                items.append((new_key, json.dumps(v) if type(v) is list else v))
        return dict(items)

    def append_process_date(self, records) -> dict:
        """A function that appends the current UTC to every record"""

        def process_date(record):
            record["_PROCESS_DATE"] = datetime.utcnow().isoformat()
            return record

        return list(map(lambda x: process_date(x), records))
