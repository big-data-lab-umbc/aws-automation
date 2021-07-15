# For Dataset information, please refer to Dataset/Result section of the paper 
# "Deep Multi-Sensor Domain Adaptation on Active and Passive Satellite Remote Sensing Data" at 
# http://mason.gmu.edu/~lzhao9/venues/DeepSpatial2020/papers/DeepSpatial2020_paper_14_camera_ready.pdf 

# For GPU computing, latency per epoch is around 13 sec.
# For CPU computing, latency per epoch is around 26 sec.

import sys

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import numpy as np
import torch

if len(sys.argv) != 2:
    print("Usage: DistributedDL.py <gpu or cpu>", file=sys.stderr)
    sys.exit(-1)
_device = sys.argv[1]

if torch.cuda.is_available() and _device == "gpu":
    print("torch.cuda.is_available:",torch.cuda.is_available())
else:
    _device = "cpu"


data = np.load('./data/train10.npz')

# Active dataset: Calipso (represented as X_s [source domain], or X_c [calipso] in the code), 
# Passive Dataset: VIRRS  (represented as X_t [target domain], or X_c [virrs] in the code), 
# load common data, please refer to the paper above for the common attributes 
latlon = data['latlon']
iff = data['iff']

# Load viirs data 
X_v = data['viirs']
Y_v = data['label']
print ('X_v shape:')
print (X_v.shape)

# Load calipso data 
X_c = data['calipso']
Y_c = data['label']
print ('X_c shape:')
print (X_c.shape)

inds_v,vals_v = np.where(Y_v>0)
Y_v = Y_v[inds_v]
X_v = X_v[inds_v]
print ('X_v')
print (X_v)

inds_c,vals_c = np.where(Y_c>0)
Y_c = Y_c[inds_c]
X_c = X_c[inds_c]
print ('X_c')
print (X_c)

# process common data
Latlon = latlon[inds_v]
Iff = iff[inds_v]

print('original X_v: ', X_v.shape)
rows = np.where((X_v[:,0] >= 0) & (X_v[:,0] <= 83) & (X_v[:,15] > 100) & (X_v[:,15] < 400) & (X_v[:,16] > 100) & (X_v[:,16] < 400) & (X_v[:,17] > 100) & (X_v[:,17] < 400) & (X_v[:,18] > 100) & (X_v[:,18] < 400) & (X_v[:,19] > 100) & (X_v[:,19] < 400) & (X_v[:,10] > 0))
print("rows:", rows)
print("rows.shape:", len(rows))

Latlon = Latlon[rows]
Iff = Iff[rows]

Y_v = Y_v[rows]
X_v = X_v[rows]

Y_c = Y_c[rows]
X_c = X_c[rows]

print('after SZA X_v: ', X_v.shape)
print('after SZA X_c: ', X_c.shape)

#concanate common data
# X_v = np.concatenate((X_v, Latlon, Iff), axis=1)
X_c = np.concatenate((X_c, Latlon, Iff), axis=1)
print (X_v.shape)
print (X_c.shape)

X_v = np.nan_to_num(X_v)
X_c = np.nan_to_num(X_c)

# combine data and split latter to define ground truth for MLR
n1=20
n2=25
X=np.concatenate((X_v, X_c), axis=1)
Y=Y_v
print (X.shape)
print (Y_v)
x_train, x_valid, y_train, y_valid = train_test_split(X, Y,
                                                    test_size=0.3,
                                                    random_state=0,
                                                    stratify=Y)

# x_valid, x_test, y_valid, y_test = train_test_split(x_temp, y_temp,
#                                                     test_size=0.5,
#                                                     random_state=0,
#                                                     stratify=y_temp)

# feature scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
x_train=sc_X.fit_transform(x_train)
x_valid=sc_X.transform(x_valid)
# x_test=sc_X.fit_transform(x_test)

x_train_v = x_train[:, 0:20]
x_train_c = x_train[:, 20:45]
x_train_comm = x_train[:, 45:51]
x_train_src = x_train[:, 20:51]

print(x_train_v.shape)
print(x_train_c.shape)
print(x_train_comm.shape)
print(x_train_src.shape)
print(y_train.shape)

x_valid_v = x_valid[:, 0:20]
x_valid_c = x_valid[:, 20:45]
x_valid_comm = x_valid[:, 45:51]

print(x_valid_v.shape)
print(x_valid_c.shape)
print(x_valid_comm.shape)

# add the common attributes into the viirs dataset
x_train_pt = np.concatenate((x_train_v, x_train_comm),axis=1)
x_valid_pt = np.concatenate((x_valid_v, x_valid_comm),axis=1)

data_test = np.load('./data/test_142_day.npz')

passive =1

# process the test data
#load common data
latlon_test = data_test['latlon']
iff_test = data_test['iff']

# if passive ==1:
x_t_test = data_test['viirs']
y_t_test = data_test['label']
# else:
x_s_test = data_test['calipso']
y_s_test = data_test['label']
    
inds_test,vals_test = np.where(y_t_test>0)

# process common data
Latlon_test = latlon_test[inds_test]
Iff_test = iff_test[inds_test]

