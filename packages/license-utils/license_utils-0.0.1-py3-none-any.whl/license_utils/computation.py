from typing import List

from license_utils.build_licenses import SpdxLicense
from license_utils.normalize import normalize
from license_utils.sorensen_dice import get_dice_coefficient


def compute_match_scores(inputText, licenses: List[SpdxLicense]):
    """Normalizes the given license text and forms bigrams before comparing it
    with a database of known licenses.

    Arguments:
        text {string} -- text is the license text input by the user.

    Returns:
        dictionary -- dictionary with license name as key and dice coefficient as value.
    """
    matches = {}
    normalizedInputText = normalize(inputText)
    for license in licenses:
        matches[license.spdx_id] = get_dice_coefficient(
            normalizedInputText, license.normalized_text
        )
    return matches
