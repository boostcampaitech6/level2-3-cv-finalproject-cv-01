from model import CNN5d, CNN20d
from dataset import StockDataset

import argparse
import torch
import numpy as np
import random
import torch.optim as optim
import torch
import torch.nn as nn
from importlib import import_module


def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


def train(args):
    seed_everything(args.seed)

    if args.window_size >= 15:
        model = CNN20d(args.window_size)
    else:
        model = CNN5d(args.window_size)
    

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    dataset = StockDataset(args.window_size, args.target_day, \
                           args.use_pickle, args.pickle_dir, \
                           args.transform_type, args.csv_dir)
    
    train_size = int(len(dataset)*(1-0.3))
    valid_size = len(dataset) - train_size

    train_set, valid_set = torch.utils.data.random_split(dataset, [train_size, valid_size])
    
    train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=32, shuffle=True)
    valid_loader = torch.utils.data.DataLoader(dataset=valid_set, batch_size=32, shuffle=True)

    criterion = nn.BCELoss().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.00001, weight_decay=0.01)
    

    n_epochs = 100
    early_stop_epoch = 95
    valid_loss_min = np.Inf # track change in validation loss
    train_loss_set = []
    valid_loss_set = []
    train_acc_set = []
    valid_acc_set = []
    invariant_epochs = 0
    savefile = 'sample.pth'


    for epoch_i in range(1, n_epochs+1):

        # keep track of training and validation loss 
        train_loss, train_acc = 0.0, 0.0
        valid_loss, valid_acc = 0.0, 0.0
        
        #### Model for training 
        model.train()
        for i, (data, target) in enumerate(train_loader):


            target = (1-target).unsqueeze(1) @ torch.LongTensor([1., 0.]).unsqueeze(1).T + target.unsqueeze(1) @ torch.LongTensor([0, 1]).unsqueeze(1).T
            target = target.to(torch.float32)

            data = data.to(device)
            target = target.to(device)
            
            # clear the gradients of all optimized variables
            optimizer.zero_grad()
            # forward pass: compute predicted outputs by passing inputs to the model
            output = model(data)
            # calculate the batch loss
            loss = criterion(output, target)
            # backward pass: compute gradient of the loss with respect to model parameters
            loss.backward()
            # perform a single optimization step (parameter update)
            optimizer.step()
            # update training loss
            train_loss += loss.item()*data.size(0)
            # update training acc
            train_acc += (output.argmax(1) == target.argmax(1)).sum()


        #### Model for validation
        model.eval()
        for i, (data, target) in enumerate(valid_loader):
            target = (1-target).unsqueeze(1) @ torch.LongTensor([1., 0.]).unsqueeze(1).T + target.unsqueeze(1) @ torch.LongTensor([0, 1]).unsqueeze(1).T
            target = target.to(torch.float32)

            
            # move tensors to GPU if CUDA is available
            data, target = data.to(device), target.to(device)
            # forward pass: compute predicted outputs by passing inputs to the model
            output = model(data)
            # calculate the batch loss
            loss = criterion(output, target)
            # update average validation loss 
            valid_loss += loss.item()*data.size(0)
            valid_acc += (output.argmax(1) == target.argmax(1)).sum()
        
        # Compute average loss
        train_loss = train_loss/len(train_loader.sampler)
        train_loss_set.append(train_loss)
        valid_loss = valid_loss/len(valid_loader.sampler)
        valid_loss_set.append(valid_loss)

        train_acc = train_acc/len(train_loader.sampler)
        train_acc_set.append(train_acc.cpu().numpy())
        valid_acc = valid_acc/len(valid_loader.sampler)
        valid_acc_set.append(valid_acc.cpu().numpy())
            
        print('Epoch: {} Training Loss: {:.6f} Validation Loss: {:.6f} Training Acc: {:.5f} Validation Acc: {:.5f}'.format(epoch_i, train_loss, valid_loss, train_acc, valid_acc))
        
        # if validation loss gets smaller, save the model
        if valid_loss <= valid_loss_min:
            print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(valid_loss_min,valid_loss))
            valid_loss_min = valid_loss
            invariant_epochs = 0
            torch.save({
                'epoch': epoch_i,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict()
                }, savefile)
        else:
            invariant_epochs = invariant_epochs + 1
        
        if invariant_epochs >= early_stop_epoch:
            print(f"Early Stop at Epoch [{epoch_i}]: Performance hasn't enhanced for {early_stop_epoch} epochs")
            break



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--seed", type=int, default=42, help="random seed (default: 42)")

    # dataset
    parser.add_argument("--window_size", type=int, default=20, help="window size : 5 ~ 30")
    parser.add_argument("--target_day", type=int, default=1, help="target_day : 1 ~ 30")
    parser.add_argument("--transform_type", type=str, default="rasterize", help="stock data to image type")
    parser.add_argument("--pickle_dir", type=str, default='./rasterize_pkl', help="pickle directory path")
    parser.add_argument("--use_pickle", type=bool, default=False, help="use pickle data or not")
    parser.add_argument("--csv_dir", type=str, default='./stock_csv', help="csv directory path")

    args = parser.parse_args()

    train(args)
