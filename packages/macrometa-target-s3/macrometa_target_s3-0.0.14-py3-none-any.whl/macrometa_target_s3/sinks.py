"""s3 target sink class, which handles writing streams."""

from __future__ import annotations

import datetime
import logging

from c8connector import ensure_datetime
from singer_sdk.sinks import BatchSink

from macrometa_target_s3.formats.format_base import FormatBase, format_type_factory
from macrometa_target_s3.formats.format_csv import FormatCsv
from macrometa_target_s3.formats.format_json import FormatJson
from macrometa_target_s3.formats.format_parquet import FormatParquet

LOGGER = logging.getLogger("macrometa-target-s3")
FORMAT_TYPE = {"parquet": FormatParquet, "csv": FormatCsv, "json": FormatJson}


class s3Sink(BatchSink):
    """s3 target sink class."""

    MAX_SIZE = 10000  # Max records to write in one batch

    def __init__(
        self,
        target: any,
        stream_name: str,
        schema: dict,
        key_properties: list[str] | None,
    ) -> None:
        super().__init__(target, stream_name, schema, key_properties)
        # what type of file are we building?
        self.format_type = self.config.get("format", None).get("format_type", None)
        if self.format_type:
            if self.format_type not in FORMAT_TYPE:
                raise Exception(
                    f"Unknown file type specified. {key_properties['type']}"
                )
        else:
            raise Exception("No file type supplied.")

    @property
    def is_full(self) -> bool:
        return False
    
    @property
    def current_size(self) -> int:
        pending_size = len(self._pending_batch.get('records', [])) if self._pending_batch else 0
        return self._batch_records_read or pending_size

    def _add_sdc_metadata_to_record(
        self,
        record: dict,
        message: dict,
        context: dict,
    ) -> None:
        record["_sdc_extracted_at"] = message.get("time_extracted")
        record["_sdc_batched_at"] = (
            context.get("batch_start_time", None)
            or datetime.datetime.now(tz=datetime.timezone.utc)
        ).isoformat()
        record["_sdc_deleted_at"] = record.get("_sdc_deleted_at")

    def _add_sdc_metadata_to_schema(self) -> None:
        properties_dict = self.schema["properties"]
        for col in (
            "_sdc_extracted_at",
            "_sdc_batched_at",
            "_sdc_deleted_at",
        ):
            properties_dict[col] = {
                "type": ["null", "string"],
                "format": "date-time",
            }

    def _remove_sdc_metadata_from_schema(self) -> None:
        properties_dict = self.schema["properties"]
        for col in (
            "_sdc_extracted_at",
            "_sdc_received_at",
            "_sdc_batched_at",
            "_sdc_sequence",
            "_sdc_table_version",
        ):
            properties_dict.pop(col, None)

        # We need `_sdc_deleted_at` column if `hard_delete` is enabled
        if not self.config.get("hard_delete"):
            properties_dict.pop("_sdc_deleted_at")

    def _remove_sdc_metadata_from_record(self, record: dict) -> None:
        record.pop("_sdc_extracted_at", None)
        record.pop("_sdc_received_at", None)
        record.pop("_sdc_batched_at", None)
        record.pop("_sdc_sequence", None)
        record.pop("_sdc_table_version", None)
        # We need `_sdc_deleted_at` value if `hard_delete` is enabled
        if not self.config.get("hard_delete"):
            record.pop("_sdc_deleted_at", None)

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        # add stream name to context
        context["stream_name"] = self.stream_name
        context["logger"] = self.logger
        # creates new object for each batch
        format_type_client = format_type_factory(
            FORMAT_TYPE[self.format_type], self.config, context
        )
        # force base object_type_client to object_type_base class
        assert (
            isinstance(format_type_client, FormatBase) is True
        ), f"format_type_client must be of type Base; Type: {type(self.format_type_client)}."

        format_type_client.run()

    def process_record(self, record: dict, context: dict) -> None:
        # Record extracted time for metric calculations
        if "time_extracted" not in record:
            record["time_extracted"] = datetime.datetime.now(datetime.timezone.utc)
        else:
            record["time_extracted"] = ensure_datetime(record["time_extracted"])
        super().process_record(record, context)
