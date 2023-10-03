import pytest

from license_utils.build_licenses import fetch_spdx_licenses


@pytest.mark.asyncio
async def test_build_licenses():
    licenses = await fetch_spdx_licenses(load_text=True)

    assert len(licenses) > 500
    assert all(license.text != None for license in licenses)

    assert [license for license in licenses if license.spdx_id == "MIT"][
        0
    ].text.startswith("MIT License")
