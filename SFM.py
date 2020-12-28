import numpy as np


def calc_TFL_dist(prev_container, curr_container, focal, pp):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    if abs(tZ) < 10e-6:
        print('tz = ', tZ)
    elif norm_prev_pts.size == 0:
        print('no prev points')
    elif norm_prev_pts.size == 0:
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(
            norm_prev_pts, norm_curr_pts, R, foe, tZ)
    return curr_container


def prepare_3D_data(prev_container, curr_container, focal, pp):
    norm_prev_pts = normalize(prev_container.traffic_light, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light, focal, pp)
    R, foe, tZ = decompose(np.array(curr_container.EM))
    return norm_prev_pts, norm_curr_pts, R, foe, tZ


def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec


def normalize(pts, focal, pp):
    return np.array([np.array([p[0] - pp[0], p[1] - pp[1], focal]) / focal for p in pts])


def unnormalize(pts, focal, pp):
    return np.array([[(p[0] * focal) + pp[0], (p[1] * focal) + pp[1], focal] for p in pts])


def decompose(EM):
    T = EM[:3, 3]
    return EM[:3, :3], [T[0] / T[2], T[1] / T[2]], T[2]


def rotate(pts, R):
    return np.array([(R @ p) for p in pts])


def find_corresponding_points(p, norm_pts_rot, foe):
    m = ((foe[1] - p[1]) / (foe[0] - p[0]))
    n = ((p[1] * foe[0]) - (foe[1] * p[0])) / (foe[0] - p[0])
    d = [abs((m * point[0] + n - point[1]) / ((m ** 2) + 1) ** 0.5) for point in norm_pts_rot]
    return np.argmin(d), norm_pts_rot[np.argmin(d)]


def calc_dist(p_curr, p_rot, foe, tZ):
    dist_x = (tZ * (foe[0] - p_rot[0])) / (p_curr[0] - p_rot[0])
    dist_y = (tZ * (foe[1] - p_rot[1])) / (p_curr[1] - p_rot[1])
    return np.average([dist_x, dist_y], weights=[abs(p_rot[0] - p_curr[0]), abs(p_rot[1] - p_curr[1])])
