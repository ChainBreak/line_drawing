#!/usr/bin/env python3
import cv2
import math
import argparse
import utils
import json
import numpy as np

import paper
import utils

img_debug = True
animate = True

class Scribble():

    def __call__(self,img_np,paper_size,paper_orientation):
        # if img_debug: cv2.imshow("raw image",img_np)
        img_np = utils.ensure_gray(img_np)

        #Resize the image to a nominal size so that blurs and effects are proportionate
        image_w,image_h = paper.size("A4",paper_orientation)
        image_w = int(round(image_w*1000))
        image_h = int(round(image_h*1000))
        img_np = utils.crop_resize(img_np,image_w,image_h)
        if img_debug: cv2.imshow("nominal size",img_np)

        #thresh hold the to solid white
        mask = img_np > 150
        img_np[mask] = 255

        if img_debug: cv2.imshow("thresh",img_np)



        #invert the image colors
        img_np = 255 - img_np
        # if img_debug: cv2.imshow("invert",img_np)


        canvas = np.ones_like(img_np)*255

        if animate:
            cv2.namedWindow("crop",0)
            cv2.namedWindow("invert",0)
            cv2.namedWindow("canvas",0)

        while True:

            #find the brigest pixel as a starting location

            y,x = np.unravel_index(np.argmax(img_np*np.random.rand(*img_np.shape)),img_np.shape)

            # x,y = (0,0)

            for i in range(50):
                kernel=5
                step = 5
                x = np.clip(x, kernel, image_w-kernel-1)
                y = np.clip(y, kernel, image_h-kernel-1)
                xi,yi = int(x),int(y)

                x0,y0 = xi-kernel,yi-kernel
                x1,y1 = xi+kernel+1,yi+kernel+1


                crop = img_np[y0:y1,x0:x1].astype("float")


                #find the centroid
                h,w = crop.shape
                dist = np.arange(w).reshape(1,w).astype("float")
                crop_sum = np.sum(crop)+ 10e-6
                xc = np.sum(crop * dist )/ crop_sum
                yc = np.sum(crop * dist.T) / crop_sum


                #get the vector from the center of the crop to the centroid
                dx = xc - kernel
                dy = yc - kernel

                #get the length of the vector
                l = math.sqrt(dx**2 + dy**2) + 10e-6

                dx *= step/l
                dy *= step/l

                last_x,last_y = x,y

                x += dx
                y += dy

                cv2.line(img_np,(int(round(last_x)),int(round(last_y))),(int(round(x)),int(round(y))),0)
                cv2.line(canvas,(int(round(last_x)),int(round(last_y))),(int(round(x)),int(round(y))),0)

                #normalise the vector then scale by the step speed

                print(xc,yc,dx,dy,l)


                if animate:
                    cv2.imshow("crop",(crop).astype("uint8"))
                    cv2.imshow("invert",img_np)
                    cv2.imshow("canvas",canvas)
                    cv2.waitKey(1)






        if img_debug: cv2.waitKey(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=str, help="file path to an image" )
    args = parser.parse_args()


    img_np = cv2.imread(args.img_path)

    scribble = Scribble()

    stroke_list = scribble(img_np,"A4", "portrait")
