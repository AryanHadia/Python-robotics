import torch
import torch.nn as nn
from torch.utils.data import Dataset , TensorDataset , DataLoader

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(1, 4)
        self.output = nn.Linear(4, 1)


    def forward(self, x):
        x = self.hidden(x)
        x = torch.relu(x)
        x = self.output(x)
        return x

    


class dataset(Dataset):
    def __init__(self):
        x = torch.linspace(-10 , 10 , 1000)
        y = x ** 2
        self.dataset_ = TensorDataset(x, y)
        self.dataloader_ = self.dataloader()
        print(self.dataset_)
        print(self.dataloader_)
        print(len(self))
        print(self[0])
    
    def __getitem__(self , index):
        return self.dataset_[index]

    
    def __len__(self):
        return len(self.dataset_)


    def dataloader(self , batch_size=100):
        return torch.utils.data.DataLoader(self.dataset_ , batch_size=batch_size , shuffle=True)
        

