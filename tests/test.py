import unittest
from unittest import mock
from product_recommentation.utils import get_recommendation


class Test(unittest.TestCase):
    def test_sample_input_one(self,):
        _input = {'prediction': ['Shirts'], 'colors':['white', 'blue', 'red']} 
        result = get_recommendation(prediction=_input['prediction'], colors=_input['colors'])
        # The assertion
        pass



if __name__ == '__main__':
    unittest.main()
