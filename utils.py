#!/usr/bin/env python3
import cv2

def ensure_gray(img_np):
    #convert the image to grayscale if it is not already
    if len(img_np.shape) == 3:
        img_np = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
    return img_np

def crop_resize(img_np,out_w,out_h):
    """crops to the desired aspect ratio then resizes"""

    #calculate the aspect ratio of the paper
    target_aspect = out_w / out_h

    #get the size of the image
    image_h,image_w = img_np.shape

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

    #Resize the image to the desired size
    img_np = cv2.resize(img_np,(out_w,out_h))

    return img_np