Y_t_test = y_t_test[inds_test]
X_t_test = x_t_test[inds_test]

Y_s_test = y_s_test[inds_test]
X_s_test = x_s_test[inds_test]

# 0 =< SZA <= 83
# Feature engineering from Chenxi's paper 
print('original X_t_test: ', X_t_test.shape)
rows_test = np.where((X_t_test[:,0] >= 0) & (X_t_test[:,0] <= 83) & (X_t_test[:,15] > 100) & (X_t_test[:,15] < 400) & (X_t_test[:,16] > 100) & (X_t_test[:,16] < 400) & (X_t_test[:,17] > 100) & (X_t_test[:,17] < 400) & (X_t_test[:,18] > 100) & (X_t_test[:,18] < 400) & (X_t_test[:,19] > 100) & (X_t_test[:,19] < 400) & (X_t_test[:,10] > 0))
print("rows_test:", rows_test)
print("rows_test.shape:", len(rows_test))

Latlon_test = Latlon_test[rows_test]
Iff_test = Iff_test[rows_test]

Y_t_test = Y_t_test[rows_test]
X_t_test = X_t_test[rows_test]

Y_s_test = Y_s_test[rows_test]
X_s_test = X_s_test[rows_test]

X_s_test = np.nan_to_num(X_s_test)
X_t_test = np.nan_to_num(X_t_test)

print('after SZA X_t_test: ', X_t_test.shape)
print('after SZA X_s_test: ', X_s_test.shape)

#concanate common data
# X_t_test = np.concatenate((X_t_test, Latlon_test, Iff_test), axis=1)
X_s_test = np.concatenate((X_s_test, Latlon_test, Iff_test), axis=1)

print (X_s_test.shape)
print (X_t_test.shape)

X_test=np.concatenate((X_t_test, X_s_test), axis=1)

# apply the feature scalar to testing data
x_test2=sc_X.transform(X_test)

X_t_test = x_test2[:, 0:20]
x_test_c2 = x_test2[:, 20:45]
x_test_comm2 = x_test2[:, 45:51]

x_test_pt_test = np.concatenate((X_t_test, x_test_comm2),axis=1)
print(x_test_pt_test.shape)

# Set random seed for reproducibility.
np.random.seed(131254)
import torch

torch.manual_seed(1)  # Set seed for reproducibility.

# pytorch mlp for multiclass classification
from numpy import vstack
from numpy import argmax
from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from torch import Tensor
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Softmax
from torch.nn import Module
from torch.nn import Dropout
from torch.nn import BatchNorm1d
from torch.optim import SGD,RMSprop,Adam
from torch.nn import CrossEntropyLoss
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_
import torch

# Horovod: adjust number of epochs based on number of GPUs.
n_epochs = 25
lambda_ = 0.001
NUM = 26
# DIFFERECE_COL = 5
BATCH_SIZE = 1024

# dataset definition, create dataset for torch data loader 
class CSVDataset(Dataset):
    # load the dataset
    def __init__(self, X1, Y1):

        self.X=X1
        self.y=Y1
        print("self.X before fit_transform")
        print(self.X)
        print("self.y before fit_transform")
        print(self.y)
        self.X = self.X.astype('float32')
        # label encode target and ensure the values are floats
        self.y = LabelEncoder().fit_transform(self.y)
        print("self.X before fit_transform")
        print(self.X)
        print("self.y after fit_transform")
        print(self.y)

    # number of rows in the dataset
    def __len__(self):
        return len(self.X)

    # get a row at an index
    def __getitem__(self, idx):
        return [self.X[idx], self.y[idx]]

    # get indexes for train and test rows
    def get_splits(self, n_test=0.33):
        # determine sizes
        test_size = round(n_test * len(self.X))
        train_size = len(self.X) - test_size
        # calculate the split
        return random_split(self, [train_size, test_size])

# DL model definition in torch 
class MLP(Module):
    # define model elements
    def __init__(self, n_inputs):
        super(MLP, self).__init__()
        # # input to very beginning hidden layer
        self.hidden = Linear(n_inputs, 128)
        kaiming_uniform_(self.hidden.weight, nonlinearity='relu')
        self.act = ReLU()
        # # input to beginning hidden layer
        self.hidden0 = Linear(128, 256)
        kaiming_uniform_(self.hidden0.weight, nonlinearity='relu')
        self.act0 = ReLU()
        # input to first hidden layer
        self.hidden1 = Linear(256, 128)
        kaiming_uniform_(self.hidden1.weight, nonlinearity='relu')
        self.act1 = ReLU()
        # second hidden layer
        self.hidden2 = Linear(128, 64)
        kaiming_uniform_(self.hidden2.weight, nonlinearity='relu')
        self.act2 = ReLU()
        # third hidden layer and output
        self.hidden3 = Linear(64, 6)
        xavier_uniform_(self.hidden3.weight)
        self.act3 = Softmax(dim=1)
        self.dropout = Dropout(p=0.5)
        self.batchnorm = BatchNorm1d(128)
        self.batchnorm0 = BatchNorm1d(256)
        self.batchnorm1 = BatchNorm1d(128)
        self.batchnorm2 = BatchNorm1d(64)

    # forward propagate input
    def forward(self, X):
        # # input to very first hidden layer
        X = self.hidden(X)
        X = self.batchnorm(X)
        X = self.act(X)
        X = self.dropout(X)
        # input to first hidden layer
        X = self.hidden0(X)
        X = self.batchnorm0(X)
        X = self.act0(X)
        X = self.dropout(X)
        # input to first hidden layer
        X = self.hidden1(X)
        X = self.batchnorm1(X)
        X = self.act1(X)
        X = self.dropout(X)
        # second hidden layer
        X = self.hidden2(X)
        X = self.batchnorm2(X)
        X = self.act2(X)
        X = self.dropout(X)
        # output layer
        X = self.hidden3(X)
        X = self.act3(X)
        return X

