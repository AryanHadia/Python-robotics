from dset import samples as spl
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader , Dataset

class Neuralnetwork(nn.Module): # the neural network class
    def __init__(self):
        super().__init__()
        self.ley1 = nn.Linear(1,10) # layer 1 -> 6
        self.ley2 = nn.Linear(10,1) # layer 6 -> 1

    def forward(self , x): # going forward in network
        # Using relu as a activition function
        x = self.ley1(x)
        x = torch.relu(x)
        x = self.ley2(x)
        return x

    def training_(self):
        self.ds = DS()
        self.samples = self.ds.dataloader()
        print(f"weight1 :{self.ley1.weight}")
        optimizer = torch.optim.SGD(self.parameters() , lr=0.001)
        for epoch in range (1,201):
            list_ = []
            for x, y in self.samples:
                y_ = self.forward(x)
                loss_fn = nn.MSELoss()
                loss = loss_fn(y_, y)
                print(loss)
                list_.append(loss)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            lss = 0
            for ls in list_:
                lss += ls
            print(f"weight2 :{self.ley1.weight}")
            print(f"epoch{epoch}: {lss/len(list_)}")

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
model = Neuralnetwork()
model.training_()
X_test = torch.tensor([[2.0],[3.0],[5.0]])
print("_____________________________")
with torch.no_grad():
    y_predict = model(X_test)

print(f"predict: {y_predict}")
