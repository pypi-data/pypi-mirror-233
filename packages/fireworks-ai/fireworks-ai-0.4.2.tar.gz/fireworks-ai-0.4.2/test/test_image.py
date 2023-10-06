import unittest
from unittest.mock import patch, MagicMock
import fireworks.client.image as image
from fireworks.client.image import ImageInference, ImageGenerationRequest
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings

class TestImageInference(unittest.TestCase):

    @patch('httpx.Client.post')
    def test_generate_success(self, mock_post):
        # Mock the response from the server
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = b'fake_binary_content'
        mock_post.return_value.headers = {
            'Finish-Reason': 'STOP',
            'Seed': '42',
            'Content-Length': '17'
        }

        client = ImageInference()

        prompt = [
            generation.Prompt(
                parameters=generation.PromptParameters(weight=1.0),
                text="A quick brown fox transcending reality",
            ),
            generation.Prompt(
                parameters=generation.PromptParameters(weight=-1.0),
                text="blurry",
            ),
        ]

        response = client.generate(prompt=prompt)


        called_prompt = [
            image.Prompt(
                text="A quick brown fox transcending reality",
                weight=1.0,
            ),
            image.Prompt(
                text="blurry",
                weight=-1.0,
            )
        ]
        # Validate that request was formatted correctly
        mock_post.assert_called_with(
            'http://sdxl-test.default.default.aws-knative.inference.fireworks.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'image/png',
            },
            json=ImageGenerationRequest(
                text_prompts=called_prompt
            ).dict()
        )

        # Validate the response
        self.assertEqual(response.artifacts[0].binary, b'fake_binary_content')
        self.assertEqual(response.artifacts[0].seed, 42)
        self.assertEqual(response.artifacts[0].size, 17)


    @patch('httpx.Client.post')
    def test_init_image_not_supported(self, mock_post):
        client = ImageInference()
        with self.assertRaises(NotImplementedError):
            client.generate(prompt="Hello world", init_image="some_image")


    @patch('httpx.Client.post')
    def test_mask_image_not_supported(self, mock_post):
        client = ImageInference()
        with self.assertRaises(NotImplementedError):
            client.generate(prompt="Hello world", mask_image="some_mask")


    @patch('httpx.Client.post')
    def test_classifiers_not_supported(self, mock_post):
        client = ImageInference()
        with self.assertRaises(NotImplementedError):
            client.generate(prompt="Hello world", classifiers=MagicMock())


    @patch('httpx.Client.post')
    def test_start_schedule_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", start_schedule=0.5)
            self.assertTrue(any("start_schedule and end_schedule are being ignored" in str(warning.message) for warning in w))


    @patch('httpx.Client.post')
    def test_end_schedule_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", end_schedule=0.5)
            self.assertTrue(any("start_schedule and end_schedule are being ignored" in str(warning.message) for warning in w))


    @patch('httpx.Client.post')
    def test_safety_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", safety=False)
            self.assertTrue(any("safety is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_classifiers_ignored(self, mock_post):
        client = ImageInference()
        with self.assertRaises(NotImplementedError):
            client.generate(prompt="Hello world", classifiers=MagicMock())

    @patch('httpx.Client.post')
    def test_guidance_cuts_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", guidance_cuts=1)
            self.assertTrue(any("guidance_cuts is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_guidance_strength_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", guidance_strength=0.5)
            self.assertTrue(any("guidance_strength is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_guidance_prompt_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", guidance_prompt="some_prompt")
            self.assertTrue(any("guidance_prompt is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_guidance_models_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", guidance_models=["model1"])
            self.assertTrue(any("guidance_models is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_adapter_type_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", adapter_type=MagicMock())
            self.assertTrue(any("adapter_type is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_adapter_strength_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", adapter_strength=0.6)
            self.assertTrue(any("adapter_strength is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_adapter_init_type_ignored(self, mock_post):
        client = ImageInference()
        with warnings.catch_warnings(record=True) as w:
            client.generate(prompt="Hello world", adapter_init_type=MagicMock())
            self.assertTrue(any("adapter_init_type is being ignored" in str(warning.message) for warning in w))

    @patch('httpx.Client.post')
    def test_prompt_validation(self, mock_post):
        client = ImageInference()
        with self.assertRaises(ValueError):
            client.generate(prompt=None)

if __name__ == '__main__':
    unittest.main()
