import base64
import aiohttp
from typing import Tuple

from bovine.jsonld import with_external_context
from bovine.utils.date import parse_gmt, check_max_offset_now


def find_with_item(key_list, key_id):
    for key in key_list:
        if key.get("id") == key_id:
            return key
    return None


def public_key_owner_from_dict(
    actor: dict, key_id: str
) -> Tuple[str | None, str | None]:
    public_key_data = actor.get("publicKey", {})

    if isinstance(public_key_data, list):
        if len(public_key_data) == 1:
            public_key_data = public_key_data[0]
        else:
            public_key_data = find_with_item(public_key_data, key_id)

    if not public_key_data:
        return None, None

    public_key = public_key_data.get("publicKeyPem")
    owner = public_key_data.get("owner")

    return public_key, owner


def actor_object_to_public_key(
    actor: dict, key_id: str
) -> Tuple[str | None, str | None]:
    public_key, owner = public_key_owner_from_dict(with_external_context(actor), key_id)

    if public_key and owner:
        return public_key, owner

    return public_key_owner_from_dict(actor, key_id)


def validate_basic_signature_fields(message, request, signature):
    if "(request-target)" not in signature.fields:
        return message.error("(request-target) must be a signature field")

    if "host" not in signature.fields:
        return message.error("host must be a signature field")

    if "date" not in signature.fields:
        return message.error("date must be a signature field")

    date_header = request.headers.get("date")
    message.add(f"Got date header {date_header}")

    try:
        date_parsed = parse_gmt(date_header)
    except Exception as e:
        return message.error(["Failed to parse date", repr(e)])

    if not check_max_offset_now(date_parsed):
        return message.error(["Date not within the last 5 minutes"])

    return None


async def retrieve_public_key(message, key_id, request):
    if key_id == "about:inline":
        try:
            public_key = base64.standard_b64decode(
                request.headers.get("X-Public-Key")
            ).decode("utf-8")
        except Exception:
            public_key = None
        if not public_key:
            return None, message.error(
                "Please set the header 'X-Public-Key' to provide a public key"
            )
    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(key_id) as response:
                    if "json" in response.headers.get("content-type"):
                        data = await response.json()
                        public_key, _ = actor_object_to_public_key(data)
                    else:
                        public_key = await response.text()
        except Exception as e:
            return (
                None,
                message.error(
                    [
                        "Failed to fetch public key",
                        "Use about:inline to include a public key in a header",
                        "    about:inline is expected to be base64 encoded",
                        "or make sure keyId can be resolved to a public key",
                        repr(e),
                    ]
                ),
            )

    return public_key, None
