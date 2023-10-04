from torchvision import transforms
import torch.utils.data as data
import torch
import glob
import os
from PIL import Image
import torchvision
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import DataLoader

class load_dataset(DataLoader):
    def __init__(self, batch_size, system_size, datapath, num_workers=8):
        super(DataLoader, self).__init__()
        self.transform = transforms.Compose([transforms.Resize((system_size),interpolation=2),transforms.ToTensor()])
        self.bs = batch_size
        self.datapath = datapath
        self.padding = 0
        self.num_workers = num_workers
    def MNIST(self):
        train_dataset = torchvision.datasets.MNIST(self.datapath, train=True, transform=self.transform, download=True)
        val_dataset = torchvision.datasets.MNIST(self.datapath, train=False, transform=self.transform, download=True)
        train_dataloader = DataLoader(dataset=train_dataset, batch_size=self.bs, num_workers=self.num_workers, shuffle=True, pin_memory=True)
        val_dataloader = DataLoader(dataset=val_dataset, batch_size=self.bs, num_workers=self.num_workers, shuffle=False, pin_memory=True)
        return train_dataloader, val_dataloader

    def FMNIST(self):
        train_dataset = torchvision.datasets.FashionMNIST(self.datapath, train=True, transform=self.transform, download=True)
        val_dataset = torchvision.datasets.FashionMNIST(self.datapath, train=False, transform=self.transform, download=True)
        train_dataloader = DataLoader(dataset=train_dataset, batch_size=self.bs, num_workers=self.num_workers, shuffle=True, pin_memory=True)
        val_dataloader = DataLoader(dataset=val_dataset, batch_size=self.bs, num_workers=self.num_workers, shuffle=False, pin_memory=True)
        return train_dataloader, val_dataloader

