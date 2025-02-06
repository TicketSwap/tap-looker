"""Custom client handling, including LookerStream base class."""

from __future__ import annotations
from enum import Enum
import json
import os
import typing as t
from datetime import datetime
from pathlib import Path

import looker_sdk
from looker_sdk.sdk.api40 import models
from singer_sdk.streams import Stream

if t.TYPE_CHECKING:
    from singer_sdk import Tap
    from singer_sdk.helpers.types import Context

ROW_LIMIT = 5000
SCHEMAS_DIR = Path(__file__).parent / "schemas"


class LookerStream(Stream):
    """Stream class for Looker streams."""

    def __init__(self, tap: Tap):
        super().__init__(tap)
        os.environ["LOOKERSDK_BASE_URL"] = self.config.get("base_url")
        os.environ["LOOKERSDK_CLIENT_ID"] = self.config.get("client_id")
        os.environ["LOOKERSDK_CLIENT_SECRET"] = self.config.get("client_secret")
        self.sdk = looker_sdk.init40()

    @property
    def schema_filepath(self) -> Path | None:
        """Get path to schema file.

        Returns:
            Path to a schema file for the stream or `None` if n/a.
        """
        return SCHEMAS_DIR / f"{self.name}.json"

    def convert_to_dict(self, obj: object) -> dict:
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, list):
            return [self.convert_to_dict(item) for item in obj]
        if isinstance(obj, dict):
            return {key: self.convert_to_dict(value) for key, value in obj.items()}
        if hasattr(obj, "__dict__"):
            return self.convert_to_dict(obj.__dict__)
        return obj


class LookerSystemActivityStream(LookerStream):
    def __init__(self, tap: Tap):
        super().__init__(tap)
        self.replication_key = f"{self.name}.created_time"
        self.primary_keys = [f"{self.name}.id"]

    def get_records(
        self,
        context: Context | None,
    ) -> t.Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.

        Raises:
            NotImplementedError: If the implementation is TODO
        """
        result_count: int = ROW_LIMIT - 1
        result_max_date: datetime = self.get_starting_timestamp(context)
        while result_count != ROW_LIMIT:
            response = self.sdk.run_inline_query(
                result_format="json",
                body=models.WriteQuery(
                    model="system__activity",
                    view=self.name,
                    fields=list(self.schema["properties"].keys()),
                    filters={
                        self.replication_key: f"after {result_max_date.strftime('%Y-%m-%d %H:%M:%S')}",
                    },
                ),
                limit=ROW_LIMIT,
            )
            response_results = json.loads(response)
            result_count = len(response_results)
            result_max_date = datetime.strptime(  # noqa: DTZ007
                response_results[-1][self.replication_key],
                "%Y-%m-%d %H:%M:%S",
            )
            yield from response_results
