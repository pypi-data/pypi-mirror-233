# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import unittest
import numpy as np
import pyBlindOpt.hc as hc


# define objective function
def f1(x):
    return np.power(x, 2)[0]


# define objective function
def f2(x):
    return x[0]**2.0 + x[1]**2.0


# define global variable and callback
total = 0
def callback(epoch, best, current, candidate):
    global total
    total += 1


class TestHC(unittest.TestCase):
    def test_hc_00(self):
        bounds = np.asarray([(-5.0, 5.0)])
        result, _ = hc.hillclimbing(f1, bounds, n_iter=1500, verbose=False)
        desired = np.array([0])
        np.testing.assert_allclose(result, desired, atol=1)
    
    def test_hc_01(self):
        bounds = np.asarray([(-5.0, 5.0), (-5.0, 5.0)])
        result, _ = hc.hillclimbing(f2, bounds, n_iter=1500, verbose=False)
        desired = np.array([0.0, 0.0])
        np.testing.assert_allclose(result, desired, atol=1)
    
    def test_hc_02(self):
        global total
        total = 0
        bounds = np.asarray([(-5.0, 5.0), (-5.0, 5.0)])
        hc.hillclimbing(f2, bounds, n_iter=10, callback=callback, verbose=False)
        desired = 10
        self.assertEqual(total, desired)
    
    def test_hc_03(self):
        bounds = np.asarray([(-5.0, 5.0), (-5.0, 5.0)])
        result, _ = hc.hillclimbing(f2, bounds, n_iter=100, verbose=False)
        self.assertTrue(isinstance(result,np.ndarray))
    
    def test_hc_04(self):
        n_iter = 100
        bounds = np.asarray([(-5.0, 5.0), (-5.0, 5.0)])
        _, _, debug = hc.hillclimbing(f2, bounds, n_iter=n_iter, verbose=False, debug=True)
        
        self.assertTrue(isinstance(debug, list))
        self.assertEqual(len(debug), n_iter)
        