# Program to collect error in a Python code and send to a DB
# Written by Ezgi DEMIR, PhD. Industrial Engineering

import sqlite3 as sql
from pylint import epylint
import datetime
import getpass
import platform
#import re

#gathering error as a dictionary

# Linting Errors 
def define_error(filename):
    options = '--errors-only'  # all messages will be shown
    pylint_stdout, pylint_stderr = epylint.py_run(filename+ ' ' + options, return_std=True)
    #db_dict={} #Creating an Open Dictionary
    
    #Finding the keyword 'error'
    #keyword=re.compile('error')
    
    #obtaining the index numbers of string list containing the keywords
    #index=[]
    
    #Filtering process of pylint stdout
    explanation=pylint_stdout.getvalue()
    explanation=explanation.replace('(','')
    explanation=explanation.replace(')','')
    explanation=explanation.replace(':',' ')
    explanation=explanation.replace('  ',' ')
    explanation=explanation.replace(',','')   
    
    #Splitting the sentence into a list of string arrays
    s2=explanation.split()    
    s2=explanation.split(filename)    
    
    #Filtering Result List
    s2=s2[1:]
    
    return s2

       






