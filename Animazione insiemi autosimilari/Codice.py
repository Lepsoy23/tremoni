from math import tau
from manim import *

class ContinuousRotatingCube3D(ThreeDScene):
    def construct(self):
        # Set up the camera for 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Create title
        title = Text("Cube", font_size=36)
        title.move_to([1, 2.9, 0])
        
        # Create the single large cube
        large_cube = Cube(side_length=1.0)
        large_cube.set_fill(BLUE, opacity=0.5)
        large_cube.set_stroke(WHITE, width=1)
        large_cube.move_to([-1, 0.5, 1.5])  # Position below title
        
        # Create eight smaller cubes in a compact 2x2x2 arrangement below the large cube
        small_cubes = VGroup()
        cube_spacing = 0.6  # Reduced spacing between cubes for more compact arrangement
        positions = [
            # Front layer
            [-cube_spacing/2-2 +1.3 , + 0.5, cube_spacing/2 -0.25],    # front left
            [cube_spacing/2-2 +1.3,+0.5, cube_spacing/2 -0.25],     # front right
            [-cube_spacing/2-2 +1.3, +0.5, -cube_spacing/2 -0.25 ],   # back left
            [cube_spacing/2-2 +1.3, +0.5, -cube_spacing/2 -0.25],    # back right
            # Back layer
            [-cube_spacing/2-2 +1.3, 1, cube_spacing/2 -0.25],   # front left
            [cube_spacing/2-2 +1.3 , +1, cube_spacing/2 -0.25],    # front right
            [-cube_spacing/2-2 +1.3, +1, -cube_spacing/2 -0.25],  # back left
            [cube_spacing/2-2 +1.3, +1, -cube_spacing/2 -0.25],   # back right
        ]
        
        for pos in positions:
            small_cube = Cube(side_length=0.4)
            small_cube.set_fill(BLUE, opacity=0.5)
            small_cube.set_stroke(WHITE, width=1)
            small_cube.move_to(pos)
            small_cubes.add(small_cube)
        
        # Add all objects to scene
        self.add_fixed_in_frame_mobjects(title)
        self.add(large_cube)
        self.add(small_cubes)
        
        # Create continuous rotation animation
        self.play(
            Rotating(large_cube, axis=[0, 0, 1], angle=tau, run_time=4, rate_func=linear),
            Rotating(small_cubes, axis=[0, 0, 1], angle=tau, run_time=4, rate_func=linear)
        )