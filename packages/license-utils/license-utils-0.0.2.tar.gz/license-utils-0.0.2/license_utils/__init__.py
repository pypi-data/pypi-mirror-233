__version__ = "0.0.2"

from .build_licenses import SpdxLicense
from .matcher import SpdxLicenseUtils

__all__ = ["SpdxLicenseUtils", "SpdxLicense"]
