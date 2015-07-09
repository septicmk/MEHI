################################
# Author   : septicmk
# Date     : 2015年07月07日 星期二 17时02分21秒
# FileName : MEHI_s_tracking.py
################################

import numpy as np
import pulp
import math
import itertools
from MEHI_s_global import *
from MEHI_s_common import *

class Tracker:
    
    def likehood(self, vecA, vecB):
        vecA = np.array(vecA)
        vecB = np.array(vecB)
        num = float(vecA.T *vecB)
        denom = np.linalg.norm(vecA) * np.linalg.norm(vecB)
        cos = num / denom
        sim = .5 + .5*cos
        return sim

    def add_hypothesis(self, cur_df, aft_df):
           pass

    def integer_programming(self, cur_df, aft_df):
        possible_events = [tuple(x) for x in itertools.product(cur_df.index, aft_df.index)]
        #possible_events = [x for x in self.add_hypothesis(cur_df, aft_df)]
        x = pulp.LpVariable.dicts('event', possible_events, 
                            lowBound = 0,
                            upBound = 1,
                            cat = pulp.LpInteger)
        prob = pulp.LpProblem("tracking", pulp.LpMaximize)
        prob += sum([2 * likehood(event) * x[event] for event in possible_events])
        for cell in cur_df.index:
            prob += sum(x[event] for event in possible_events if cell == event[0]) <= 1
        for cell in aft_df.index:
            prob += sum(x[event] for event in possible_events if cell in event[1:]) <= 1
        prob.solve()
        links = []
        for event in possible_events:
            if x[event].value == 1.0:
                links.append(event)
        return links

    def filter1(self, cur_df, aft_df, links):
        tmp = [x[1] for x in links]
        bad_cell = []
        for cell in aft_df.index:
            if cell not in tmp:
                bad_cell.append(cell)
                aft_df = aft_df.drop(cell)
        return aft_df, bad_cell

    def filter2(self, cur_df, aft_df, links):
        
                
        


        


