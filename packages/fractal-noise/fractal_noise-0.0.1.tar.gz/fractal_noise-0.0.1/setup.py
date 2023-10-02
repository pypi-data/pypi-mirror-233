from setuptools import setup, find_packages

setup(
    name="fractal_noise",
    version="0.0.1",
    description="Python implementation for Fractal Noise, ideal for creating realistic terrain, cloud-like textures, and intricate visual effects.",
    author="Sophia Shovkovy",
    author_email="sophiashovkovy@gmail.com",
    packages=find_packages(include=["fractal_noise"]),
    install_requires=["numpy", "perlin-noise"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
