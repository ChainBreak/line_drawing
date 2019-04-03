#!/usr/bin/env python3
import argparse
import math
import numpy as np
import cv2

import paper

class WaveLines():

    def draw_image(self,img_np,paper_size,paper_orientation,num_lines,border):

        cv2.imshow("raw image",img_np)
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
        cv2.imshow("cropped image",img_np)

        #get the new size of the image
        image_h,image_w = img_np.shape

        #do histagram equalisation to spread the intensities output
        img_np = cv2.equalizeHist(img_np)
        cv2.imshow("hist image",img_np)

        # #threashold the brghtest colors to plain white
        # mask = img_np > 128
        # img_np[mask] = 255
        # cv2.imshow("white thresh image",img_np)

        draw_w = paper_w - 2*border #meters
        draw_h = paper_h - 2*border #meters
        line_h = draw_h / num_lines #meters
        max_r = line_h / 2 #meters
        min_wave_length = 5 / 1000 # meters
        step_dist = 1 / 1000 #meters

        for line_i in range(num_lines):
            line_y_center = line_h*(0.5+line_i) + border
            x = border
            y = line_y_center
            theta = 0.0
            ratio = 1.0
            while x < paper_w - border:
                x_step = step_dist
                x += x_step

                theata_step = x_step/min_wave_length




        cv2.waitKey(0)


if __name__ == "__main__":
    print("Hello There!")
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=str, help="file path to an image" )
    args = parser.parse_args()


    img_np = cv2.imread(args.img_path)
    # img_np = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
    wl = WaveLines()

    wl.draw_image(img_np, "A4", "portrait", 2,5/1000)
