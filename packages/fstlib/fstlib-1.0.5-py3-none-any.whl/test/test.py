from fstlib import fstlib
import os

def test_savefst():
    import pandas as pd
    import numpy as np

    #path_s3 = "projects/I4CE/402.MLEVA/SIM2/I4CE_SIM2_EVA_WING_GWL_15.fst"
    
    df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'])

    fstlib.savefst(df2, "df2.fst")
    
    df = fstlib.readfst("df2.fst")
    
    assert (df.shape[0] ) > 1

    os.remove("df2.fst")
    
    