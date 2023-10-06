import hashlib
from datetime import datetime
from typing import Any

import ecdsa
from uagents.crypto import Identity

from verifyaname.helpers import (
    AGENT_ADDRESS_PREFIX,
    SIGNATURE_PREFIX,
    decode_bech32,
    encode_length_prefixed,
)


def _generate_digest(
    contract_address: str,
    domain: str,
    address: str,
    expiry: int,
    chain_id: str,
):
    hasher = hashlib.sha256()
    hasher.update(encode_length_prefixed(contract_address))
    hasher.update(encode_length_prefixed(domain))
    hasher.update(encode_length_prefixed(address))
    hasher.update(encode_length_prefixed(expiry))
    hasher.update(encode_length_prefixed(chain_id))

    return hasher.digest()


def _signed_digest(
    identity: Identity,
    contract_address: str,
    domain: str,
    address: str,
    expiry: int,
    chain_id: str,
) -> str:
    return identity.sign_digest(
        _generate_digest(contract_address, domain, address, expiry, chain_id)
    )


def generate_approval_token(
    identity: Identity,
    contract_address: str,
    domain: str,
    address: str,
    expiry: datetime,
    chain_id: str,
) -> Any:
    oracle_wallet_pubkey = identity.address
    seconds_since_epoch = int(expiry.timestamp())
    nanos_since_epoch = int(seconds_since_epoch * 10**9)

    signature = _signed_digest(
        identity, contract_address, domain, address, seconds_since_epoch, chain_id
    )

    verification_dict = {
        "oracle_agent_address": oracle_wallet_pubkey,
        "signature": signature,
        "expiry": str(nanos_since_epoch),
    }

    return verification_dict


def _verify_signature(
    signature: str,
    contract_address: str,
    domain: str,
    oracle_agent_address: str,
    address: str,
    expiry: datetime,
    chain_id: str,
) -> bool:
    # This is just a mock implementation of signature verification - it will be done onchain

    seconds_since_epoch = int(expiry.timestamp())
    digest = _generate_digest(
        contract_address, domain, address, seconds_since_epoch, chain_id
    )

    oracle_pk_prefix, oracle_pk_data = decode_bech32(oracle_agent_address)

    sig_prefix, sig_data = decode_bech32(signature)

    if oracle_pk_prefix != AGENT_ADDRESS_PREFIX:
        raise ValueError("Unable to decode oracle public key")

    if sig_prefix != SIGNATURE_PREFIX:
        raise ValueError("Unable to decode signature")

    # build the verifying key
    verifying_key = ecdsa.VerifyingKey.from_string(
        oracle_pk_data, curve=ecdsa.SECP256k1
    )

    try:
        result = verifying_key.verify_digest(sig_data, digest)
    except ecdsa.keys.BadSignatureError:
        return False

    return result


def verify_token(
    approval_token: dict,
    contract_address: str,
    domain: str,
    address: str,
    chain_id: str,
) -> bool:
    # This is just a mock implementation of approval token verification - it will be done onchain

    signature = approval_token["signature"]
    oracle_agent_address = approval_token["oracle_agent_address"]
    expiry = datetime.fromtimestamp(int(approval_token["expiry"]) // 10**9)

    # Onchain verification will consist of:
    # Verify if oracle_wallet_pubkey belongs to the oracle address
    # Verify if the address from owner_wallet_pubkey is the same as info.sender

    return _verify_signature(
        signature,
        contract_address,
        domain,
        oracle_agent_address,
        address,
        expiry,
        chain_id,
    )
