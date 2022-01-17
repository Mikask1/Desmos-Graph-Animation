# Desmos-Graph-Animation
Graphs a video onto Desmos. Example: https://youtu.be/GHGoi_Fn-Wo

## Steps
### Install Dependencies:
```sh
pip install PIL
pip install opencv-python
pip install numpy
pip install potrace
pip install json
pip install regex
pip install tkinter
```

### Run `main.py`
Select the video you want to convert.

### Controls in `main.py`
- Preprocessors (Pick one)
```
OTSU        = Uses Otsu's method to determine the upper and lower bound
SIGMA_BALLS = Uses ... something that has to do with data (I really don't know how this works)
```

- Filters (Decreases the number of equations)
```
FILTERED    = Uses bilateral filter to smooth out the image
L2          = Uses L2 gradient to better calculate the gradient magnitude
```

### Render
Open `index.html`
- Drag and zoom the viewport to make sure all of the image shows
- Press `SET STATE`
- Press `Choose Files` and select all the latex<sub>n</sub>.txt

### Compiling the images
Once it's done rendering, the image sequence will directly download to your downloads folder
- Press `Allow` when it asks you if you want to let it download multiple files
- It will ask you to `Allow` every 50 downloads/frames
- Use a software/tool to combine the image sequence to a video


## FAQ:
- Desmos is a graphing calculator
- Potrace is a software that turns bitmap images to vector (with beizer lines)
- It is recommended to use 10/15 fps and 360p/480p videos to reduce the number of frames you need to load
- Make sure to delete `graphs` folder before converting another video
- You can press `SAVE STATE` to save the current state and use `GET STATE` to return to that state even after reloading.
- You can run multiple `index.html` and do them in batches. Make sure it's on a different window.
- If you run into `OSError: [WinError 1450] Insufficient system resources exist to complete the requested service`, you should manually allocate the number of cores to use in `Pool(os.cpu_count())` to `Pool(5)`


Example:

<img src="https://user-images.githubusercontent.com/88318140/132680429-13c12472-a933-4d96-a3d7-7104ba23e4ed.png" width="350">

<img src="https://user-images.githubusercontent.com/88318140/132681141-a6a3085b-c286-4127-b09a-ec2ea3873604.png" width="350">


