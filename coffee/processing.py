# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:38:43 2017

@author: arjan.groen
"""
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import numpy as np
import matplotlib.pyplot as plt
import dominate
from dominate.tags import *
import os

class coffee(object):
    
    def __init__(self,df,maxdims=50,docTitle="testcase",run=True):
        """
        input:
        output:
        """
        self.df = df
        self.len = self.df.shape[0]
        self.maxdims = maxdims
        self.doc = dominate.document(title=docTitle)
        self.name = docTitle
        self.collection = {}
        
        if run:
            self.run()
        
    def run(self):
        self.grind_columns()
        self.make()
        
    def place_cup(self):
        directory = self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    def milk(self,col,ax):   
        fig = ax.get_figure()
        figname = col + ".jpg"
        fig.savefig(figname)
        return figname
        
    def make_VC_table(self,col,maxDims=50):
        vc = self.collection[col]["valCounts"]
        print(vc.head())
        tbl = table()
        row1 = tr()
        th1 = th("Value")
        th2 = th("Frequency")
        row1 += th1
        row1 += th2
        tbl+=row1
        
        dims = min(maxDims,vc.shape[0])
        for i in range(dims):
            rowi = tr()
            tdi1 = td(vc.index[i])
            tdi2 = td(vc.loc[vc.index[i]])
            rowi += tdi1
            rowi += tdi2
            tbl += rowi
            
        return tbl
        
    def serve(self,col):
        # Get colSummary
        colSummary = self.collection[col]
        
        # Add Column Name
        self.doc+= h1(col)
        
        # Add plot
        self.doc+= h2("distribution of values")
        self.doc+= img(src=colSummary["plotfile"])
        
        # Add number of dimensions
        self.doc+= h2("unique values")
        text = "The number of unique values is: " + str(colSummary["n_dims"])
        self.doc+= p(text)
        
        # Add number of missing values
        self.doc+= h2("missing values")
        text = "The number of missing values is: " + str(colSummary["n_missing"])
        self.doc+= p(text)
        pct = 100*(colSummary["n_missing"]/self.len)
        text = "The percentage of missing values is: " + str(pct)
        self.doc+= p(text)
        
        # Add ValCounts
        table = self.make_VC_table(col)
        self.doc+= table

    def make(self):
        for key,value in self.collection.items():
            self.serve(key)

        with open(self.name +"/" + self.name+'.html', 'w',encoding='utf-8') as f:
            f.write(self.doc.render())
            
    def coffee_bar(self,col):
        colSummary = self.collection[col]
        plt.figure(figsize=(14,5))
        if colSummary["n_dims"] <= 50:
            ax = colSummary["valCounts"].plot(kind="bar")
        else:
            ax = colSummary["valCounts"][:25].plot(kind="bar")
        return ax    
        
    def grind_string(self,col):
        """
        input: column name from self.df which contains a string/object dtype
        output: analysis dictionary.
        """
        colSummary = {}
        series = self.df[col]
        colSummary["valCounts"] = series.value_counts(dropna=False)
        colSummary["n_dims"] = colSummary["valCounts"].shape[0]
        colSummary["n_missing"] = pd.isnull(series).sum()
        self.collection[col] = colSummary
        #if colSummary["n_dims"] <= 50:
        #    ax = colSummary["valCounts"].plot(kind="bar")
        #else:
        #    ax = colSummary["valCounts"][:10].plot(kind="bar")
        ax = self.coffee_bar(col)
        figname = self.milk(col,ax)
        plt.cla()
        colSummary["plotfile"] = figname
        #STORE RESULT
        self.collection[col] = colSummary

    def grind_numeric(self,col):
        """
        input: column name from self.df which contains a numeric dtype
        output: analysis dictionary.
        """        
        colSummary = {}
        series = self.df[col]
        colSummary["valCounts"] = series.value_counts(dropna=False)
        colSummary["n_dims"] = colSummary["valCounts"].shape[0]
        colSummary["n_missing"] = self.df[col].shape[0] - np.isfinite(series).sum()
        ax = series.hist(bins=20)
        self.milk(col,ax)
        plt.cla()        
        colSummary["plotfile"] = col + ".jpg"
        
        #STORE RESULT
        self.collection[col] = colSummary        
        
    def grind_columns(self):
        """
        input: pandas dataframe 
        output: html report for all columns
        """
        self.place_cup()
        for col in self.df.columns:
            if is_string_dtype(self.df[col]):
                self.grind_string(col)
            elif is_numeric_dtype(self.df[col]):
                self.grind_numeric(col)
            else:
                print("Unkown dtype for col: ",col)
                print("Dtype = ",self.df[col].dtype)
                
        
            
            
        
        
    