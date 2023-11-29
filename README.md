# Blender Image Edge Animation - Create animations from images

Check out this working video for more information:
[![Blender Image Edge Animation - Create animations from images](https://img.youtube.com/vi/cjNpCEW_dEs/0.jpg)](https://www.youtube.com/watch?v=cjNpCEW_dEs)

## Setup Instructions
### Installing Required Packages 

Execute the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Running the Application 

Run the main Python script via the following command: 

```bash
python main.py
```
Follow these steps in the GUI:

1. Select an image file when the "Select an image" window appears.
2. Specify the output video directory in the "Select output video directory" window.

## Understanding the Configuration Settings - in main.py file


### Render Settings 

You can customize the rendering of your image through the following settings:

```python
render_settings = {
    "Render Engine": 'BLENDER_EEVEE',
    "Output Path": output_video_path,
    "background_color": (0, 0, 0),
    "Resolution": {"Percentage": 100},
    "Samples": 16,
    "Memory cache limit": 1024 * 8
}
```

The `render_settings` dictionary has the following parameters:

1. `Render Engine`: Sets the render engine to be used by Blender. The available options are 'BLENDER_EEVEE' and 'CYCLES'. Eevee is a real-time render engine, while Cycles is a ray tracing render engine. 'BLENDER_EEVEE' generally provides a faster and better result in this case.

2. `Output Path`: Defines the file path where the final animation will be saved.

3. `background_color`: Sets the background color of the rendered animation. The color is represented as an RGB triplet where each component ranges from 0.0 to 1.0.

4. `Resolution`: This dictionary specifies the resolution scale relative to the base resolution of the image. A `Percentage` value of 100 denotes full resolution (equivalent to the input image resolution), whereas a value of 200 signifies double resolution, and so on.

5. `Samples`: Dictates the number of samples to be used in the rendering process. Higher values improve the quality of the render but also extend the rendering time. This parameter is effective when using the Cycles engine.

6. `Memory cache limit`: Indicates the memory cache limit (in megabytes) during the rendering process. This feature aids in accelerating render times by storing frequently used data, but a higher limit may result in Blender consuming all available system memory.


### Bloom Settings 

Bloom settings are used to create a glowing effect for curves. These settings apply only when using the 'BLENDER_EEVEE' render engine.

```python
bloom_settings = {
    "use_bloom": True,
    "bloom_threshold": 0.8,
    "bloom_knee": 0.5,
    "bloom_intensity": 0.8,
    "bloom_radius": 1,
    "bloom_color": (1.0, 1.0, 1.0)
}
```

The `bloom_settings` dictionary is composed of the following parameters:

1. `use_bloom`: A boolean flag that decides whether the Bloom effect is activated (`True`) or deactivated (`False`).

2. `bloom_threshold`: This value establishes the minimum intensity for a pixel to be considered for the Bloom effect. Higher values signify that fewer pixels qualify for the Bloom effect, i.e., only brighter regions of the image will contribute to the effect.

3. `bloom_knee`: Affects the transition smoothness between bloomed and non-bloomed areas. Lower values result in a more distinct transition.

4. `bloom_intensity`: Determines the strength of the Bloom effect. Higher values amplify the effect.

5. `bloom_radius`: Dictates the size of the Bloom effect on eligible pixels. Larger values produce a more significant Bloom effect.

6. `bloom_color`: Defines the color of the Bloom effect using an RGB triplet. For instance, (1.0, 0.0, 0.0) is red, while (0.0, 0.0, 1.0) is blue.

Please note that Bloom settings are exclusive to the Eevee rendering engine in Blender and may not apply or may behave differently with other rendering engines like Cycles.

### Curve Color Settings 

You can customize the color settings of the curves as follows:

```python
curves_color = {
    'random_color': True,
    'color': (1.0, 0.0, 0.0)
}
```

This dictionary includes the following parameters:

1. `random_color`: A boolean flag that decides whether the color of the curve will be randomly selected (`True`) or fixed (`False`).

2. `color`: Specifies the color of the curve, represented as an RGB triplet, when `random_color` is set to `False`. For instance, (1.0, 0.0, 0.0) is red, while (0.0, 0.0, 1.0) is blue.
