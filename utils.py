#!/usr/bin/env python3
import cv2
import math

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

def count_points(path_list):
    point_count = 0
    for path in path_list:
        point_count += len(path)

    return point_count

def thin_path_list(path_list):
    for path in path_list:
        l = len(path)
        if l > 3:
            old_path = path.copy()
            path.clear()

            p0 = old_path[0]
            p2 = old_path[1]

            path.append(p0)
            for i in range(2,l):
                p1 = p2
                p2 = old_path[i]

                #vector betweem points p0 and p1
                v0 = [ p1[0]-p0[0], p1[1]-p0[1] ]
                #vector betweem points p1 and p2
                v1 = [ p2[0]-p1[0], p2[1]-p1[1] ]

                angle = _cosine_angle(v0,v1)
                angle_deg = math.degrees(angle)

                if angle_deg > 10.0:
                    path.append(p1)
                    p0 = p1


            path.append(p2)
    return path_list




def _cosine_angle(v0,v1):

    #calculate the lenght of vector one
    l0 = math.sqrt( v0[0]**2 + v0[1]**2)

    #calculate the lenght of vector two
    l1 = math.sqrt( v1[0]**2 + v1[1]**2)

    #normalise vector one
    v0[0] /= l0
    v0[1] /= l0

    #normalise vector two
    v1[0] /= l1
    v1[1] /= l1

    #do the dot product
    dot = v0[0]*v1[0] + v0[1]*v1[1]

    #calculate the angle between the vectors in radians
    angle = math.acos(dot)

    return angle
