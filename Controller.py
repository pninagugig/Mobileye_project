from level4.FrameData import FrameData
from level4.TflManager import TflManager


class Controller:
    def __init__(self, pls_path):
        file_ = open(pls_path)
        list_ = file_.read().split("\n")[:]
        self.clip = list_[1:]
        self.frame_data = FrameData(list_[0])
        self.tfl_manager = TflManager()

    def run_all(self):
        for img_path in self.clip:
            self.tfl_manager.run(img_path)
        self.tfl_manager.aaa()

