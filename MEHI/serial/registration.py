################################
# Author   : septicmk
# Date     : 2015/07/23 19:20:39
# FileName : registration.py
################################

import numpy as np
import math

def _generate_H(imgA, imgB):
    '''
    Usage:
     - calc the grey level histogram of imgA&B
    '''
    H = np.zeros((255,255))
    _X, _Y = imgA.shape
    for i in range(_X):
        for j in range(_Y):
            H[imgA[i,j],imgB[i,j]] += 1
    return H.astype(float)

def _mutual_info(H):
    '''
    Usage:
     - calc the -(mutual information)
    '''
    tot = .0+ sum(H.flatten())
    p = H/tot
    HAB = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, p.flatten()))
    HA = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, sum(p).flatten()))
    HB = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, sum(p.T).flatten()))
    IAB = HA + HB - HAB
    return -IAB

def _PV_interpolation(H ,p, q):
    '''
    Usage:
     - update the grey level histogram
    '''
    imgA, imgB = imgA, imgB
    _X, _Y = imgA.shape
    px, py = p
    qx, qy = q
    dx, dy = qx-math.floor(qx), qy-math.floor(qy)
    if qx <= 0 or qx >= _X-1 or qy <= 0 or qy >= _Y-1:
        H[imgA[0,0],imgA[0,0]] += 1 
    else:
        H[imgA[int(math.floor(qx)),int(math.floor(qy))], imgB[px, py]] += (1-dx)*(1-dy)
        H[imgA[int(math.floor(qx)),int(math.ceil(qy))], imgB[px, py]] += dx*(1-dy)
        H[imgA[int(math.ceil(qx)),int(math.floor(qy))], imgB[px, py]] += (1-dx)*dy
        H[imgA[int(math.ceil(qx)),int(math.ceil(qy))], imgB[px, py]] += dx*dy

def _get_trans(vec):
    '''
    Usage:
     - calc the U from vec
    '''
    tx, ty, sita, sx, sy, hx, hy= tuple(vec)
    A = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    B = np.array([[math.cos(sita),  -math.sin(sita),  0], [math.sin(sita),  math.cos(sita),  0], [0, 0, 1]])
    C = np.array([[sx,  0,  0], [0, sy, 0], [0, 0, 1]])
    D = np.array([[1, hx, 0], [0, 1, 0], [0, 0, 1]])
    E = np.array([[1, 0, 0], [hy, 1 , 0], [0, 0, 1]])
    F = np.dot(np.dot(A,B),C)
    return np.dot(np.dot(F,D),E)

def _update(vec, imgA, imgB):
    H = _generate_H(imgA, imgB)
    _H = H.copy()
    _X, _Y = imgA.shape
    U = _get_trans(vec)
    for i in range(_X):
        for j in range(_Y):
            p = np.array([i,j,1])
            q = np.dot(U, p)
            p = (p[0],p[1])
            q = (q[0],q[1])
            _PV_interpolation(_H, p, q)
    return _mutual_info(_H)

def _trans(frame, vec):
    from MEHI.udf.TRANS import trans
    frame = frame.copy(order='C')
    ret = np.zeros_like(frame)
    U = _get_trans(vec)
    trans(frame, U, ret)
    return ret  
     
@exeTime        
def p_powell(imgA, imgB ,vec0):
    '''
    Usage:
     - calc the best vector
    '''
    import scipy.optimize as sciop
    def cb(xk):
        print xk
    ret = sciop.fmin_powell(_update, vec0, args=(imgA,imgB), callback=cb)
    return ret


@exeTime
def c_powell(imgA, imgB ,vec0):
    '''
    ditto
    '''
    import scipy.optimize as sciop
    from MEHI.udf.registration import update
    def cb(xk):
        print xk
    ret = sciop.fmin_powell(update, vec0, args=(imgA,imgB), callback=cb)
    return ret

@exeTime
def execute(img_stack, vec):
    '''
    Usage:
     - Affine Transform the img stack using vec
    '''
    def func(frame):
        ret = []
        ret.append(trans(frame, vec))
        ret = np.array(ret)
        return ret
    return map(func, img_stack)
          

if __name__ == '__main__':
    pass
