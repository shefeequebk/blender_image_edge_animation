import math
import random

import bpy
import numpy as np
from scipy.ndimage import convolve
from skimage.morphology import skeletonize


# from matplotlib import pyplot as plt


def detect_curves(skeleton):
    # Extract curves
    def get_neighbors(pixel, image):
        x, y = pixel
        neighbors = [(x + i, y + j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
        return [neighbor for neighbor in neighbors
                if 0 <= neighbor[0] < image.shape[0] and 0 <= neighbor[1] < image.shape[1]
                and image[neighbor] == 1]

    def dfs(pixel, image, visited):
        stack = [pixel]
        curve = [pixel]
        while stack:
            pixel = stack.pop()
            neighbors = get_neighbors(pixel, image)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    curve.append(neighbor)
        return curve

    visited = set()
    raw_curves = []
    for i in range(skeleton.shape[0]):
        for j in range(skeleton.shape[1]):
            if skeleton[i, j] == 1 and (i, j) not in visited:
                curve = dfs((i, j), skeleton, visited)
                curve = list(set(curve))  # ADDED
                raw_curves.append(curve)
    return raw_curves


def draw_curve_colored(curves, skeleton):
    # Create a color image
    color_image = np.zeros((skeleton.shape[0], skeleton.shape[1], 3), dtype=np.uint8)
    binary_image = np.full((skeleton.shape[0], skeleton.shape[1]), False, dtype=bool)

    # Assign a unique color to each curve
    # colors = plt.cm.hsv(np.linspace(0, 1, len(curves))).tolist()  # hsv color map covers a wide range of colors
    import random

    def generate_random_rgb():
        r = random.randint(150, 255)
        g = random.randint(150, 255)
        b = random.randint(150, 255)
        return r, g, b

    # Use the function
    # rgb_color = generate_random_rgb()
    # print(rgb_color)
    for curve in curves:
        rgb_color = generate_random_rgb()
        # print(rgb_color,curve)
        for x, y in curve:
            # color_image[x, y] = [int(c * 255) for c in
            #                      color[:3]]  # convert color from float in range [0, 1] to int in range [0, 255]
            color_image[x, y] = rgb_color  # convert color from float in range [0, 1] to int in range [0, 255]
            binary_image[x, y] = True
    return color_image, binary_image


def split_curve_jumps(raw_curves):
    curves = []
    for raw_curve in raw_curves:
        curve = [raw_curve[0]]
        for i in range(1, len(raw_curve)):
            if np.sqrt((raw_curve[i][0] - raw_curve[i - 1][0]) ** 2 +
                       (raw_curve[i][1] - raw_curve[i - 1][1]) ** 2) > np.sqrt(2):
                # Jump detected, start a new curve
                curves.append(curve)
                curve = []
            curve.append(raw_curve[i])
        curves.append(curve)
    return curves


def detect_curves_2(binary_image):
    # Normalize the image, to keep skimage happy
    # binary_image = binary_image > 128

    # Perform the operation
    # skeleton = skeletonize(binary_image)
    skeleton = binary_image

    # find the junctions and endpoints
    conv_filter = np.array([[1, 1, 1],
                            [1, 10, 1],
                            [1, 1, 1]])
    filtered_skeleton = convolve(skeleton.astype(int), conv_filter)
    # junctions = ((filtered_skeleton > 11) & (filtered_skeleton < 14)).astype(int)
    junctions = ((filtered_skeleton > 12)).astype(int)
    endpoints = (filtered_skeleton == 11).astype(int)

    # Extract curves
    def get_neighbors(pixel, image):
        x, y = pixel
        neighbors = [(x + i, y + j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
        return [neighbor for neighbor in neighbors
                if 0 <= neighbor[0] < image.shape[0] and 0 <= neighbor[1] < image.shape[1]
                and image[neighbor] == 1]

    def dfs(pixel, image, visited):
        stack = [pixel]
        curve = [pixel]
        while stack:
            pixel = stack.pop()
            neighbors = get_neighbors(pixel, image)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    curve.append(neighbor)
        return curve

    visited = set()
    raw_curves = []
    for i in range(skeleton.shape[0]):
        for j in range(skeleton.shape[1]):
            if skeleton[i, j] == 1 and (i, j) not in visited:
                curve = dfs((i, j), skeleton, visited)
                raw_curves.append(curve)

    # Split curves at jumps
    curves = []
    for raw_curve in raw_curves:
        curve = [raw_curve[0]]
        for i in range(1, len(raw_curve)):
            if np.sqrt((raw_curve[i][0] - raw_curve[i - 1][0]) ** 2 +
                       (raw_curve[i][1] - raw_curve[i - 1][1]) ** 2) > np.sqrt(2):
                # Jump detected, start a new curve
                curves.append(curve)
                curve = []
            curve.append(raw_curve[i])
        curves.append(curve)

    return curves


def generate_random_rgb():
    r = random.randint(50, 255)
    g = random.randint(50, 255)
    b = random.randint(50, 255)
    return r, g, b


def set_render_camera(img_shape):
    # select all objects
    bpy.ops.object.select_all(action='SELECT')

    # delete all selected objects
    bpy.ops.object.delete()

    # Create two coordinates on xy plane
    coord1 = (0, 0, 2)
    coord2 = (img_shape[0] / 10, img_shape[1] / 10, 2)

    # ## Add two points in the scene
    # bpy.ops.mesh.primitive_uv_sphere_add(location=coord1, radius=0.1)
    # bpy.ops.mesh.primitive_uv_sphere_add(location=coord2, radius=0.1)

    # Calculate midpoint
    midpoint = ((coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2, 0)

    # Calculate distance (this will be the diagonal of the image)
    dist = math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    # Set the resolution of the render output
    bpy.context.scene.render.resolution_y = int(coord2[0] * 10)
    bpy.context.scene.render.resolution_x = int(coord2[1] * 10)

    # Add a camera to the scene
    bpy.ops.object.camera_add(location=midpoint)

    # Set the camera to the active camera
    bpy.context.scene.camera = bpy.context.object

    # Now, let's adjust the camera's location and rotation to ensure the two points are in its field of view
    # This is based on Pythagorean theorem and trigonometry
    height = dist / (2 * math.tan(bpy.context.object.data.angle / 2))

    # Move camera to its correct position
    bpy.context.object.location.z += height

    bpy.context.object.rotation_euler.z = math.pi / 2


def clear_blender_scene():
    # select all objects
    bpy.ops.object.select_all(action='SELECT')

    # delete all selected objects
    bpy.ops.object.delete()


def set_render_settings(rend_details):

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value =\
        (*rend_details['background_color'], 1)

    bpy.data.scenes[0].render.engine = "CYCLES"

    # Set the device_type
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"  # or "OPENCL"

    # Set the device and feature set
    bpy.context.scene.cycles.device = "GPU"

    # get_devices() to let Blender detects GPU device
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1  # Using all devices, include GPU and CPU
        print(d["name"], d["use"])
    bpy.context.preferences.system.memory_cache_limit = 4000

    # Set the render engine
    bpy.context.scene.render.engine = rend_details['Render Engine']

    # Set the output path to a specific folder
    bpy.context.scene.render.filepath = rend_details["Output Path"]

    # Set the resolution percentage
    bpy.context.scene.render.resolution_percentage = rend_details["Resolution"]["Percentage"]

    # Enable denoising and set the denoise settings
    bpy.context.scene.cycles.use_denoising = True
    # Set the max samples
    bpy.context.scene.cycles.samples = rend_details["Samples"]

    # Set the output format to FFmpeg
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

    # Set the output video codec to lossless
    bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOSSLESS'

    bpy.context.scene.cycles.device = 'GPU'


import cv2


def resize_image_by_scale(image, scale):
    # Calculate the new dimensions based on the scale factor
    new_width = int(image.shape[1] * scale)
    new_height = int(image.shape[0] * scale)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


def set_bloom_settings(bloom_settings):
    # Select the scene
    scene = bpy.context.scene

    # Set the bloom settings using the dictionary
    scene.eevee.use_bloom = bloom_settings["use_bloom"]
    scene.eevee.bloom_threshold = bloom_settings["bloom_threshold"]
    scene.eevee.bloom_knee = bloom_settings["bloom_knee"]
    scene.eevee.bloom_intensity = bloom_settings["bloom_intensity"]
    scene.eevee.bloom_radius = bloom_settings["bloom_radius"]
    scene.eevee.bloom_color = bloom_settings["bloom_color"]
