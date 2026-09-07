from dset import samples as spl
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader , Dataset

class Neuralnetwork(nn.Module): # the neural network class
    def __init__(self):
        super().__init__()
        self.ley1 = nn.Linear(1,4) # layer 1 -> 4
        self.ley2 = nn.Linear(4,1) # layer 4 -> 1

    def forward(self , x): # going forward in network
        # Using relu as a activition function
        x = self.ley1(x)
        x = torch.relu(x)
        x = self.ley2(x)
        return x

    def training(self):
        self.ds = DS()
        list_ = []
        self.samples = self.ds.dataloader()
        for x, y in self.samples:
            y_ = self.forward(x)
            loss = y - y_
            list_.append(loss)


class DS(Dataset): # for taining and handling samples
    def __init__(self):
        x, y = spl()
        self.dataset = TensorDataset(x, y)
        print(self.dataset[100])

    def __getitem__(self, index): # getting a sample by index
        return self.dataset[index]

    def __len__(self):
        return len(self.dataset)

    def dataloader(self , batch_size = 100): # batching samples
        return torch.utils.data.DataLoader(self.dataset , batch_size=batch_size , shuffle=True)

