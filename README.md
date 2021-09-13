# Desmos-Graph-Animation
FINISHED


This branch only graphs an image

Install Dependencies:
```sh
pip install PIL
pip install opencv-python
pip install numpy
pip install potrace
```

How to use Image to Graph:
- Run main.py
- Pick the image you want
- It will take some time, there should be a latex.txt as a result
- Copy and paste the latex.txt content to Desmos Graphing Calculator (just select all and copy, then paste on to the first equation on Desmos)

The different ways you can make the result better:
- Use the different edge-finder functions (e.g. thresh, sigma_balls, or otsu)
- Set filtered to True or False (Filtering it will simplify the image)
