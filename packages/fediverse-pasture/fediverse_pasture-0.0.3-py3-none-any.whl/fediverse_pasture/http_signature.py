import base64
import logging
import click
from quart import Quart, request

from bovine.crypto.helper import sign_message
from bovine.crypto.signature import Signature
from bovine.crypto.http_signature import build_signature

from .server.utils import validate_basic_signature_fields, retrieve_public_key
from .types import Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--port", default=2909, help="port to run on")
def http_signature(port):
    app = Quart(__name__)

    @app.get("/")
    async def get_handler():
        message = Message()
        message.add("Got get request")

        signature_header = request.headers.get("signature")
        if not signature_header:
            return message.error("Signature header is missing"), 401

        message.add(f"Signature header '{signature_header}'")

        try:
            signature = Signature.from_signature_header(signature_header)
        except Exception as e:
            return (
                message.error(
                    [
                        "Failed to parse signature",
                        repr(e),
                    ]
                ),
                401,
            )

        message.add(f"""Got fields {", ".join(signature.fields)}""")

        error_dict = validate_basic_signature_fields(message, request, signature)

        if error_dict:
            return error_dict, 401

        header_fields = [x for x in signature.fields if x[0] != "("]

        http_signature = build_signature("http_signature", "get", request.path)

        for x in header_fields:
            if x != "host":
                http_signature.with_field(x, request.headers.get(x))

        message.add(f"""Message to sign "{http_signature.build_message()}" """)
        message.add(f"Got key id {signature.key_id}")

        public_key, error_dict = await retrieve_public_key(
            message, signature.key_id, request
        )

        if error_dict:
            return error_dict, 401

        message.add(f"""Got public key "{public_key}" """)

        try:
            result = http_signature.verify(
                public_key=public_key, signature=signature.signature
            )
        except Exception as e:
            return (
                message.error(
                    [
                        "Something went wrong when verifying signature",
                        repr(e),
                    ]
                ),
                401,
            )

        if not result:
            private_key = request.headers.get("X-Private-Key")

            if private_key is None:
                message.add(
                    "Set X-Private-Key to your base64 encoded private key\
                        for expected signature",
                )
            else:
                message.add("Expected signature:")
                message.add(
                    sign_message(
                        private_key=base64.standard_b64decode(private_key).decode(
                            "utf-8"
                        ),
                        message=http_signature.build_message(),
                    )
                )

            return message.error("Invalid signature"), 401
        else:
            message.add("SUCCESS!!!")

        return message.response, 200 if result else 401

    app.run(port=port, host="0.0.0.0", use_reloader=True)


if __name__ == "__main__":
    http_signature()
