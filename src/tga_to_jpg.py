import argparse
import os
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser(description='Transform tga files to jpg')
    parser.add_argument('input_dir', type=str, help='Path of input directory containing tga files')
    parser.add_argument('output_dir', type=str, help='Path of output directory containing jpg files')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    os.makedirs(args.output_dir, exist_ok=True)
    for file in os.listdir(args.input_dir):
        if file.endswith('.tga'):
            im = Image.open(os.path.join(args.input_dir, file))
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(args.output_dir, file[:-4] + '.jpg'))
