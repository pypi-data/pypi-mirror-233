from rpy2 import robjects
"""
fstlib.

A python wrapper to handle fst files.
"""
import os
from rpy2.robjects import pandas2ri 
os.environ['R_HOME'] =  os.popen("which R").read().strip()# Replace with the correct path to your installation R

import rpy2.robjects as robjects



## import library 

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
           
## read more about this package to converte R variable to Python one and inverse
def fn_s3fdrd2(prefix, name_file, layer = None, colnames = None):

    '''
    Read data frames from and to a fast-storage ('fst') file from S3. 
    
    Allows for compression and (file level) random access of stored data, 
    
    even for compressed datasets. Multiple threads are used to obtain high 
    
    (de-)serialization speeds but all background threads are re-joined before 
    
    'read_fst' return (reads and writes are stable). 
    
    When using a 'data.table' object for 'x', the key (if any) is preserved,
     
    allowing storage of sorted data.
    
    --
    Input :

        prefix : s3 dirname of the file

        name_file : name of the file 

    --
    Output
        data : A python dataframe .

    '''
    
    code = f'''
    
        prefix <- "{prefix}"
        name.file <- "{name_file}"
        layer <- {"NULL" if layer is None else layer}
        colnames <- {"NULL" if colnames is None else colnames}

        prefix <- gsub("s3://finres/", "", prefix)
        ls.file <- file.path(prefix, name.file)
        nm.file <- paste0("~/", basename(ls.file))
        save_object(paste0("s3://finres/", ls.file, sep = ""),
                    file = nm.file)
        vc.sfx <-  last(unlist(strsplit(nm.file, "[.]")))
        
        if(vc.sfx == "fst"){{ dt <- read_fst(path = nm.file, as.data.table = TRUE) }}
        
        rm(ls.file, nm.file, vc.sfx)
            
        dt
        
    '''
    
    data = robjects.r(code)
    data = pandas2ri.rpy2py_dataframe(robjects.DataFrame(data))
    
    
    return data



def readfst(file_name):

    '''
    Read data frames from and to a fast-storage ('fst') file. 
    
    Allows for compression and (file level) random access of stored data, 
    
    even for compressed datasets. Multiple threads are used to obtain high 
    
    (de-)serialization speeds but all background threads are re-joined before 
    
    'read_fst' return (reads and writes are stable). 
    
    When using a 'data.table' object for 'x', the key (if any) is preserved,
     
    allowing storage of sorted data.
    
    --
    Input :

        data :a data frame to write to disk

        file_name : path to fst file
        
        compress : value in the range 0 to 100, indicating the amount of compression to use. Lower values mean larger file sizes. 
                   The default compression is set to 50.

    --
    Output
        Nothing.

    '''
    
    robjects.r.assign("nm.file ", file_name)

    code = f'''

        #nm.file <- "{file_name}"

         dt <- read_fst(path = nm.file, as.data.table = TRUE)
            
        dt
        
    '''
    
    data = robjects.r(code)
    data = pandas2ri.rpy2py_dataframe(robjects.DataFrame(data))
    
    
    return data

 

def write_fst(data, file_name, compress = 50, uniform_encoding = True):

    '''
    Write data frames from and to a fast-storage ('fst') file. 
    
    Allows for compression and (file level) random access of stored data, 
    
    even for compressed datasets. Multiple threads are used to obtain high 
    
    (de-)serialization speeds but all background threads are re-joined before 
    
    'write_fst' return (reads and writes are stable). 
    
    When using a 'data.table' object for 'x', the key (if any) is preserved,
     
    allowing storage of sorted data.

    --
    Input :

        data :a data frame to write to disk

        file_name : path to fst file
        
        compress : value in the range 0 to 100, indicating the amount of compression to use. Lower values mean larger file sizes. 
                   The default compression is set to 50.

    --
    Output
        Nothing.

    
    '''
        
    
    with (robjects.default_converter + pandas2ri.converter).context():
        
        r_dataframe = robjects.conversion.get_conversion().py2rpy(data)

        #file_name = "~/Desktop/test.fst"

        robjects.r.assign("data", data)

        code = f'''
            
            nm.file <- "{file_name}"
            compress <- {compress}
            uniform_encoding <- {"TRUE" if uniform_encoding else "FALSE"} 
            write_fst(data, path = nm.file, compress = compress, uniform_encoding = uniform_encoding) 
            
            '''
        
        robjects.r(code)
    
        print("done")