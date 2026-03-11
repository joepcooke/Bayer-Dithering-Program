This program filters images by applying the Bayer dithering technique, then converting it to a chosen colour palette.

In order for this program to function correctly you should (?) unzip the file, and you must have a Python environment installed. In addition, please install the following modules:

Pillow
numpy
matplotlib

This can be done through the following commands:

py -m pip install Pillow
py -m pip install numpy
py -m pip install matplotlib 

if using the default IDE (can do this through the system Command Prompt, can be found by searching Windows apps), or

conda install Pillow
conda install numpy
conda install matplotlib

if using Anaconda based environments (e.g. for Spyder, can type directly into IPython console). The program will notify you if any modules are missing, specifying which ones.

Updating the names of the directories will cause the program to break unless they are updated accordingly in the main program. These is the original directory layout:

Examples
Filtered Images
Palettes
Reference Images
Bayer Dithering Program, v1.0.py
README.txt


USING THE PROGRAM

Add any images you would like to use into the 'Reference Images' folder. These *must* be JPG images. Then, follow the program instructions to filter the image. A greater selection of palettes than those mentioned in the program interface can be found by looking in the 'Palettes' folder.




TIP: for the GameBoy filter, compressed images tend to give off a more noticeable dithering effect, which the GameBoy style lends itself to (in my opinion).