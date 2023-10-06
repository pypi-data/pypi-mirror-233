import base64
import hashlib
from dataclasses import dataclass

from verifyaname.helpers import encode_length_prefixed

TXT_VERIFICATION_KEY = "fetch-ans-token"
CHAIN_ID = "verification"


def _generate_digest(domain: str, address: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(encode_length_prefixed(domain))
    hasher.update(encode_length_prefixed(address))
    return hasher.digest()


def generate_verification_string(domain: str, address: str) -> str:
    return VerificationData(digest=_generate_digest(domain, address)).encode()


@dataclass
class VerificationData:
    digest: bytes

    @staticmethod
    def _safe_base64_encode(data: bytes):
        """
        Removes any `=` used as padding from the encoded string.
        """
        encoded = base64.urlsafe_b64encode(data).decode()
        return encoded.rstrip("=")

    @staticmethod
    def _safe_base64_decode(data: str):
        """
        Adds back in the required padding before decoding.
        """
        padding = 4 - (len(data) % 4)
        string = data + ("=" * padding)
        return base64.urlsafe_b64decode(string)

    @staticmethod
    def decode(verification_string: str) -> "VerificationData":
        decoded_verification = VerificationData._safe_base64_decode(verification_string)
        return VerificationData(decoded_verification)

    def encode(self) -> str:
        return VerificationData._safe_base64_encode(self.digest)


def verify_domain_string(
    data: VerificationData,
    domain: str,
    address: str,
) -> bool:
    # Verify the signature
    digest = _generate_digest(domain, address)

    return data.digest == digest
