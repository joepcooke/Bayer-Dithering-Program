# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 23:00:37 2025

@author: joepc
"""


#in case module importing fails
run_program = True

#import modules

import json
import copy


#import Pillow
try:
    
    from PIL import Image
   
except:
    
    run_program = False
    
    print("Pillow module not found. To install this, please run in your command window: py -m pip install Pillow OR in IPython: conda install Pillow (depending on your environment).")


#import matplotlib
try:
    
    from matplotlib import pyplot as plt

except:
    
    run_program = False
    
    print("matplotlib module not found. To install this, please run in your command window: py -m pip install matplotlib OR in IPython: conda install matplotlib (depending on your environment).")


#import numpy and define constants/parameters
try:
    
    import numpy as np
    
    #define source and destination relative paths

    ref_img_path = ".\\Reference Images\\"
    dest_img_path = ".\\Filtered Images\\"
    palette_path = ".\\Palettes\\"

    #file name we wish to read
    img_name = "man"

    #size of the bayer matrices
    n = 16

    #possible filter matrices

    bayer_matrices = [
        
        np.array([
         
         [0, 2],

         [3, 1]
         
         ]),
        
        np.array([
         
         [0, 8, 2, 10],

         [12, 4, 14, 6],
         
         [3, 11, 1, 9],
         
         [15, 7, 13, 5]
         
         ]),
        
        np.array([
         
         [0, 32, 8, 40, 2, 34, 10, 42],
         [48, 16, 56, 24, 50, 18, 58, 26],
         [12, 44, 4, 36, 14, 46, 6, 38],
         [60, 28, 52, 20, 62, 30, 54, 22],
         [3, 35, 11, 43, 1, 33, 9, 41],
         [51, 19, 59, 27, 49, 17, 57, 25], 
         [15, 47, 7, 39, 13, 45, 5, 37],
         [63, 31, 55, 23, 61, 29, 53, 21]
         
         ]),
         
         np.array([
          
          [0, 128, 32, 160, 8, 136, 40, 168, 2, 130, 34, 162, 10, 138, 42, 170],
          [192, 64, 224, 96, 200, 72, 232, 104, 194, 66, 226, 98, 202, 74, 234, 106],
          [48, 176, 16, 144, 56, 184, 24, 152, 50, 178, 18, 146, 58, 186, 26, 154],
          [240, 112, 208, 80, 248, 120, 216, 88, 242, 114, 210, 82, 250, 122, 218, 90],
          [12, 140, 44, 172, 4, 132, 36, 164, 14, 142, 46, 174, 6, 134, 38, 166],
          [204, 76, 236, 108, 196, 68, 228, 100, 206, 78, 238, 110, 198, 70, 230, 102],
          [60, 188, 28, 156, 52, 180, 20, 148, 62, 190, 30, 158, 54, 182, 22, 150],
          [252, 124, 220, 92, 244, 116, 212, 84, 254, 126, 222, 94, 246, 118, 214, 86], 
          [3, 131, 35, 163, 11, 139, 43, 171, 1, 129, 33, 161, 9, 137, 41, 169],
          [195, 67, 227, 99, 203, 75, 235, 107, 193, 65, 225, 97, 201, 73, 233, 105],
          [51, 179, 19, 147, 59, 187, 27, 155, 49, 177, 17, 145, 57, 185, 25, 153],
          [243, 115, 211, 83, 251, 123, 219, 91, 241, 113, 209, 81, 249, 121, 217, 89],
          [15, 143, 47, 175, 7, 135, 39, 167, 13, 141, 45, 173, 5, 133, 37, 165],
          [207, 79, 239, 111, 199, 71, 231, 103, 205, 77, 237, 109, 197, 69, 229, 101],
          [63, 191, 31, 159, 55, 183, 23, 151, 61, 189, 29, 157, 53, 181, 21, 149],
          [255, 127, 223, 95, 247, 119, 215, 87, 253, 125, 221, 93, 245, 117, 213, 85]
          
          ])
         
         ]
    
    
except:
    
    run_program = False
    
    print("numpy module not found. To install this, please run in your command window: py -m pip install numpy OR in IPython: conda install numpy (depending on your environment).")


#define functions

#round down length and width of image to divide perfectly by filter size n, so filter can be applied to image an exact number of times

def crop_image(np_frame, n):

    image_rows = (np.shape(np_frame)[0] // n) * n
    image_cols = (np.shape(np_frame)[1] // n) * n

    image_arr = np_frame[0:image_rows, 0:image_cols]

    return image_arr


def bayer_dither(image_arr, spread, filter_size = 4):    
    
    rows, cols = np.shape(image_arr)[0:2]
    
    #to find the appropriate Bayer matrix, find the base 2 log of the filter size then index to list
    
    bayer_index = int(np.log2(filter_size)) - 1
    
    bayer_matrix = bayer_matrices[bayer_index]
    
    #scale to be between 0 and 1
    
    bm_scaled = (1 / 256) * bayer_matrix
    
    
    #shift (normalise) to be between -0.5 and 0.5 (although technically max isn't 0.5 so I think this changes
    #the overall brightness ever so slightly)
    
    bayer_noise = bm_scaled - 0.5
    
    #create new image array for floats, as this function returns values between 0 and 1
    
    new_image_arr = np.zeros(np.shape(image_arr), dtype = np.float32())
    
    for i in range(rows):
        
        for j in range(cols):
            
            #find rgb of pixels
            pixel_vals = copy.copy(image_arr[i,j])
            
            #calculate rgb values as between 0 and 1
            
            r = pixel_vals[0] / 255
            g = pixel_vals[1] / 255
            b = pixel_vals[2] / 255
            
            #calculate indices of where pixel lands in filter (somewhere between 0-15 for x and y)
            
            bayer_i = i % filter_size
            
            bayer_j = j % filter_size
            
            #calculate dithered values for each channel
            
            r_dith = r + spread * bayer_noise[bayer_i, bayer_j]
            g_dith = g + spread * bayer_noise[bayer_i, bayer_j]
            b_dith = b + spread * bayer_noise[bayer_i, bayer_j]
            
            new_pixel_vals = np.array([r_dith, g_dith, b_dith], dtype = np.float32())
            
            new_image_arr[i, j] = new_pixel_vals
            
    return new_image_arr

#requires scaled values with rgb values between 0 and 1

def quantize_image(image_arr_scaled, palette, levels = 2):
    
    rows, cols = np.shape(image_arr_scaled)[0:2]    
    
    #create an empty array of the same shape to store new pixel data, now needs to be np.uint8() in order to be valid
    #for pillow function
    
    new_image_arr = np.zeros(np.shape(image_arr_scaled), dtype = np.uint8())
    
    for i in range(rows):
        
        for j in range(cols):
            
            #find scaled rgb values of dithered pixels
            
            dithered_pixel_vals = copy.copy(image_arr_scaled[i,j])
            
            r_dith = dithered_pixel_vals[0]
            g_dith = dithered_pixel_vals[1]
            b_dith = dithered_pixel_vals[2]
            
            #calculate nearest colours in each channel according to specified levels (returns values between 0 and 1
            #so need to be scaled)
            
            
            #if no palette is specified assume levels and create equally spaced colours across spectrum
            
            if np.shape(palette) == ():
            
                new_r_scaled = np.round((levels - 1) * r_dith) / (levels - 1)
                new_g_scaled = np.round((levels - 1) * g_dith) / (levels - 1)
                new_b_scaled = np.round((levels - 1) * b_dith) / (levels - 1)
                
                #multiply by 255 and convert to np.uint8 so they're of the correct data type and value
                
                new_r = np.uint8(new_r_scaled * 255)
                new_g = np.uint8(new_g_scaled * 255)
                new_b = np.uint8(new_b_scaled * 255)
            
                new_pixel_vals = np.array([new_r, new_g, new_b], dtype = np.uint8())
                
            #otherwise, use the specified palette
            
            else:
                
                #palette must be a numpy array!
                
                #scale palette so values are between 0 and 1
                
                scaled_palette = palette / 255
                
                #calculate displacements from given pixel value to all colours in the palette
                
                colour_displacements = scaled_palette - dithered_pixel_vals
                
                #calculate euclidean distances for each colour
                
                colour_distances = np.linalg.norm(colour_displacements, axis = 1)
                
                #find index for minimum distance (i.e. closest colour)
                
                closest_col_index = np.argmin(colour_distances)
                
                #find corresponding closest colour
                
                new_pixel_vals = palette[closest_col_index]
    
            new_image_arr[i, j] = new_pixel_vals
    
    
    return new_image_arr



###############################################  MAIN CODE  ###############################################

def main():
    
    exit_program = False    
    
    while exit_program == False:
         
        #INPUTS
        
        #image choice 
        im_frame = None
        
        #palette choice
        palette_choice = []
        
        #filter size
        n = 0

        #OTHER
        
        #used for validation
        palette_name = "!"

        #select image (out of file names in 'Reference Images' folder)
        
        while im_frame == None:
            
            img_name = input("\nPlease enter the file name of the image contained in the 'Reference Images' folder that you wish to edit; the image must be in a .jpg format. To exit the program, simply press Enter at any time. ")
            
            if img_name == "":
                
                exit_program = True
                
                break
            
            #remove file extension if entered
            img_name = img_name.replace(".jpg", "")
            
            try:
                
                im_frame = Image.open(ref_img_path + img_name + ".jpg")
            
            except:
                
                print("\nImage not found. Please check you have entered correctly, or try another image.")
        
        if exit_program:
            
            break
        
        
        #select palette type (out of file names in 'Palettes' folder)
    
        while palette_name == "!":
            
            palette_name = input("\nPlease enter the palette type to filter with. Some presets are: \n\n one_bit: Filters the image to be made entirely of black and white pixels. \n\n three_bit: Filters the image to contain only black, white, red, blue, green, magenta, yellow and cyan. \n\n gameboy: Filters the image to the colour palette of the original GameBoy. \n\n You can add custom palettes by creating .txt files in the 'Palettes' folder. ")
            
            if palette_name == "":
                
                exit_program = True
                
                break
            
            #remove file extension if entered
            palette_name = palette_name.replace(".txt", "")
            
            try:
                
                file = open(palette_path + palette_name + ".txt", "r")
                
                palette_choice = np.array(json.loads(file.read()))
                
                file.close()
                
            except:
                
                print("\nSomething went wrong. Either the palette was not found, or the format of the palette is not correct. Please try again.")
                
                palette_name = "!"
                
        if exit_program:
                
            break
        
        
        #select filter size (out of 2, 4, 8 or 16)
        
        while n == 0:
            
            filter_size = input("\nPlease enter the filter size you would like the Bayer dithering effect to use, out of 2, 4, 8 or 16. Note: 16 is recommended, as greater size maintains more detail and better lighting. ")
            
            if filter_size == "":
                
                exit_program = True
                
                break
            
            if filter_size in ["2", "4", "8", "16"]:
                
                n = int(filter_size)
            
            else:
                
                print("\nInput was not one of the valid filter size numbers. Please try again.")
        
        if exit_program:
            
            break
        
        
        #FILTERING THE IMAGE
        
        #convert reference image to a numpy array
        np_frame = np.array(im_frame, dtype = np.uint8())
    
 
    
        #crop image so filter can be used exactly
        print("\nCropping image...")   
        
        cropped_image = crop_image(np_frame, n)
        
        
        #dither image
        print("\nApplying Bayer dither...")
        
        dithered_image = bayer_dither(cropped_image, spread = 1, filter_size = n)
        
        
        #quantize image
        print("\nQuantizing image using chosen palette...")
        quantized_image = quantize_image(dithered_image, palette = palette_choice)
        
        
        #save new image
        print("\nSaving filtered image...")
        
        img = Image.fromarray(quantized_image, "RGB")
        
        img_name = img_name.replace(".jpg", ".png")
        
        img.save(dest_img_path + img_name + ".png")
        
        
        #display new image
        img.show()
        
        
        #reset inputs
        
        im_frame = None
        
        palette_choice = None
        
        n = 0
        
        print("\nImage filter complete. The saved image can be found in the 'Filtered Images' folder.\n\n")

        
if run_program == True:
    
    main()
    
else:
    
    input("\nPress Enter to close. ")

