#!/usr/bin/env python3
import math
def size(paper_size,orientation):
    paper_sizes = ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]
    orientations = ["portrait", "landscape"]
    assert paper_size in paper_sizes, "Paper size muse be one of %s"%" ".join(paper_sizes)
    assert orientation in orientations, "Orientation must be either portrait or landscape"

    paper_type = paper_size[0]

    if paper_type == "A":
        i = int(paper_size[1:])
        a_const = 1.0 * math.pow(2.0,1/4)
        w = a_const*math.pow( 2, -(i+1)/2 )
        h = a_const*math.pow( 2, -i/2 )

    if orientation == "landscape":
        w,h = h,w

    return w,h


if __name__ == "__main__":
    print("Hello There!")
    for orientation in ["portrait", "landscape"]:
        for paper_size in ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]:
            w,h = size(paper_size,orientation)
            print("%s %s %ix%imm"%(orientation,paper_size,round(w*1000),round(h*1000)))
