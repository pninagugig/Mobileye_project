import pickle
import numpy as np
#
# from SFM_standAlone import prev_container, curr_container, prev_frame_id, curr_frame_id


class FrameData:
    def __init__(self, pkl_path):
        print(pkl_path)
        with open(pkl_path, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        self.m_pp = data['principle_point']
        self.m_focal = data['flx']
        # prev_container.traffic_light = np.array(data['points_' + str(prev_frame_id)][0])
        # curr_container.traffic_light = np.array(data['points_' + str(curr_frame_id)][0])
        self.m_EM = np.eye(4) #TODO how to initialize the egomotion
        for i in range(24, 29):
            self.m_EM = np.dot(data['egomotion_' + str(i) + '-' + str(i + 1)], self.m_EM)