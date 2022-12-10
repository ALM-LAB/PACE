import glob
from PIL import Image

def make_gif(frame_folder):
    folders = glob.glob(f"{frame_folder}/*")
    for folder in folders:
        frames = [Image.open(image) for image in glob.glob(f"{folder}/*.png")]
        frame_one = frames[0]
        frame_one.save(f"{folder}/chapter.gif", format="GIF", append_images=frames,
                save_all=True, duration=700, loop=0)
    
if __name__ == "__main__":
    make_gif("./images")