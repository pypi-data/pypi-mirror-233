from datetime import datetime
from decimal import Decimal
from json import JSONEncoder, dumps

from bson import ObjectId

from macrometa_target_s3.formats.format_base import FormatBase


class JsonSerialize(JSONEncoder):
    def default(self, obj: any) -> any:
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        else:
            raise TypeError(f"Type {type(obj)} not serializable")


class FormatJson(FormatBase):
    def __init__(self, config, context) -> None:
        super().__init__(config, context, "json")
        pass

    def _prepare_records(self):
        # use default behavior, no additional prep needed
        # TODO: validate json records?
        return super()._prepare_records()

    def _write(self) -> None:
        if not self.object_per_record:
            modified: list = []
            for r in self.records:
                if not r.get("_sdc_deleted_at") and len(r) > 2:
                    modified.append(r)
            
            if len(modified):
                return super()._write(dumps(modified, cls=JsonSerialize))
            else:
                return

        deleted_records: list = []
        for r in self.records:
            key: str = self.create_key(r)

            # having just 2 properties means only _key and time_extracted is available.
            # this means this is a DELETE record.
            if r.get("_sdc_deleted_at") or len(r) < 3:
                deleted_records.append(
                    {"Key": f"{key.split('/', 1)[1]}.{self.extension}"}
                )
            else:
                super()._write(dumps(r, cls=JsonSerialize), key)

        # delete files if hard_delete is enabled and object_to_record is enabled
        if self.config["hard_delete"] and self.object_per_record:
            super().delete(deleted_records)

    def run(self) -> None:
        # use default behavior, no additional run steps needed
        return super().run(self.context["records"])
