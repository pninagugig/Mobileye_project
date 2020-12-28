class CandidateData:
    def __init__(self, x_red, y_red, x_green, y_green):
        self.m_coordinates = []
        self.m_auxiliary = []
        for x, y in zip(x_red, y_red):
            self.m_coordinates.append([x, y])
            self.m_auxiliary.append(0)

        for x, y in zip(x_green, y_green):
            self.m_coordinates.append([x, y])
            self.m_auxiliary.append(1)
