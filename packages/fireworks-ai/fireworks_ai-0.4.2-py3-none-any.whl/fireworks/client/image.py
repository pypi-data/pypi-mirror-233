# Copyright (c) Stability AI Ltd, All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

from typing import Generator, List, Optional, Sequence, Union
import httpx
import os
import warnings
from pydantic import BaseModel, Field
import urllib.parse as urlparse

try:
    from PIL import Image
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
except ImportError as e:
    raise ImportError(
        "Please install fireworks-ai[stability] to use the image generation client."
    ) from e

# TODO: share this with backend
class Prompt(BaseModel):
    text : str
    weight : float


# TODO: share this with backend
class ImageGenerationRequest(BaseModel):
    cfg_scale: int = Field(7)
    clip_guidance_preset: str = Field("NONE")
    height: int = Field(1024)
    width: int = Field(1024)
    samples: int = Field(1)
    steps: int = Field(50)
    seed: int = Field(0)
    style_preset: Optional[str] = Field(None, nullable=True)
    text_prompts: list[Prompt]


class _ImageInference:
    def __init__(
        self,
        host: str = "http://sdxl-test.default.default.aws-knative.inference.fireworks.ai",
        key: str = "",
        engine: str = "stable-diffusion-xl-1024-v1-0",
        upscale_engine: str = "esrgan-v1-x2plus",
        verbose: bool = False,
        wait_for_ready: bool = True,
    ):
        self.host = host
        # TODO: Unify with `fireworks.client.base_url` somehow
        if self.host == "":
            self.host = os.environ.get("STABILITY_HOST", "")
        if self.host == "":
            raise ValueError("Please specify a host for the image generation client.")

        self.key = key

        # TODO: enable and pass as header
        import fireworks.client
        if self.key == "" and fireworks.client.api_key is not None:
            self.key = fireworks.client.api_key
        if self.key == "":
            self.key = os.environ.get("STABILITY_KEY", "")


        self.verbose = verbose
        self.engine = engine
        self.upscale_engine = upscale_engine

        # FIXME: there's gotta be a better way to convert a string name to
        # a protobuf enum value...
        self._finish_reasons_dict = dict(generation.FinishReason.items())

    def generate(
        self,
        prompt: Union[str, List[str], generation.Prompt, List[generation.Prompt]],
        init_image: Optional[Image.Image] = None,
        mask_image: Optional[Image.Image] = None,
        height: int = 1024,
        width: int = 1024,
        start_schedule: float = 1.0,
        end_schedule: float = 0.01,
        cfg_scale: float = 7.0,
        sampler: generation.DiffusionSampler = None,
        steps: int = 50,
        seed: Union[Sequence[int], int] = 0,
        samples: int = 1,
        safety: bool = True,
        classifiers: Optional[generation.ClassifierParameters] = None,
        guidance_preset: generation.GuidancePreset = "NONE",  # FIXME: use proto
        guidance_cuts: int = 0,
        guidance_strength: Optional[float] = None,
        guidance_prompt: Union[str, generation.Prompt] = None,
        guidance_models: List[str] = None,
        adapter_type: generation.T2IAdapter = None,
        adapter_strength: float = 0.4,
        adapter_init_type: generation.T2IAdapterInit = generation.T2IAdapterInit.T2IADAPTERINIT_IMAGE,
        style_preset: Optional[str] = None
    ) -> Generator[generation.Answer, None, None]:
        if init_image is not None:
            raise NotImplementedError("init_image is not supported yet.")

        if mask_image is not None:
            raise NotImplementedError("mask_image is not supported yet.")

        if start_schedule != 1.0 or end_schedule != 0.01:
            warnings.warn("start_schedule and end_schedule are being ignored")
            start_schedule, end_schedule = 1.0, 0.01

        if not safety:
            warnings.warn("safety is being ignored")
            safety = True

        if classifiers is not None:
            raise NotImplementedError("classifiers are not supported yet.")

        if guidance_cuts != 0:
            warnings.warn("guidance_cuts is being ignored")
            guidance_cuts = 0

        if guidance_strength is not None:
            warnings.warn("guidance_strength is being ignored")
            guidance_strength = None

        if guidance_prompt is not None:
            warnings.warn("guidance_prompt is being ignored")
            guidance_prompt = None

        if guidance_models is not None:
            warnings.warn("guidance_models is being ignored")
            guidance_models = None

        if adapter_type is not None:
            warnings.warn("adapter_type is being ignored")
            adapter_type = None

        if adapter_strength != 0.4:
            warnings.warn("adapter_strength is being ignored")
            adapter_strength = 0.4

        if adapter_init_type != generation.T2IAdapterInit.T2IADAPTERINIT_IMAGE:
            warnings.warn("adapter_init_type is being ignored")
            adapter_init_type = generation.T2IAdapterInit.T2IADAPTERINIT_IMAGE

        if (prompt is None) and (init_image is None):
            raise ValueError("prompt or init_image must be specified")

        prompts: List[generation.Prompt] = []
        if isinstance(prompt, (str, generation.Prompt)):
            prompt = [prompt]
        for p in prompt:
            if isinstance(p, str):
                p = Prompt(text=p, weight=1)
            elif isinstance(p, generation.Prompt):
                weight = p.parameters.weight if p.parameters else 1.0
                assert p.text is not None
                p = Prompt(text=p.text, weight=weight)
            else:
                raise TypeError("prompt must be a string or generation.Prompt object")
            prompts.append(p)

        return self._execute_request(
            prompts=prompts,
            init_image=init_image,
            mask_image=mask_image,
            height=height,
            width=width,
            start_schedule=start_schedule,
            end_schedule=end_schedule,
            cfg_scale=cfg_scale,
            sampler=sampler,
            steps=steps,
            seed=seed,
            samples=samples,
            safety=safety,
            classifiers=classifiers,
            guidance_preset=guidance_preset,
            guidance_cuts=guidance_cuts,
            guidance_strength=guidance_strength,
            guidance_prompt=guidance_prompt,
            guidance_models=guidance_models,
            adapter_type=adapter_type,
            adapter_strength=adapter_strength,
            style_preset=style_preset,
        )


