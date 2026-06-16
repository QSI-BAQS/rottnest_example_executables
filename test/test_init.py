'''
    Black box test on circuit object creation
'''

import unittest
import rottnest_example_executables

base_tests = {} 
for cls in rottnest_example_executables.rottnest_executables: 
    def _wrap(*args, **kwargs):
        '''
            Simple instantiate and call
            using default arguments
        '''
        obj = cls()
        obj()
    name = "test_init_{}".format(cls.__name__)
    base_tests[name] = _wrap 
        

TestInit = type('base', (unittest.TestCase,), base_tests) 

if __name__ == '__main__':
    unittest.main()
