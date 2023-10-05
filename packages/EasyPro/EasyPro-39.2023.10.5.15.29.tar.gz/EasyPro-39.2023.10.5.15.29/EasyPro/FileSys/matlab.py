# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 13:06
# @Author  : Quanfa
# @Desc    : 
# region import
from torch import Tensor
# endregion

def save_mat(object, path, name) -> str:
    import numpy as np
    from scipy import io
    object = np.array(object)
    object = np.squeeze(object)
    mdic = {name: object}
    io.savemat(path, mdic)

    return path


def load_mat(path) -> Tensor:
    from scipy import io
    result = io.loadmat(path)
    r = Tensor(result[list(result.keys())[3]])
    return r