class _ImageRESTImpl(_ImageInference):
    def __init__(
        self,
        host: str = "http://sdxl-test.default.default.aws-knative.inference.fireworks.ai",
        key: str = "",
        engine: str = "stable-diffusion-xl-1024-v1-0",
        upscale_engine: str = "esrgan-v1-x2plus",
        verbose: bool = False,
        wait_for_ready: bool = True,
    ):
        super().__init__(
            host=host,
            key=key,
            engine=engine,
            upscale_engine=upscale_engine,
            verbose=verbose,
            wait_for_ready=wait_for_ready,
        )

        self.client = httpx.Client()

    def _execute_request(
            self,
            prompts: List[generation.Prompt],
            init_image: Optional[Image.Image] = None,
            mask_image: Optional[Image.Image] = None,
            height: int = 1024,
            width: int = 1024,
            start_schedule: float = 1.0,
            end_schedule: float = 0.01,
            cfg_scale: float = 7.0,
            sampler: generation.DiffusionSampler = None,
            steps: int = 50,
            seed: Union[Sequence[int], int] = 0,
            samples: int = 1,
            safety: bool = True,
            classifiers: Optional[generation.ClassifierParameters] = None,
            guidance_preset: generation.GuidancePreset = "NONE",  # FIXME: use proto
            guidance_cuts: int = 0,
            guidance_strength: Optional[float] = None,
            guidance_prompt: Union[str, generation.Prompt] = None,
            guidance_models: List[str] = None,
            adapter_type: generation.T2IAdapter = None,
            adapter_strength: float = 0.4,
            adapter_init_type: generation.T2IAdapterInit = generation.T2IAdapterInit.T2IADAPTERINIT_IMAGE,
            style_preset: Optional[str] = None
    ) -> generation.Answer:
        request_body = ImageGenerationRequest(
            cfg_scale=cfg_scale,
            clip_guidance_preset=guidance_preset,
            height=height,
            width=width,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            text_prompts=prompts,
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "image/png",
        }

        payload_dict = request_body.dict()
        uri = urlparse.urljoin(self.host, f"/v1/generation/{self.engine}/text-to-image")
        response = self.client.post(uri, headers=headers, json=payload_dict)
        if response.status_code == 200:
            finish_reason : generation.FinishReason = self._finish_reasons_dict[response.headers.get("Finish-Reason", "STOP")]
            answer =  generation.Answer(
                answer_id="",  # TODO: populate
                request_id="", # TODO: populate
                received=0, # TODO: populate
                created=0, # TODO: populate
                meta=None, # TODO: populate
                artifacts=[generation.Artifact(
                    id=0, # TODO: populate
                    type=generation.ArtifactType.ARTIFACT_IMAGE,
                    mime="image/png", # Does the stability SDK support json return?
                    magic="PNG",
                    index=0,
                    finish_reason=finish_reason,  # TODO: stricter dict lookup once backend is updated
                    seed=int(response.headers.get("Seed", 0)),  # TODO: stricter dict lookup once backend is updated
                    uuid="",  # TODO: populate
                    size=int(response.headers.get("Content-Length", len(response.content))),  # TODO: stricter dict lookup once backend is updated
                )]
            )
            answer.artifacts[0].binary = response.content
            return answer
        else:
            return f"Failed to generate image: {response.status_code}, {response.text}"


# TODO: switch to GRPC backend when it exists
class ImageInference(_ImageRESTImpl):
    pass
