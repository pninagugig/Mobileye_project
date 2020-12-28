import glob
import json
from tkinter import Image

import numpy as np
import matplotlib.pyplot as plt
from Scripts.publish import args

from level4.CandidateData import CandidateData
from level4.FilterTfl import FilterTfl
from level4.FindCandidate import FindCandidate
from level4.FindDistance import FindDistance


class TflManager:
    def __init__(self):
        self.find_candidate_point = FindCandidate()
        self.filter_tfls = FilterTfl()
        self.find_distance = FindDistance()
        self.prev = None
        self.candidate_data = None

    def run(self, image):
        self.candidate_data = self.find_candidate_point.run(image)
        tfls = self.filter_tfls.run(self.candidate_data)
        if self.prev:
            self.find_distance.run(tfls, self.prev)
        self.prev = image

    def show_image_and_gt(self, image, objs, fig_num=None):
        plt.figure(fig_num).clf()
        plt.imshow(image)
        labels = set()
        if objs is not None:
            for o in objs:
                poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
                plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
                labels.add(o['label'])
            if len(labels) > 1:
                plt.legend()

    def test_find_tfl_lights(self, image_path, json_path=None, fig_num=None):
        image = np.array(Image.open(image_path))
        if json_path is None:
            objects = None
        else:
            gt_data = json.load(open(json_path))
            what = ['traffic light']
            objects = [o for o in gt_data['objects'] if o['label'] in what]
        self.show_image_and_gt(image, objects, fig_num)
        red_x, red_y, green_x, green_y = self.find_candidate_point.run(image)
        plt.plot(red_x, red_y, 'ro', color='r', markersize=4)
        plt.plot(green_x, green_y, 'ro', color='g', markersize=4)

    def aaa(self):
        flist = glob.glob(np.os.path.join(args.dir, '*_leftImg8bit.png'))
        for image in flist:
            json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
            if not np.os.path.exists(json_fn):
                json_fn = None
            self.test_find_tfl_lights(image, json_fn)
