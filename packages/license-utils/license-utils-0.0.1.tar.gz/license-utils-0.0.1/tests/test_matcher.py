import os

import pytest
import requests

from license_utils import matcher


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "github_path,spdx_id",
    [
        (
            "testingautomated-usi/bisupervised/bd2046e651cbed5b609026c3344e926f189fa105/LICENSE",
            "MIT",
        ),
        (
            "upscayl/upscayl/568224182510952690d057c2708f3e932807f5ff/LICENSE",
            "AGPL-3.0",
        ),
    ],
)
async def test_matcher(github_path: str, spdx_id: str):
    # Download the license text from github, if not already cached
    local_license_path = os.path.join(
        "tests/resources/licenses", github_path.replace("/", "_")
    )
    try:
        with open(local_license_path, "r") as f:
            license_text = f.read()
    except FileNotFoundError:
        os.makedirs(os.path.dirname(local_license_path), exist_ok=True)
        response = requests.get(f"https://raw.githubusercontent.com/{github_path}")
        license_text = response.text
        with open(local_license_path, "w") as f:
            f.write(license_text)

    license_utils = await matcher.SpdxLicenseUtils.create(
        cache_file="tests/resources/.license_cache.json"
    )

    matching = license_utils.match_text_to_id(license_text)

    assert matching[spdx_id] > 0.95
    assert matching[spdx_id] == max(matching.values())
