# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:48:52 2017

@author: arjan.groen
"""
import pandas as pd

def check_special_characters(series, chars = r'.,|/\!@#$&*(){}[]-'):
    charlist = [c for c in chars]
    charIndexDict = {}
    for c in charlist:
        indices = series[series==c].index.tolist()
        if len(indices) == 0:
            continue
        elif len(indices) > 10:
            first = indices[0]
            last = indices[-1]
            text = str(len(indices)) + " observations, the first on index: " + \
                str(first) + " and the last on index " + str(last)
        else:
            indices = [str(x) for x in indices]
            text = ",".join(indices)
        charIndexDict[c] = text
    return charIndexDict
        
        
    
    