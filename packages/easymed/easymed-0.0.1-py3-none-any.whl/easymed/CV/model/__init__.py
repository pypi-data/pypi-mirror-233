from typing import Type
import torch

def binary(tensor: Type[torch.Tensor], threshold: float=0.5) -> Type[torch.Tensor]:
    tensor[tensor >= threshold] = 1
    tensor[tensor < threshold] = 0
    return tensor.bool()