import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


class Diffusadle:
    def __init__(self):
        model_id = "CompVis/stable-diffusion-v1-4"
        device = "cuda"

        # slow
        # self.pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True)

        # fast
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True)

        self.pipe = self.pipe.to(device)

    @autocast("cuda")
    def diffuse(self, prompt: str):
        image = self.pipe(prompt, guidance_scale=7.5).images[0]

        # to colab
        # display(image)

        # not to colab
        image.save(f"{prompt}.png")


d = Diffusadle()
d.diffuse("big world dancers")
