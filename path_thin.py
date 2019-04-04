#!/usr/bin/env python3
import math


def thin(path_list):
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

                angle = cosine_angle(v0,v1)
                angle_deg = math.degrees(angle)

                if angle_deg > 10.0:
                    path.append(p1)
                    p0 = p1


            path.append(p2)
    return path_list




def cosine_angle(v0,v1):

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


if __name__ == "__main__":
    print("Hello There!")
