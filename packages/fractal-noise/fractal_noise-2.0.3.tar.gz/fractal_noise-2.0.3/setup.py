from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fractal_noise",
    packages=find_packages(include=["fractal_noise"]),
    version="2.0.3",
    description="Python implementation for Fractal Noise, ideal for creating realistic terrain, cloud-like textures, and intricate visual effects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sophia Shovkovy",
    author_email="sophiashovkovy@gmail.com",
    install_requires=["numpy", "perlin-noise"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
