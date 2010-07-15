#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Image
import ImageDraw

def fractal(draw, x, y, r):
    if r > 0:
        fractal(draw, x-r/2, y-r/2, r/2);
        fractal(draw, x-r/2, y+r/2, r/2);
        fractal(draw, x+r/2, y-r/2, r/2);
        fractal(draw, x+r/2, y+r/2, r/2);
        box(draw, x, y, r);

def box(draw, x, y, r):
    ## random color
    import random
    draw.rectangle([x-r/2, y-r/2, x+r/2, y+r/2], fill=random.randint(0, 256))

    ## hierarchical color
#    draw.rectangle([x-r/2, y-r/2, x+r/2, y+r/2], fill=r % 256)

    ## same color
#    draw.rectangle([x-r/2, y-r/2, x+r/2, y+r/2], fill=128)

if __name__ == '__main__':
    image_size = 400
    im = Image.new('RGB', (image_size, image_size), '#ffffff')
    draw = ImageDraw.Draw(im)
    fractal(draw, image_size/2, image_size/2, image_size/2)
    im.show()
