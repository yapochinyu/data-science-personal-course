import pandas as pd
import numpy as np


def compare_semantics() -> dict:
    s = pd.Series([1.0, np.nan, 5.0])
    s2 = pd.Series([1, pd.NA, 5], dtype='Int64')
    
    nan_gt = s > 2
    nan_lt = s < 2
    nan_eq = s == 2
    na_gt = s2 > 2

    result = {
        'nan_gt':nan_gt[1],
        'nan_lt':nan_lt[1],
        'nan_eq':nan_eq[1],
        'na_gt':na_gt[1]
    }
    
    return result

if __name__ == '__main__':
    dictionary = compare_semantics()
    print(dictionary)
    assert dictionary['nan_gt'] == False
    assert dictionary['nan_lt'] == False
    assert dictionary['nan_eq'] == False
    assert dictionary['na_gt'] is pd.NA
    