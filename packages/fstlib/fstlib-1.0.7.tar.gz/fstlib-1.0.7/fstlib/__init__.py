from rpy2 import robjects
"""
fstlib.

A python wrapper to handle fst files.
"""
import os
from rpy2.robjects import pandas2ri 
os.environ['R_HOME'] =  os.popen("which R").read().strip()# Replace with the correct path to your installation R

import rpy2.robjects as robjects


__version__ = "0.1.0"
__author__ = 'Vhiny - Guilley MOMBO'
__credits__ = 'finres'
__all__ = [ 'fn_s3fdrd2',
            'readfst',
            'savefst'
            ]


print("initialiazing aws parameters ")

robjects.r('''
           
    library(fst)
    library(readr)
    library(aws.s3)
    library(data.table)
    
    s3_path <- "" #path on AWS for .fst files
    local_path_csv <- "" #local path for csv files
    
    if(grepl("local|home", Sys.info()["nodename"])) { 
  
        aws.localkey <- paste0('~/.ssh/',Sys.info()['user'],'_accessKeys.csv')
        aws.key <- suppressWarnings(read.csv(file = aws.localkey, header = T, sep = ","))
  
    } else {
  
        aws.localkey <- grep('_accessKeys.csv', list.files("~", full.names = T), value = T)
        aws.key <- suppressWarnings(read.csv(file = file.path("~/", basename(aws.localkey)), header = T, sep = ","))
  
    }
        
    Sys.setenv("AWS_ACCESS_KEY_ID" = as.character(aws.key$Access.key.ID),
           "AWS_SECRET_ACCESS_KEY" = as.character(aws.key$Secret.access.key),
           "AWS_DEFAULT_REGION" = "eu-west-3")
    
''')