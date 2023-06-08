import os
import random

import bpy


def curve_list_to_animation(curves, curves_color):
    scale = 10
    for i, curve in enumerate(curves):
        # Path to the .blend file
        file_path = r"Curve particle.blend"

        # Name of the collection you want to import
        collection_name = "Collection"

        # Check if the file exists
        if os.path.exists(file_path):
            # Load the collection
            bpy.ops.wm.append(directory=file_path + "/Collection/", filename=collection_name)
        else:
            print(f"No .blend file found at {file_path}")
        index_string = str(i + 1).zfill(3)
        curve_name = f"{'BezierCurve'}.{index_string}"
        print(curve_name)

        # Make sure the curve exists in the data
        if curve_name in bpy.data.curves:
            curveData = bpy.data.curves[curve_name]

        curveData.dimensions = '3D'
        ico_obj_name = f"{'Icosphere'}.{index_string}"
        ico_obj = bpy.data.objects.get(ico_obj_name)
        x, y = curve[0]
        z = 0
        x, y, z = x / scale, y / scale, z / scale
        ico_obj.location = (x, y, z)

        material_name = f"{'Smoke Domain Material'}.{index_string}"

        if curves_color['random_color']:
            curve_color = (random.randint(50, 255) / 255, random.randint(50, 255) / 255, random.randint(50, 255) / 255)
        else:
            curve_color = curves_color['color']
        bpy.data.materials[material_name].node_tree.nodes["Emission"].inputs[0].default_value = (*curve_color, 1)

        particle_system = ico_obj.particle_systems[0]
        particle_settings = particle_system.settings

        particle_settings.count = len(curve)
        #    curveData.resolution_u = 2

        # Map coordinates to spline
        #    polyline = curveData.splines.new('BEZIER')
        polyline = curveData.splines[0]
        polyline.bezier_points.add(len(curve) - len(polyline.bezier_points))
        for i, coord in enumerate(curve):
            x, y = coord
            z = 2
            x, y, z = x / scale, y / scale, z / scale
            polyline.bezier_points[i].co = (x, y, z)
            polyline.bezier_points[i].handle_right_type = 'AUTO'
            polyline.bezier_points[i].handle_left_type = 'AUTO'

        def convert_bezier_to_poly(obj):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')

            # Deselect all points
            bpy.ops.curve.select_all(action='DESELECT')

            # Select all points of the curve
            bpy.ops.curve.select_all(action='SELECT')

            # # Convert selected points to poly points
            # bpy.ops.curve.handle_type_set(type='AUTOMATIC')
            bpy.ops.curve.spline_type_set(type='POLY')

            # Switch to Object mode
            bpy.ops.object.mode_set(mode='OBJECT')

        # Replace 'BezierCurve' with the name of your Bezier curve object
        curve_object = bpy.data.objects[curve_name]
        convert_bezier_to_poly(curve_object)

    bpy.ops.ptcache.free_bake_all()
    bpy.ops.ptcache.bake_all(bake=True)
