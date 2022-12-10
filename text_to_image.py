import torch
import pandas as pd
import os
from tqdm import tqdm

from diffusers import StableDiffusionPipeline

## Stable Diffusion Pipeline for generating images from text
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe = pipe.to("cuda")

## Read the chapter titles from the csv file
df = pd.read_csv("data/df_chapters.csv", index_col=None)
chapter_titles = list(df['chapter_gist'])

## Set the number of images to generate for each chapter title
num_images = 3

## Generate images for each chapter title
for title in tqdm(chapter_titles):
    print(title)
    prompt = [title] * num_images
    images = pipe(prompt).images
    for i,image in enumerate(images):
        if not os.path.exists(f"images/{title}"):
            os.makedirs(f"images/{title}") 
        image.save(f"images/{title}/{i}.png")

