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
from shutil import copyfile
import checks
#df = pd.read_csv("testdata/football-events/events.csv",encoding="cp1252")


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
        with self.doc.head:
            link(rel='stylesheet', href='style.css')
        self.name = docTitle
        self.collection = {}
        
        if run:
            self.run()
        
    def run(self):
        self.grind_columns()
        self.make_doc()
        
    def make_dir(self):
        directory = self.name
        css = 'style.css'
        if not os.path.exists(directory):
            os.makedirs(directory)
        copyfile(css, directory + "/" + css)
        
    def save_fig(self,col,ax):   
        fig = ax.get_figure()
        figname = col + ".jpg"
        fig.savefig(self.name+"/"+figname)
        return figname
        
    def full_VC_table(self,col):
        vc = self.collection[col]["valCounts"]
        size = vc.shape[0]

        print(vc.head())
        tbl = table()
        row1 = tr()
        th1 = th("Value")
        th2 = th("Frequency")
        row1 += th1
        row1 += th2
        tbl+=row1
        
        self.doc += h2("Count of all distinct values")        
        for i in range(size):
            rowi = tr()
            tdi1 = td(vc.index[i])
            tdi2 = td(vc.loc[vc.index[i]])
            rowi += tdi1
            rowi += tdi2
            tbl += rowi
            
        return tbl
    
    def topN_VC_table(self,col,ascending=False,topSize=10):
        vc = self.collection[col]["valCounts"]
        vc = vc.sort_values(ascending=ascending)

        tbl = table()
        row1 = tr()
        th1 = th("Value")
        th2 = th("Frequency")
        row1 += th1
        row1 += th2
        tbl+=row1
              
        for i in range(topSize):
            rowi = tr()
            tdi1 = td(vc.index[i])
            tdi2 = td(vc.loc[vc.index[i]])
            rowi += tdi1
            rowi += tdi2
            tbl += rowi
            
        return tbl       
    
    def special_char_table(self,col):
        specChars = self.collection[col]["specialChars"]
        tbl = table()
        row1 = tr()
        th1 = th("Character")
        th2 = th("indices")
        row1 += th1
        row1 += th2
        tbl+=row1
        for key,value in specChars.items():
            rowi = tr()
            tdi1 = td(key)
            tdi2 = td(value)
            rowi += tdi1
            rowi += tdi2
            tbl += rowi      
            
        return tbl
            
        
    def make_doc_column(self,col,maxDims=30,topSize=10):
        # Get colSummary
        colSummary = self.collection[col]
        
        # Add Column Name
        self.doc+= h1("Column: " + col)
        self.doc+= h2("Datatype")
        self.doc+= p("The dtype is: " + colSummary["dtype"])
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
        if colSummary["n_dims"] <= maxDims:
            table = self.full_VC_table(col)
            self.doc+= table
        else:
            header2 = "Top " + str(topSize) + " (left) and bottom " + str(topSize) + " (right) value frequencies."
            
            table1 = self.topN_VC_table(col,ascending=False,topSize=topSize)
            table2 = self.topN_VC_table(col,ascending=True,topSize=topSize)
            self.doc+=h2(header2)
            self.doc+= table1
            self.doc+= table2
            
        # Add special Characters
        if colSummary["dtype"] == "object" and len(colSummary["specialChars"].values())>0:
            self.doc+=h2("Special characters found in the following indices:")
            table = self.special_char_table(col)
            self.doc+=table
            

    def make_doc(self):
        for key,value in self.collection.items():
            self.make_doc_column(key)

        with open(self.name +"/" + self.name+'.html', 'w',encoding='utf-8') as f:
            f.write(self.doc.render())
            
    def make_barChart(self,col):
        colSummary = self.collection[col]
        #plt.figure(figsize=(14,5))
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
        series = self.df[col]
        colSummary  = self.collection[col]
        colSummary["specialChars"] = checks.check_special_characters(series)
        colSummary["n_missing"] = pd.isnull(series).sum()
        self.collection[col] = colSummary
        plt.figure(figsize=(14,5))
        ax = self.make_barChart(col)
        figname = self.save_fig(col,ax)
        plt.cla()
        plt.close()
        colSummary["plotfile"] = figname
        #STORE RESULT
        self.collection[col] = colSummary

    def grind_numeric(self,col):
        """
        input: column name from self.df which contains a numeric dtype
        output: analysis dictionary.
        """        
        series = self.df[col]
        colSummary  = self.collection[col]
        colSummary["n_missing"] = self.df[col].shape[0] - np.isfinite(series).sum()
        plt.figure(figsize=(14,5))
        ax = series.hist(bins=20)
        self.save_fig(col,ax)
        plt.cla()      
        plt.close()
        colSummary["plotfile"] = col + ".jpg"
        #STORE RESULT
        self.collection[col] = colSummary        
        
    def grind_column(self,col):
        colSummary = {}
        series = self.df[col]
        colSummary["valCounts"] = series.value_counts(dropna=False)
        colSummary["n_dims"] = colSummary["valCounts"].shape[0]
        colSummary["dtype"] =    str(self.df[col].dtype)
        self.collection[col] = colSummary 
        if is_string_dtype(self.df[col]):
            self.grind_string(col)
        elif is_numeric_dtype(self.df[col]):
            self.grind_numeric(col)
        else:
            print("Unkown dtype for col: ",col)
            print("Dtype = ",self.df[col].dtype)                    
        
        
    def grind_columns(self):
        """
        input: pandas dataframe 
        output: html report for all columns
        """
        self.make_dir()
        for col in self.df.columns:
            print("Processing ",col)
            self.grind_column(col)
            

                
        
            
            
        
        
    