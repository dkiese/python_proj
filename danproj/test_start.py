'''
Created on Apr 11, 2021

@author: danki
'''
import unittest
import json


class Test(unittest.TestCase):


    # comparing all the elements of a two json list. Hardcoded the file paths, only seems to work if the courses are ordered the same
    def test_compareOutput(self):
        
        a = ""
        with open("output.json", "r") as myfile:
            a = myfile.read()
        a = json.loads(a)
        
        
        b = ""
        with open("output1.json", "r") as myfile:
            b = myfile.read()
        b = json.loads(b)
        
        print(sorted(a.items()))
        print(sorted(b.items()))
        print(a == b) 
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()