from FindCandidate import FindCandidate
from FindDistance import FindDistance
from FindTfld import FindTfld


class TflManager:
    def __init__(self):
        self.find_candidate_point = FindCandidate()
        self.filter_tfls = FindTfld()
        self.find_distance = FindDistance()


