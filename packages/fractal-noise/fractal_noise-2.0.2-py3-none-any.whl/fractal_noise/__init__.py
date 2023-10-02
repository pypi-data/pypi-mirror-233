import numpy as np
from perlin_noise import PerlinNoise


def get_fractal_noise(width, height, scale, octaves) -> np.array:
    """Generate Fractal Noise using the Perlin Noise algorithm."""

    # Input validation
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Width and height must be integers.")
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    if not isinstance(scale, (int, float)) or scale <= 0:
        raise ValueError("Scale must be a positive number.")
    if not isinstance(octaves, list) or not all(
        isinstance(octaves, int) and octave > 0 for octave in octaves
    ):
        raise ValueError("Octaves must be a list of positive integers.")

    # Initialize the noise array with zeros
    noise = np.zeros((width, height))

    for octave in octaves:
        # Double the level of detail
        # Each successive octave has noise patterns 2x smaller than the previous octave
        octave_scale = scale * (2**octave)

        # Generate Perlin Noise for the current octave
        perlin_noise = PerlinNoise(octaves=octave + 1)

        # Add the Perlin Noise to the noise array
        for x in range(width):
            for y in range(height):
                noise[x, y] += perlin_noise(
                    [x / width * octave_scale, y / height * octave_scale]
                )

    return noise
