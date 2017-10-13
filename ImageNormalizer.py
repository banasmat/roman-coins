import os, sys
from PIL import Image
import json
from pprint import pprint

class ImageNormalizer():

    base_file_dir = 'nomismaspider/output/'
    i = 0

    def parse_nomisma_output(self):

        with open('nomismaspider-output.json') as data_file:
            data = json.load(data_file)

            for entry in data:
                files_data = entry['files']
                file_paths = []

                for file_data in files_data:
                    file_paths.append(self.base_file_dir + file_data['path'])

                self.normalize_images(file_paths, entry)

    def normalize_images(self, files, data_entry):

        images = map(Image.open, files)
        widths, heights = zip(*(i.size for i in images))

        # total_width = sum(widths)
        # max_height = max(heights)
        max_width = 750
        max_height = 400

        new_im = Image.new('RGB', (max_width, max_height), 'white')

        is_image_merged = len(images) == 2
        max_width_divisor = 1
        if is_image_merged:
            max_width_divisor = 2

        x_offset = 0

        for im in images:
            im_height = im.size[1]
            if im_height <= max_height:
                y_offset = (max_height - im_height) / 2
            else:
                raise ValueError('Image height ' + im_height + 'is higher than max')

            im_width = im.size[0]
            if im_width <= max_width:
                x_offset += ((max_width / max_width_divisor) - im_width) / 2
            else:
                raise ValueError('Image width ' + im_width + 'is higher than max')

            new_im.paste(im, (x_offset, y_offset))

            x_offset = max_width / max_width_divisor

        self.i += 1

        target_dir = 'normalized-images/' + data_entry['authority']
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir, 0o777)

        new_im.save(target_dir + '/' + str(self.i) + '.jpg')

normalizer = ImageNormalizer()
normalizer.parse_nomisma_output()