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
        img_raw = img_np
        # if img_debug: cv2.imshow("raw image",img_np)
        img_np = utils.ensure_gray(img_np)

        #Resize the image to a nominal size so that blurs and effects are proportionate
        image_w,image_h = paper.size("A4",paper_orientation)
        image_w = int(round(image_w*1000))
        image_h = int(round(image_h*1000))
        img_np = utils.crop_resize(img_np,image_w,image_h)
        if img_debug: cv2.imshow("nominal size",img_np)


        # #thresh hold the to solid white
        # mask = img_np > 150
        # img_np[mask] = 255
        # if img_debug: cv2.imshow("thresh",img_np)



        canvas = np.ones_like(img_np)*255

        if animate:
            cv2.namedWindow("crop",0)
            cv2.namedWindow("difference",0)
            cv2.namedWindow("canvas",0)

        while True:


            #blur difference image
            k = 7
            canvas_blur = cv2.GaussianBlur(canvas,(k,k),0)
            canvas_blur = cv2.GaussianBlur(canvas_blur,(k,k),0)
            # canvas_blur = cv2.GaussianBlur(canvas_blur,(k,k),0)
            #calculate difference image
            img_diff_np = cv2.subtract(canvas_blur,img_np)

            # #thresh hold the to solid white
            # mask = img_diff_np<50
            # img_diff_np[mask] = 0


            #find the brigest pixel as a starting location
            rand_img = img_diff_np*np.random.rand(*img_np.shape)
            brigest = np.argmax(rand_img)
            cv2.imshow("rand",rand_img)
            cv2.waitKey(1)
            y,x = np.unravel_index(brigest,img_diff_np.shape)
            print(x,y)
            # x,y = (0,0)

            dx,dy = 0.,0.
            for i in range(100):
                kernel=11
                step = 5


                x = np.clip(x, 0, image_w-1)
                y = np.clip(y, 0, image_h-1)
                M = np.array([[1,0,kernel/2 - x], [0,1, kernel/2 - y]], dtype="float32")
                crop = cv2.warpAffine(img_diff_np,M,(kernel,kernel))


                #find the centroid
                h,w = crop.shape
                dist = np.arange(w).reshape(1,w).astype("float")
                crop_sum = np.sum(crop)+ 10e-6
                xc = np.sum(crop * dist )/ crop_sum
                yc = np.sum(crop * dist.T) / crop_sum


                #get the vector from the center of the crop to the centroid
                new_dx = xc - kernel//2
                new_dy = yc - kernel//2

                #get the length of the vector
                l = math.sqrt(new_dx**2 + new_dy**2) + 10e-6

                new_dx *= step/l
                new_dy *= step/l

                last_x,last_y = x,y

                alpha = 0.05
                dx += alpha*(new_dx - dx)
                dy += alpha*(new_dy - dy)

                x += dx
                y += dy

                x = np.clip(x, 0, image_w-1)
                y = np.clip(y, 0, image_h-1)


                cv2.line(img_diff_np,(int(round(last_x)),int(round(last_y))),(int(round(x)),int(round(y))),0)
                cv2.line(canvas,(int(round(last_x)),int(round(last_y))),(int(round(x)),int(round(y))),0)

                #normalise the vector then scale by the step speed

                # print(xc,yc,dx,dy,l)


                if animate:
                    cv2.imshow("crop",(crop).astype("uint8"))
                    cv2.imshow("difference",img_diff_np)
                    cv2.imshow("canvas",canvas)
                    cv2.waitKey(1)






        if img_debug: cv2.waitKey(100)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=str, help="file path to an image" )
    args = parser.parse_args()


    img_np = cv2.imread(args.img_path)

    scribble = Scribble()

    stroke_list = scribble(img_np,"A4", "portrait")
