################################
# Author   : septicmk
# Date     : 2015/07/23 20:10:23
# FileName : preprocess.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import math

def stripe_removal(img_stack):
    '''
    Usage:
     - remove the stripe
     - (discarded)
    '''
    import skimage.morphology as mor
    def func(frame):
        _dtype = frame.dtype
        kernel = nor.disk(3)
        frameWP = frame - mor.white_tophat(frame, kernel) * (mor.white_tophat(frame, kernel) > 1000).astype(float)
        kernel = mor.rectangle(25, 1)
        closed = mor.closing(frameWP, kernel)
        opened = mor.opening(closed, kernel)
        result = ((frameWP.astype(float) / opened.astype(float)) * 3000.0)
        return result.astype(_dtype)
    return map(func, img_stack).astype(img_stack[0].dtype)

def intensity_normalization(img_stack, dtype=None):
    '''
    Usage:
     - adjust the intensity
    args:
     - num: if you wanna 16-bit output, just let num = 16,  
    '''
    def func8(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)).astype(np.uint8)
    def func16(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*65535, frame)).astype(np.uint16)
    def funca(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        if frame.dtype == np.uint8:
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)).astype(np.uint8)
        else:
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*65535, frame)).astype(np.uint16)
    if dtype == 8:
        return map(func8, img_stack).astype(np.uint8)
    elif dtype == 16:
        return map(func16, img_stack).astype(np.uint16)
    else:
        return map(funca, img_stack).astype(img_stack[0].dtype)

def flip(img_stack):
    def func(frame):
        return frame[:,::-1]
    return map(func,img_stack)
    
def invert(img_stack):
    def func(frame):
        if frame.dtype == np.uint8:
            return map(lambda p: 255-p, frame)
        elif frame.dtype == np.uint16:
            return map(lambda p: 65535-p, frame)
        else :
            return map(lambda p: p, frame)
    return map(func, img_stack)

def black_tophat(img_stack, size=15):
    '''
    Usage:
     - black tophat 
     - change the circle to pie
    Args:
     - size: the smooth size 
    '''
    import skimage.morphology as mor
    def func(frame):
        return mor.black_tophat(frame, mor.disk(size))
    return map(func, img_stack)

def subtract_Background(img_stack, size=10):
    '''
    Usage:
     - subtrackt Background (based on C)
    args:
     - radius: the smooth size
    '''
    from MEHI.udf.SB import subtract_Background
    def func(frame):
        return subtract_Background(frame, size)
    return map(func, img_stack)
        
if __name__ == '__main__':
    print 'OK'
    pass
