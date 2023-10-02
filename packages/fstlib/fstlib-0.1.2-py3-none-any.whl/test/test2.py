from  fstlib import fstlib
import os
#readfst("~/Desktop/test.fst")

##  read from AWS s3
path_s3 = "projects/I4CE/402.MLEVA/SIM2/I4CE_SIM2_EVA_WING_GWL_15.fst"
dteva = fstlib.fn_s3fdrd2(os.path.dirname(path_s3), 
               os.path.basename(path_s3))



## save locally fst
fstlib.savefst(dteva, "~/Desktop/test.fst")

# read locally fst
dteva2 = fstlib.readfst("~/Desktop/testfunc.fst")
