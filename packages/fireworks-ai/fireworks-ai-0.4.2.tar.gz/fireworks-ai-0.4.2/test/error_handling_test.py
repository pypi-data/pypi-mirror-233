import time
import fireworks.client
import unittest
import os
from fireworks.client.error import InvalidRequestError, AuthenticationError
import sys
import asyncio

MODEL = "accounts/fireworks/models/llama-v2-7b-chat"
PROMPT = "Hello there! What is your favorite city and why?"
MAX_TOKENS = 100
MESSAGE = [{"role": "user", "content": PROMPT}]


class TestFireworksClientErrorHandling(unittest.TestCase):
    def test_invalid_request(self):
        fireworks.client.api_key = os.environ.get("API_KEY")

        with self.assertRaisesRegex(
            InvalidRequestError,
            "temperature must be between 0 and 2",
        ):
            fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, temperature=-0.5
            )

        with self.assertRaisesRegex(
            InvalidRequestError,
            "extra fields not permitted",
        ):
            fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, dummy=0
            )

        with self.assertRaisesRegex(
            InvalidRequestError,
            "value is not a valid integer",
        ):
            fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, n="5"
            )

        with self.assertRaisesRegex(
            InvalidRequestError,
            "value is not a valid boolean",
        ):
            fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, echo=0
            )

        with self.assertRaisesRegex(
            InvalidRequestError,
            "value is not a valid boolean",
        ):
            fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, stream=0
            )

        # test ChatCompletion
        with self.assertRaisesRegex(
            InvalidRequestError,
            "temperature must be between 0 and 2",
        ):
            fireworks.client.ChatCompletion.create(
                model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS, temperature=-0.5
            )

        with self.assertRaisesRegex(
            InvalidRequestError,
            "extra fields not permitted",
        ):
            fireworks.client.ChatCompletion.create(
                model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS, dummy=0
            )

    def test_invalid_request_streaming(self):
        fireworks.client.api_key = os.environ.get("API_KEY")

        with self.assertRaisesRegex(
            InvalidRequestError,
            "temperature must be between 0 and 2",
        ):
            for resp in fireworks.client.Completion.create(
                model=MODEL,
                prompt=PROMPT,
                max_tokens=MAX_TOKENS,
                temperature=-0.5,
                stream=True,
            ):
                print(resp)

        with self.assertRaisesRegex(
            InvalidRequestError,
            "extra fields not permitted",
        ):
            for resp in fireworks.client.Completion.create(
                model=MODEL,
                prompt=PROMPT,
                max_tokens=MAX_TOKENS,
                dummy=0,
                stream=True,
            ):
                print(resp)

        with self.assertRaisesRegex(
            InvalidRequestError,
            "value is not a valid integer",
        ):
            for resp in fireworks.client.Completion.create(
                model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, n="5", stream=True
            ):
                print(resp)

        # test async
        with self.assertRaisesRegex(
            InvalidRequestError,
            "value is not a valid integer",
        ):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._async_streaming())

    async def _async_streaming(self):
        async for resp in fireworks.client.Completion.acreate(
            model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, n="5", stream=True
        ):
            print(resp)

    def test_authentication_error(self):
        with self.assertRaisesRegex(
            AuthenticationError,
            "No API key provided",
        ):
            fireworks.client.api_key = ""

            fireworks.client.Completion.create(
                model=MODEL,
                prompt=PROMPT,
                max_tokens=MAX_TOKENS,
            )

        with self.assertRaisesRegex(
            AuthenticationError,
            "Invalid ApiKey",
        ):
            fireworks.client.api_key = "my-key"

            fireworks.client.Completion.create(
                model=MODEL,
                prompt=PROMPT,
                max_tokens=MAX_TOKENS,
            )


if __name__ == "__main__":
    unittest.main()
