################################
# Author   : septicmk
# Date     : 2015/07/24 18:56:05
# FileName : test_p_registration.py
################################

from MEHI.paralleled.registration import *
from MEHI.serial.preprocess import flip
from MEHI.paralleled.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np
from nose.tools import assert_equals
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side_8/'
R_pwd = os.path.abspath('.') + '/test_data/R_side_8/'

class PySparkTestRegistrationCase(PySparkTestCase):
    def setUp(self):
        super(PySparkTestRegistrationCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
        self.imgA = self.L_imgs[0]
        self.imgB = flip(self.R_imgs)[0]
        self.vec0 = [0,0,0,1,1,0,0]
    
    def tearDown(self):
        super(PySparkTestRegistrationCase, self).tearDown()

class TestParalleledRegistration(PySparkTestRegistrationCase):
    def test_p_powell(self):
        pass
        #vec = p_powell(self.imgA, self.imgB, self.vec0)
        #assert (abs(vec[0]-2) <= 5 and abs(vec[1]-3) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_c_powell(self):
        vec = c_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-3) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_execute(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = execute(rdd, self.vec0).collect() 
        ret = np.array(ret)
        assert_equals(sum(self.L_imgs.flatten()), sum(ret.flatten()))