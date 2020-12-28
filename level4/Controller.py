from TflManager import TflManager
from FrameData import FrameData

class Controller:
    def __init__(self, pls_path):
        file_ = open(pls_path)
        self.clip = file_.read().split("\n")[1:]
        self.frame_data = FrameData(file_.read().split("\n")[0]) #TODO implement Data class
        self.tfl_manager = TflManager() # TODO just use
        self.prev = None

    def run_all(self): #TODO has to run the functions of tfl_manager
        for img_path in self.clip:
            candidates = self.tfl_manager.find_candidate_point.run(img_path)
            tfls = self.tfl_manager.filter_tfls.run(candidates)
            if self.prev:
                self.tfl_manager.find_distance.run(tfls , self.prev)
                self.prev = img_path
