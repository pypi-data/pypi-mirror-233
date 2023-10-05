"""s3 target class."""

from __future__ import annotations

import time
import typing as t
from pathlib import PurePath
from threading import Lock, Thread

from prometheus_client import start_http_server
from singer_sdk import typing as th
from singer_sdk.target_base import Target

from macrometa_target_s3.constants import (
    export_errors,
    fabric_label,
    region_label,
    registry_package,
    tenant_label,
    workflow_label,
)
from macrometa_target_s3.formats.format_base import DATE_GRAIN
from macrometa_target_s3.sinks import s3Sink


class Targets3(Target):
    """Sample target for s3."""

    name = "macrometa-target-s3"
    flush_lock = Lock()
    default_sink_class = s3Sink

    def __init__(
        self,
        *,
        config: dict | PurePath | str | list[PurePath | str] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )
        # Start the Prometheus HTTP server for exposing metrics
        self.logger.info("S3 target is starting the metrics server.")
        start_http_server(8001, registry=registry_package)

    config_jsonschema = th.PropertiesList(
        th.Property(
            "format",
            th.ObjectType(
                th.Property(
                    "format_type",
                    th.StringType,
                    required=True,
                    allowed_values=[
                        "parquet",
                        "json",
                    ],  # TODO: configure this from class
                ),
                th.Property(
                    "format_parquet",
                    th.ObjectType(
                        th.Property(
                            "validate",
                            th.BooleanType,
                            required=False,
                            default=False,
                        ),
                    ),
                    required=False,
                ),
                th.Property(
                    "format_json",
                    th.ObjectType(),
                    required=False,
                ),
                th.Property(
                    "format_csv",
                    th.ObjectType(),
                    required=False,
                ),
            ),
        ),
        th.Property(
            "cloud_provider",
            th.ObjectType(
                th.Property(
                    "cloud_provider_type",
                    th.StringType,
                    required=True,
                    allowed_values=["aws"],  # TODO: configure this from class
                ),
                th.Property(
                    "aws",
                    th.ObjectType(
                        th.Property(
                            "aws_access_key_id",
                            th.StringType,
                            required=True,
                            secret=True,
                        ),
                        th.Property(
                            "aws_secret_access_key",
                            th.StringType,
                            required=True,
                            secret=True,
                        ),
                        th.Property(
                            "aws_session_token",
                            th.StringType,
                            required=False,
                            secret=True,
                        ),
                        th.Property(
                            "aws_region",
                            th.StringType,
                            required=True,
                        ),
                        th.Property(
                            "aws_profile_name",
                            th.StringType,
                            required=False,
                        ),
                        th.Property(
                            "aws_bucket",
                            th.StringType,
                            required=True,
                        ),
                        th.Property(
                            "aws_endpoint_override",
                            th.StringType,
                            required=False,
                        ),
                    ),
                    required=False,
                ),
            ),
        ),
        th.Property(
            "prefix",
            th.StringType,
            description="The prefix for the key.",
        ),
        th.Property(
            "stream_name_path_override",
            th.StringType,
            description="The S3 key stream name override.",
        ),
        th.Property(
            "include_process_date",
            th.BooleanType,
            description="A flag indicating whether to append _process_date to record.",
            default=False,
        ),
        th.Property(
            "append_date_to_prefix",
            th.BooleanType,
            description="A flag to append the date to the key prefix.",
            default=False,
        ),
        th.Property(
            "partition_name_enabled",
            th.BooleanType,
            description="A flag (only works if append_date_to_prefix is enabled) to have partitioning name formatted e.g. 'year=2023/month=01/day=01'.",
            default=False,
        ),
        th.Property(
            "append_date_to_prefix_grain",
            th.StringType,
            description="The grain of the date to append to the prefix.",
            allowed_values=DATE_GRAIN.keys(),
            default="day",
        ),
        th.Property(
            "append_date_to_filename",
            th.BooleanType,
            description="A flag to append the date to the key filename.",
            default=True,
        ),
        th.Property(
            "append_date_to_filename_grain",
            th.StringType,
            description="The grain of the date to append to the filename.",
            allowed_values=DATE_GRAIN.keys(),
            default="microsecond",
        ),
        th.Property(
            "flatten_records",
            th.BooleanType,
            description="A flag indictating to flatten records.",
        ),
        th.Property(
            "batch_flush_interval",
            th.IntegerType,
            default=60,
            description="Batch flush interval in seconds.",
        ),
        th.Property(
            "hard_delete",
            th.BooleanType,
            description="Hard Delete",
            default=True,
        ),
        th.Property(
            "object_per_record",
            th.BooleanType,
            description="Create object in S3 bucket for each record in data source.",
            default=True,
        ),
    ).to_dict()

    def _validate_config(
        self, *, raise_errors: bool = True, warnings_as_errors: bool = False
    ) -> tuple[list[str], list[str]]:
        ref_config = self._config.copy()
        self._config = {
            "format": {
                "format_type": ref_config.get("format").lower(),
            },
            "cloud_provider": {
                "cloud_provider_type": "aws",
                "aws": {
                    "aws_access_key_id": ref_config.get("access_key"),
                    "aws_secret_access_key": ref_config.get("secret_access_key"),
                    "aws_region": ref_config.get("region"),
                    "aws_profile_name": ref_config.get("profile_name"),
                    "aws_bucket": ref_config.get("bucket"),
                },
            },
            "batch_flush_interval": ref_config.get("batch_flush_interval"),
            "prefix": ref_config.get("prefix"),
            "hard_delete": ref_config.get("hard_delete"),
            "object_per_record": ref_config.get("object_per_record"),
            "stream_name_path_override": ref_config.get("target_directory"),
        }
        return super()._validate_config(
            raise_errors=raise_errors, warnings_as_errors=warnings_as_errors
        )

    def _process_lines(self, file_input: t.IO[str]) -> t.Counter[str]:
        flusher = Thread(
            target=self._flush_task, args=[self.config.get("batch_flush_interval")]
        )
        flusher.start()
        try:
            counter = super()._process_lines(file_input)
        except Exception as e:
            # Increment export_errors metric
            export_errors.labels(
                region_label, tenant_label, fabric_label, workflow_label
            ).inc()
            raise e

        # Process any missed records before exiting
        with self.flush_lock:
            self.drain_all()

        return counter

    def _flush_task(self, interval) -> None:
        while True:
            time.sleep(interval)
            self.logger.info(
                "Max age %ss reached for the batch. Draining all sinks.",
                interval,
            )
            with self.flush_lock:
                self.drain_all()

    def _handle_max_record_age(self) -> None:
        return


if __name__ == "__main__":
    Targets3.cli()
