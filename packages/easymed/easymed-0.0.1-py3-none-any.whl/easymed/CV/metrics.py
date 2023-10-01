from typing import Union
import numpy as np
import torch

def dice(a: Union[np.ndarray, torch.Tensor], b: Union[np.ndarray, torch.Tensor]) -> float:
    return 2 * (a & b).long().sum() / (a.long().sum() + b.long().sum())

def iou(a: Union[np.ndarray, torch.Tensor], b: Union[np.ndarray, torch.Tensor]) -> float:
    return (a & b).long().sum() / (a | b).long().sum()