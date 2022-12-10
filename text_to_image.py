import torch
from diffusers import StableDiffusionPipeline
import pandas as pd
from tqdm import tqdm

## Stable Diffusion Pipeline for generating images from text
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",
    guidance_scale=7.5)
pipe = pipe.to("cuda")

## Read the chapter titles from the csv file
df = pd.read_csv("data/chapters.csv", index_col=None)
chapter_titles = list(df['chapter_gist'])

## Set the number of images to generate for each chapter title
num_images = 3

## Generate images for each chapter title
for title in tqdm(chapter_titles):
    prompt = [title] * num_images
    images = pipe(prompt).images
    for i,image in enumerate(images):
        image.save(f"images/{title}_{i}.png")

