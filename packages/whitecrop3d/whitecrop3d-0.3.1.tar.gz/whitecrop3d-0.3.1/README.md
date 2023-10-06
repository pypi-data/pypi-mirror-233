# whitecrop3d
## Description
- Crops unnecessary white background from images. Meant to be for 3D models previews. 
- Whitecrop3d was developed as temporary solution for problem of 3D graphics that was time expensive to solve. We worked on solving problem properly after this temporary solution was implemeneted.
## Usage
- Install globaly: `$ sudo pip install whitecrop3d`
- Use: `$ whitecrop3d path/to/your/pngs`

### Preview
![Preview](previews/image.png)

## How it works
Do this for all images in path specified:
1. Loads image
2. Crops the image based on white background
3. Adds background to match original 1024x768 resolution
4. Saves image (inplace)
## Notes for Developers
- for further github actions
### Upload new version to PYPI
- increment version in `setup.py` file
- run `publish_to_pypi.sh`, or manualy run:
    - `$ rm dist/*`
    - `$ python3 -m build`
    - `$ python3 -m twine upload dist/*`
- note: github secret must be provided to authorize upload (not added to github repo yet)