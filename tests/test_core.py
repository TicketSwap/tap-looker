"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class, SuiteConfig

from tap_looker.tap import TapLooker

SAMPLE_CONFIG = {
    "start_date": (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "base_url": "https://ticketswap.eu.looker.com/",
    "client_id": os.environ.get("LOOKERSDK_CLIENT_ID"),
    "client_secret": os.environ.get("LOOKERSDK_CLIENT_SECRET"),
    "filter_explores": ["tickets"],
}

TEST_SUITE_CONFIG = SuiteConfig(max_records_limit=10)

# Run standard built-in tap tests from the SDK:
TestTapLooker = get_tap_test_class(
    tap_class=TapLooker,
    config=SAMPLE_CONFIG,
    suite_config=TEST_SUITE_CONFIG,
)
