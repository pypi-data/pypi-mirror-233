from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='whitecrop3d',
    version='0.3.1',
    url='https://github.com/cisar2218/whitecrop3d',
    author='Dušan Jánsky',
    author_email='cisar2218@gmail.com',
    description='Crops unnecessary white background from images. Meant to be for 3D models previews.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'whitecrop3d=src.croping:main',
        ],
    },
)
