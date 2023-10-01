import asyncio
import dataclasses
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict, List

import requests
from aiohttp import ClientSession, TCPConnector

from license_utils.normalize import normalize

# TODO make configurable
MAX_SIM_CONNECTIONS = 100


@dataclasses.dataclass
class SpdxLicense:
    spdx_id: str
    name: str
    datails_url: str
    is_deprecated_id: bool
    reference_number: int
    is_osi_approved: bool | None
    is_fsf_free: bool | None
    text: str | None = None
    _normalized_text: str | None = None

    async def load_text_if_not_set(
        self, session: ClientSession, semaphore: asyncio.BoundedSemaphore
    ):
        if self.text == None:
            async with semaphore:
                logging.info(f"Downloading license text for {self.spdx_id}")
                async with session.get(self.datails_url) as response:
                    if response.status != 200:
                        raise RuntimeError(
                            f"Received reponse with status {response.status} "
                            + f"when downloading url `{self.datails_url}`"
                        )
                    response_json = await response.json()
                    self.text = response_json["licenseText"]
                    self._normalized_text = normalize(self.text)
                    # TODO: there's other fields we may want to store
                logging.info(f"Downloaded license text for {self.spdx_id}")

    @property
    def normalized_text(self) -> str:
        if self._normalized_text == None:
            raise RuntimeError("License text not loaded")
        return self._normalized_text


async def fetch_spdx_licenses(load_text: bool) -> List[SpdxLicense]:
    url = "https://spdx.org/licenses/licenses.json"

    response = requests.get(url)
    licensesJson = response.json()["licenses"]

    licenses = [
        SpdxLicense(
            spdx_id=j["licenseId"],
            name=j["name"],
            datails_url=j["detailsUrl"],
            is_deprecated_id=j["isDeprecatedLicenseId"],
            reference_number=j["referenceNumber"],
            is_osi_approved=j.get("isOsiApproved", None),
            is_fsf_free=j.get("isFsfLibre", None),
        )
        for j in licensesJson
    ]

    if load_text:
        semaphore = asyncio.BoundedSemaphore(MAX_SIM_CONNECTIONS)

        awaitables = []
        connector = TCPConnector(limit=MAX_SIM_CONNECTIONS)
        async with ClientSession(connector=connector) as session:
            for l in licenses:
                awaitables.append(
                    l.load_text_if_not_set(session=session, semaphore=semaphore)
                )

            await asyncio.gather(*awaitables)

    return licenses


def load_licenses_from_dict(dict_licenses: List[Dict]) -> List[SpdxLicense]:
    return [SpdxLicense(**j) for j in dict_licenses]
