import os
import bpy
import cv2
from create_curve_list import create_curve_list
from utils import clear_blender_scene, set_render_camera, set_render_settings, resize_image_by_scale, \
    set_bloom_settings
from curve_list_to_blend_anim import curve_list_to_animation

image_path = 'path/to/image/file'
output_video_path = 'path/to/video/output'
blender_settings = {
    "render_settings": {
        "Render Engine": 'BLENDER_EEVEE',  # 'BLENDER_EEVEE'  # OR 'CYCLES'
        "Output Path": output_video_path,
        "background_color": (0, 0, 0),
        "Resolution": {"Percentage": 100},
        "Samples": 16,
        "Memory cache limit": 1024 * 8
    },
    "bloom_settings": {
        "use_bloom": True,
        "bloom_threshold": 0.8,
        "bloom_knee": 0.5,
        "bloom_intensity": 0.8,
        "bloom_radius": 1,
        "bloom_color": (1.0, 1.0, 1.0)  # Red color
    },
    "curves_color": {
        'random_color': True,
        'color': (1.0, 0.0, 0.0)
    }}


if __name__ == '__main__':
    clear_blender_scene()
    image = cv2.imread(image_path, 0)
    scale = 1024 / image.shape[0]
    image = resize_image_by_scale(image, scale)
    curve_list = create_curve_list(image)
    set_render_camera(image.shape)
    curve_list_to_animation(curve_list, blender_settings["curves_color"])
    set_bloom_settings(blender_settings["bloom_settings"])
    set_render_settings(blender_settings["render_settings"])
    bpy.ops.render.render(animation=True)
    current_script_path = os.path.dirname(os.path.realpath(__file__))
    blend_file_save_folder = f'{current_script_path}/blender_file'
    if not os.path.exists(blend_file_save_folder):
        os.makedirs(blend_file_save_folder)
    bpy.ops.wm.save_mainfile(filepath=f'{blend_file_save_folder}/out_blend_file.blend')


