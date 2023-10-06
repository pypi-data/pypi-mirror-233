from PIL import Image
from PIL import ImageOps
import argparse
import os

PADDING = 10


def process_file(filePath):
    image=Image.open(filePath)

    image.load()

    # remove alpha channel
    invert_im = image.convert("RGB") 

    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()

    a= imageBox[0]-PADDING
    b= imageBox[1]-PADDING
    c= imageBox[2]+PADDING
    d= imageBox[3]+PADDING

    cropped=image.crop((a,b,c,d))

    # Calculate the scaling factor
    scale_factor = min(1024/cropped.width, 768/cropped.height)

    # Resize the image
    cropped = cropped.resize((int(cropped.width * scale_factor), int(cropped.height * scale_factor)))


    # Paste cropped image to backgroung
    background = Image.new('RGB', (1024, 768), (255, 255, 255))

    offset = ((background.width - cropped.width) // 2, (background.height - cropped.height) // 2)
    background.paste(cropped, offset)

    return background




def main():
    parser = argparse.ArgumentParser(description="Crops unnecessary white background from images in specified directory.")
    parser.add_argument("directory", type=str, help="Path to the directory containing pngs")

    args = parser.parse_args()

    if os.path.isdir(args.directory):
        for single_file_name in os.listdir(args.directory):
            single_file_path = os.path.join(args.directory, single_file_name)
            print(single_file_path)

            # Check if it's a file and not a subdirectory
            if os.path.isfile(single_file_path):
                # process_file(single_file_path)
                try:
                    process_file(single_file_path)
                except Exception as ex:
                    print(ex)


    else:
        print(f"'{args.directory}' is not a valid directory!")
        exit(1)

    
if __name__ == "__main__":
    main()




