# Desmos-Graph-Animation
Graphs an animation onto Desmos

Install Dependencies:
```sh
pip install PIL
pip install opencv-python
pip install numpy
pip install potrace
```

Steps:
1. Run `main.py` and select a video to convert to latex<sub>n</sub>.txt
2. Open `index.html`
3. Set the calculator view so that you can see the entire image (400 px x 600 px = 400 x 600) and then press `SET STATE` (make sure it's blank and the image fits)
4. Locate the graphs folder and input the latex<sub>n</sub>.txt
5. Screenshot your screen
6. Press `RESET` (this will reset the view to the state you've set)
7. Repeat step 4-6 for every frame
8. Use a tool to convert the screenshot image sequence to a video

FAQ:
- Desmos is a graphing calculator
- Potrace is a software that turns edges into beizer lines
- It is recommended to use 10/15 fps videos to reduce the number of frames you need to load
- You still need to screenshot every frame as it's still on working progress
- Make sure to delete `frames` and `graphs` folder before converting another video


For obvious reasons, I will not be uploading the image sequence, or the video here.

Example:

<img src="https://user-images.githubusercontent.com/88318140/132680429-13c12472-a933-4d96-a3d7-7104ba23e4ed.png" width="350">

<img src="https://user-images.githubusercontent.com/88318140/132681141-a6a3085b-c286-4127-b09a-ec2ea3873604.png" width="350">


