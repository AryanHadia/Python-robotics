import torch
# saving samples in this file
def samples():
    x = torch.linspace(-10, 10, 20000).reshape(-1 , 1)
    y = x ** 2
    return x , y