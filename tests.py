#!/usr/bin/env 
#-*- coding: utf-8 -*-

import unittest
import drunk

class DrunkTest(unittest.TestCase):
    
    def setUp(self):
        self.start_position = 2
        self.prob_frw = 1/3
        self.testscenario = [1, 1, -1, 1, 1]
        self.n = 4

    def testCalcProb(self):
        self.assertEqual(drunk.calc_prob(self.testscenario,self.prob_frw),0.06584362139917697)

    def testWalk(self):
        self.assertEqual(drunk.walk(self.n),0.8888888888888888)

if __name__ == '__main__':
    unittest.main()    