import cv2
import numpy as np
from skimage.morphology import skeletonize, thin
from skimage import io
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

from group_nearby_curve_function import group_nearby_curves
from utils import detect_curves, draw_curve_colored, detect_curves_2


def create_curve_list(image):
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    binary_image = 255 - binary_image
    binary_image = binary_image > 128
    skeleton = skeletonize(binary_image)
    conv_filter = np.array([[1, 1, 1],
                            [1, 10, 1],
                            [1, 1, 1]])
    filtered_skeleton = convolve(skeleton.astype(int), conv_filter)
    junction_points = (filtered_skeleton > 12).astype(int)
    endpoints = (filtered_skeleton == 11).astype(int)
    junction_points_removed = skeleton - junction_points

    curves_junctions_removed = detect_curves(junction_points_removed)
    colored_curve_junctions_removed, _ = draw_curve_colored(curves_junctions_removed, junction_points_removed)

    def is_consist_endpoint(curve, endpoint_cords_list):
        for curve_cord in curve:
            if curve_cord in endpoint_cords_list:
                return True
        return False

    x_coordinates, y_coordinates = np.where(endpoints == 1)
    endpoint_cords_list = list(zip(x_coordinates, y_coordinates))
    curves_removed_cons_endpoints = []
    for curve in curves_junctions_removed:
        if not is_consist_endpoint(curve, endpoint_cords_list):
            curves_removed_cons_endpoints.append(curve)
        elif len(curve) > 20:
            curves_removed_cons_endpoints.append(curve)

    colored_curves_removed_cons_endpoints, skeleton_removed_ends = draw_curve_colored(curves_removed_cons_endpoints,
                                                                                      junction_points_removed)

    skeleton_removed_end_curves = skeleton_removed_ends + junction_points
    curves_end_removed = detect_curves_2(skeleton_removed_end_curves)


    curves_grouped = group_nearby_curves(curves_end_removed)

    return curves_grouped



