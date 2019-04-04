#!/usr/bin/env python3
import argparse
import math
import numpy as np
import cv2
import json
import os

import paper
import plot_path
import path_thin

img_debug = True

class WaveLines():

    def draw_image(self,img_np,paper_size,paper_orientation,num_lines,border):

        if img_debug: cv2.imshow("raw image",img_np)
        #convert the image to grayscale if it is not already
        if len(img_np.shape) == 3:
            img_np = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)

        #get the size of the image
        image_h,image_w = img_np.shape

        #get the size of the paper
        paper_w,paper_h = paper.size(paper_size,paper_orientation)

        #calculate the aspect ratio of the paper
        target_aspect = paper_w / paper_h


        crop_h = image_h
        crop_w = crop_h * target_aspect

        if crop_w > image_w:
            crop_w = image_w
            crop_h = crop_w / target_aspect


        #get the pixel coordinates of the center crop
        x0 = int(round((image_w-crop_w)/2))
        x1 = x0 + int(round(crop_w))
        y0 = int(round((image_h-crop_h)/2))
        y1 = y0 + int(round(crop_h))

        #take a crop out of the image that has the same aspect ratio as the paper
        img_np = img_np[y0:y1,x0:x1]
        if img_debug: cv2.imshow("cropped image",img_np)

        #Resize the image to a nominal size so that blurs and effects are proportionate
        image_w,image_h = paper.size("A4",paper_orientation)
        image_w = int(round(image_w*1000))
        image_h = int(round(image_h*1000))
        img_np = cv2.resize(img_np,(image_w,image_h))
        if img_debug: cv2.imshow("nominal size",img_np)


        #do histagram equalisation to spread the intensities out
        img_np = cv2.equalizeHist(img_np)
        if img_debug: cv2.imshow("hist image",img_np)

        #blur the image to smooth it out
        k = 7
        img_np = cv2.GaussianBlur(img_np,(k,k),0)
        img_np = cv2.GaussianBlur(img_np,(k,k),0)
        # img_np = cv2.GaussianBlur(img_np,(k,k),0)
        if img_debug: cv2.imshow("blur",img_np)


        draw_h = paper_h - 2*border
        draw_w = paper_w - 2*border

        #calculate the distance in between lines
        line_spacing = image_h / num_lines #pixels

        #The maximum amplitute of a wave is half the line spacing
        max_amplitute = line_spacing / 2 #pixels


        min_wave_length = line_spacing / 3 #pixels
        step_dist = 0.1  #pixels

        path_list = []

        path_count = 0
        point_count = 0

        for line_i in range(num_lines):
            line_y_center = line_spacing*(0.5+line_i)
            x = 0.0
            y = line_y_center
            theta = 0.0

            pixel_intensity = 0.0

            path = []
            path_list.append(path)
            path_count += 1

            first_point = True

            #scan accros the image
            while x < image_w:

                xi = int(x)
                yi = int(line_y_center)

                #0 white 1 black
                new_pixel_intensity = 1.0 - float(img_np[yi,xi] / 255)

                if first_point:
                    first_point = False
                    pixel_intensity = new_pixel_intensity

                #use lowpass filter to smooth out changes in pixel intensities
                pixel_intensity += 0.1 * (new_pixel_intensity - pixel_intensity)


                #the ratio between x and theta
                theta_ratio = pixel_intensity * 2*math.pi/min_wave_length

                #the x step is adjusted so that it takes smaller steps when its on stepper parts of the sign wave
                x_step = math.sqrt( step_dist**2/ (1 + theta_ratio**2 * math.cos(theta)**2))

                #step the x position along
                x += x_step

                #step the theata along acording to the theta ratio
                theta += x_step * theta_ratio

                #calculate the y position.
                y = line_y_center + max_amplitute * pixel_intensity * math.sin(theta)

                #scale from image coordinates to paper coordinates with border
                x_draw = x / image_w * draw_w + border
                y_draw = y / image_h * draw_h + border

                #append this point to the path
                path.append((x_draw,y_draw))
                point_count += 1

        cv2.waitKey(1)

        print("path_count",path_count)
        print("point_count", point_count)
        return path_list


if __name__ == "__main__":
    print("Hello There!")
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=str, help="file path to an image" )
    args = parser.parse_args()


    img_np = cv2.imread(args.img_path)
    # img_np = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
    wl = WaveLines()
    path_list = wl.draw_image(img_np, "A4", "portrait", 40,0.005)
    plot_path.plot(path_list)
    path_list = path_thin.thin(path_list)


    output_path = ".".join(args.img_path.split(".")[:-1]) + ".json"
    print(output_path)

    with open(output_path,'w') as f:
        json.dump(path_list,f,indent=4)

    plot_path.plot(path_list)
