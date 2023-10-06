import fireworks.client
import os
import httpx
import unittest


fireworks.client.api_key = os.environ.get("API_KEY")
fireworks.client.account = os.environ.get("TEST_ACCOUNT") or "fireworks"
fireworks.client.base_url = (
    os.environ.get("FIREWORKS_BASE_URL") or "https://api.fireworks.ai/inference/v1/"
)


class TestApiE2E(unittest.TestCase):
    def _completion_api_test(self, model_name: str):
        completion = fireworks.client.Completion.create(
            model=model_name,
            prompt="Say this is a test",
        )
        if not completion.choices[0].text:
            raise ValueError(model_name, "The response text is empty.")

    def test_all_models(self):
        failed_models = []
        for model in fireworks.client.Model.list().data:
            if "fireworks" in model.id:
                print("Testing", model.id, "...")
                try:
                    self._completion_api_test(model.id)
                except Exception as e:
                    print(f"Model {model.id} test failed: {e}")
                    failed_models.append(model.id)
        if failed_models:
            raise ValueError(f"Models {failed_models} failed")

        # also test the image models
        url = f"{fireworks.client.base_url}image_generation/stable_diffusion"
        headers = {
            "Content-Type": "application/json",
            "Accept": "image/png",
            "Authorization": f"Bearer {fireworks.client.api_key}",
        }

        model = f"accounts/fireworks/{fireworks.client.account}/stable-diffusion-xl-1024-v1-0"
        data = {
            "cfg_scale": 7,
            "model": model,
            "clip_guidance_preset": "NONE",
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 25,
            "seed": 0,
            "sampler": None,
            "style_preset": None,
            "text_prompts": [{"text": "", "weight": 1}],
        }
        print("show request", headers, data)

        # Using httpx to send a POST request
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)

        # Manually raise an error if the response status code is not 200
        if response.status_code != 200:
            raise httpx.HTTPStatusError(
                f"Unexpected HTTP status: {response.status_code}", response
            )

        # Write the response to output.png
        with open("/tmp/output.png", "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    unittest.main()
