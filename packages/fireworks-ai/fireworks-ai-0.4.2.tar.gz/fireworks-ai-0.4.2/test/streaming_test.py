import fireworks.client
import sys
import os
import asyncio
import time
import unittest
import statistics

MODEL = "accounts/fireworks/models/llama-v2-7b-chat"
PROMPT = "Hello there! What is your favorite city and why?"
MAX_TOKENS = 100
MESSAGE = [{"role": "user", "content": PROMPT}]

fireworks.client.api_key = os.environ.get("API_KEY")


def write_output(text: str):
    """Utility function to write text to stdout."""
    sys.stdout.write(text)
    sys.stdout.flush()


class TestFireworksClient(unittest.TestCase):
    def test_streaming(self):
        time_for_chunks = []
        cur_time = time.time()
        for resp in fireworks.client.Completion.create(
            model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, stream=True
        ):
            new_time = time.time()
            time_for_each_chunk = (new_time - cur_time) * 1000
            time_for_chunks.append(time_for_each_chunk)
            cur_time = new_time
        assert statistics.median(time_for_chunks) > 50

    def test_streaming_chat(self):
        time_for_chunks = []
        cur_time = time.time()
        for resp in fireworks.client.ChatCompletion.create(
            model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS, stream=True
        ):
            new_time = time.time()
            time_for_each_chunk = (new_time - cur_time) * 1000
            time_for_chunks.append(time_for_each_chunk)
            cur_time = new_time
        assert statistics.median(time_for_chunks) > 50

    def test_chat(self):
        resp = fireworks.client.ChatCompletion.create(
            model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS
        )
        write_output(resp.choices[0].message.content or "")
        write_output("\n")

    def test_completion(self):
        resp = fireworks.client.Completion.create(
            model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS
        )
        write_output(resp.choices[0].text)
        write_output("\n")

    def test_async_streaming(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_streaming())

    def test_async_streaming_chat(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_streaming_chat())

    def test_async_chat(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_chat())

    def test_async_completion(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_completion())

    async def _async_streaming(self):
        time_for_chunks = []
        cur_time = time.time()
        async for resp in fireworks.client.Completion.acreate(
            model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS, stream=True
        ):
            new_time = time.time()
            time_for_each_chunk = (new_time - cur_time) * 1000
            time_for_chunks.append(time_for_each_chunk)
            cur_time = new_time
        assert statistics.median(time_for_chunks) > 50

    async def _async_streaming_chat(self):
        time_for_chunks = []
        cur_time = time.time()
        async for resp in fireworks.client.ChatCompletion.acreate(
            model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS, stream=True
        ):
            new_time = time.time()
            time_for_each_chunk = (new_time - cur_time) * 1000
            time_for_chunks.append(time_for_each_chunk)
            cur_time = new_time
        assert statistics.median(time_for_chunks) > 50

    async def _async_chat(self):
        resp = await fireworks.client.ChatCompletion.acreate(
            model=MODEL, messages=MESSAGE, max_tokens=MAX_TOKENS
        )
        write_output(resp.choices[0].message.content or "")
        write_output("\n")

    async def _async_completion(self):
        resp = await fireworks.client.Completion.acreate(
            model=MODEL, prompt=PROMPT, max_tokens=MAX_TOKENS
        )
        write_output(resp.choices[0].text)
        write_output("\n")


if __name__ == "__main__":
    unittest.main()
