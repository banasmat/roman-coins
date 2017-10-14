import os, sys
from PIL import Image
import json
from pprint import pprint

class ImageNormalizer():

    base_file_dir = 'nomismaspider/output/'
    base_target_dir = 'normalized-images/'
    i = 0

    def parse_nomisma_output(self):

        if not os.path.isdir(self.base_target_dir):
            os.mkdir(self.base_target_dir, 0o777)

        with open('nomismaspider-output.json') as data_file:
            data = json.load(data_file)

            for entry in data:
                files_data = entry['files']
                file_paths = []

                for file_data in files_data:
                    file_paths.append(self.base_file_dir + file_data['path'])

                if(len(file_paths) > 0):
                    self.merge_images(file_paths, entry)

    def merge_images(self, file_paths, data_entry):

        images = map(Image.open, file_paths)
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height), 'white')

        x_offset = 0

        for im in images:
            im_height = im.size[1]
            y_offset = 0
            if im_height < max_height:
                y_offset = (max_height - im_height) / 2

            new_im.paste(im, (x_offset, y_offset))
            x_offset += im.size[0]

        target_dir = self.base_target_dir + data_entry['authority'].replace('/', '_')
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir, 0o777)
            self.i = 0

        self.i += 1

        new_im.save(target_dir + '/' + str(self.i) + '.jpg')

normalizer = ImageNormalizer()
normalizer.parse_nomisma_output()