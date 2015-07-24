################################
# Author   : septicmk
# Date     : 2015/07/24 15:39:02
# FileName : test_preprocess.py
################################

from MEHI.serial.preprocess import *
from MEHI.serial.IO import load_tiff
from test_utils import LocalTestCase
import numpy as np

L_pwd = os.path.abspath('.') + 'test_data/L_side/'
R_pwd = os.path.abspath('.') + 'test_data/R_side/'

class LocalTestPreprocessCase(LocalTestCase):
    def setUp(self):
        super(LocalTestPreprocessCase, self).setUp()
        self.L_imgs = load_tiff(L_pwd)
        self.R_imgs = load_tiff(R_pwd)

    def tearDown(self):
        super(LocalTestPreprocessCase, self).tearDown()

class TestSerialPreprocess(LocalTestPreprocessCase):
    def test_stripe_removal():
        ret = stripe_removal(self.self.L_imgs)
        assert (ret.shape == self.self.L_imgs.shape) 
        assert (ret.dtype == self.self.L_imgs.dtype)
    
    def test_intensity_normalization():
        ret = intensity_normalization(self.L_imgs)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
        ret = intensity_normalization(self.L_imgs, 8)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint8)
        ret = intensity_normalization(self.L_imgs, 16) 
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint16)
    
    def test_flip():
        ret = flip(self.L_imgs)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_invert():
        ret = invert(self.L_imgs)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_black_tophat():
        ret = black_tophat(self.L_imgs)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_subtract_Background():
        ret = subtract_Background(self.L_imgs)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_shrink():
        ret = shrink(self.L_imgs)
        assert (ret.dtype == self.L_imgs.dtype)
        assert (ret.shape == (10, 256, 256))
