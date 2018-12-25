import os

from setuptools import setup, find_packages

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path) as f:
    description = f.read()

setup(
    name='pixela2img',
    varsion='2018.1',
    author='ryosms',
    url='https://github.com/ryosms/pixela2img',
    description="Create image files or objects from pixela svg graphs.",
    long_description=description,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    install_requires=['pillow', 'defusedxml'],
)
