import struct
from typing import Tuple, Union

import bech32

SIGNATURE_PREFIX = "sig"
PUBLIC_KEY_PREFIX = "pub"
AGENT_ADDRESS_PREFIX = "agent"


def encode_length_prefixed(value: Union[str, int, bytes]) -> bytes:
    if isinstance(value, str):
        encoded = value.encode()
    elif isinstance(value, int):
        encoded = struct.pack(">Q", value)
    elif isinstance(value, bytes):
        encoded = value
    else:
        assert False

    length = len(encoded)
    prefix = struct.pack(">Q", length)

    return prefix + encoded


def decode_bech32(value: str) -> Tuple[str, bytes]:
    prefix, data_base5 = bech32.bech32_decode(value)
    data = bytes(bech32.convertbits(data_base5, 5, 8, False))
    return prefix, data


def encode_bech32(prefix: str, value: bytes) -> str:
    value_base5 = bech32.convertbits(value, 8, 5)
    return bech32.bech32_encode(prefix, value_base5)


def encode_public_key(pubkey: bytes) -> str:
    return encode_bech32(PUBLIC_KEY_PREFIX, pubkey)
