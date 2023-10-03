from typing import List

from license_utils.build_licenses import SpdxLicense
from license_utils.normalize import normalize
from license_utils.sorensen_dice import get_dice_coefficient


def compute_match_scores(
    inputText, licenses: List[SpdxLicense], return_first_threshold: float | None = None
) -> dict[str, float] | SpdxLicense:
    """Normalizes the given license text and forms bigrams before comparing it
    with a database of known licenses.

    Arguments:
        text {string} -- text is the license text input by the user.
        licenses {list} -- list of licenses to compare the input text with.
        return_first_threshold {float} -- if set, will return the first license with a match score above this threshold. If not found, returns all matches.

    Returns:
        dictionary -- dictionary with license name as key and dice coefficient as value, or the first license with a match score above the threshold.
    """
    matches = {}
    normalizedInputText = normalize(inputText)
    for license in licenses:
        matches[license.spdx_id] = get_dice_coefficient(
            normalizedInputText, license.normalized_text
        )
        if (
            return_first_threshold != None
            and matches[license.spdx_id] >= return_first_threshold
        ):
            return license
    return matches