# Create data loader for training 
# prepare the dataset - random split within a dataset
def prepare_data(X2_train, Y2_train, X2_test, Y2_test):
    # load the train dataset
    train = CSVDataset(X2_train, Y2_train)
    # load the test dataset
    test = CSVDataset(X2_test, Y2_test)
    # prepare data loaders
    train_dl = DataLoader(train, batch_size=BATCH_SIZE, shuffle=True)
    test_dl = DataLoader(test, batch_size=BATCH_SIZE, shuffle=True)
    return train_dl, test_dl


aggre_losses = []
aggre_train_acc = []
aggre_test_acc = []
aggre_train_tgt_acc = []
import time

# train the model
def train_model(train_dl, test_dl, model,device):

    # define the optimization
    criterion = CrossEntropyLoss()
    # Horovod: adjust learning rate based on number of GPUs.
    optimizer = RMSprop(model.parameters(), lr=0.001)

    if device == "gpu":
      model = model.cuda()

    # enumerate epochs
    j = 0
    for epoch in range(n_epochs):
        t1=time.time()
        j += 1
        # enumerate mini batches
        train_steps = len(train_dl)
        print("train_steps:", train_steps)
        epoch_loss = 0
        for i, (inputs, targets) in enumerate(train_dl):
            # clear the gradients
            optimizer.zero_grad()
            # compute the model output
            if device == "gpu":
                inputs = inputs.to(device)
                targets = targets.to(device)
            yhat = model(inputs)
            # print("epoch", 1)
            # print("yhat")
            # print(yhat.shape)
            # print(yhat)
            # print("targets")
            # print(targets.shape)
            # print(targets)
            # calculate loss
            loss = criterion(yhat, targets)
            epoch_loss += loss
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()
        print('Train ith Epoch %d result:' % epoch)
        # calculate train accuracy
        train_acc = evaluate_model(train_dl, model, device)
        aggre_train_acc.append(train_acc)
        print('train_acc: %.3f' % train_acc)

        # calculate test accuracy
        test_acc = evaluate_model(test_dl, model, device)
        aggre_test_acc.append(test_acc)
        print('test_acc: %.3f' % test_acc)

        epoch_loss = epoch_loss / train_steps
        aggre_losses.append(epoch_loss)
        t2=time.time()
        if device == "gpu":
            print(f'[GPU computing] epoch: {j:3}, loss: {epoch_loss.item():6.4f}, time(sec) taken: ',round((t2 - t1), 2))
        else:
            print(f'[CPU computing] epoch: {j:3}, loss: {epoch_loss.item():6.4f}, time(sec) taken: ',round((t2 - t1), 2))

# evaluate the model
def evaluate_model(test_dl, model, device):
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(test_dl):
        if device == "gpu":
            inputs = inputs.to(device)
            targets = targets.to(device)

        # evaluate the model on the test set
        with torch.no_grad():
          yhat = model(inputs)
        # retrieve numpy array
        if device == "gpu":
            yhat = yhat.detach().cpu().numpy()
            actual = targets.cpu().numpy()
        else:
            yhat = yhat.detach().numpy()
            actual = targets.numpy()
        # convert to class labels
        yhat = argmax(yhat, axis=1)
        # reshape for stacking
        actual = actual.reshape((len(actual), 1))
        yhat = yhat.reshape((len(yhat), 1))
        # store
        predictions.append(yhat)
        actuals.append(actual)
    predictions, actuals = vstack(predictions), vstack(actuals)
    # calculate accuracy
    acc = accuracy_score(actuals, predictions)
    return acc

# make a class prediction for one row of data
def predict(row, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat


X_t = x_train_pt
Y_t = y_train

X_t_test = x_test_pt_test
Y_t_test = Y_s_test


train_tgt, test_tgt = prepare_data(X_t, Y_t, X_t_test, Y_t_test)
print("train_tgt")
print(train_tgt)
print(len(train_tgt.dataset))
print("test_tgt")
print(test_tgt)
print(len(test_tgt.dataset))
# define the network
model = MLP(NUM)
# train the model, this is a simple MLP model training and testing on Virrs (target) dataset. 
train_model(train_tgt, test_tgt, model, _device)

# evaluate the model
acc = evaluate_model(test_tgt, model, _device)
print('Accuracy: %.3f' % acc)

