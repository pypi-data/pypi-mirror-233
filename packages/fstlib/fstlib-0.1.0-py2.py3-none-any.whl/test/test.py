from fstlib import fstlib
import os

def test_fn_s3fdrd2():
    path_s3 = "projects/I4CE/402.MLEVA/SIM2/I4CE_SIM2_EVA_WING_GWL_15.fst"
    
    dteva = fstlib.fn_s3fdrd2(os.path.dirname(path_s3), 
               os.path.basename(path_s3))
    
    assert (dteva.shape[0] ) > 1
    

    
    