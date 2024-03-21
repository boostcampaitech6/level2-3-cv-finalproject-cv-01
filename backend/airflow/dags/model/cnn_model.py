from collections import OrderedDict
import torch
import torch.nn as nn

class CNN20d(nn.Module):
    # Input: [N, (1), 64, 60]; Output: [N, 2]
    # Three Convolution Blocks
    
    def init_weights(self, m):
        if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)
    
    def __init__(self):
        super(CNN20d, self).__init__()
        self.conv1 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(1, 64, (5, 3), padding=(3, 1), stride=(3, 1), dilation=(2, 1))), # output size: [N, 64, 21, 60]
            ('BN', nn.BatchNorm2d(64, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 64, 10, 60]
        ]))
        self.conv1 = self.conv1.apply(self.init_weights)
        
        self.conv2 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(64, 128, (5, 3), padding=(3, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 128, 12, 60]
            ('BN', nn.BatchNorm2d(128, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 128, 6, 60]
        ]))
        self.conv2 = self.conv2.apply(self.init_weights)
        
        self.conv3 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(128, 256, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 256, 6, 60]
            ('BN', nn.BatchNorm2d(256, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 256, 3, 60]
        ]))
        self.conv3 = self.conv3.apply(self.init_weights)

        self.DropOut = nn.Dropout(p=0.5)
        self.FC = nn.Linear(46080, 2)
        self.init_weights(self.FC)
        self.Softmax = nn.Softmax(dim=1)

    def forward(self, x): # input: [N, 64, 60]
        x = x.unsqueeze(1).to(torch.float32)   # output size: [N, 1, 64, 60]
        x = self.conv1(x) # output size: [N, 64, 10, 60]
        x = self.conv2(x) # output size: [N, 128, 6, 60]
        x = self.conv3(x) # output size: [N, 256, 3, 60]
        x = self.DropOut(x.view(x.shape[0], -1))
        x = self.FC(x) # output size: [N, 2]
        x = self.Softmax(x)
        
        return x
    

def get_cnn_model(day):
    model = CNN20d()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load(f'./dags/model/weight/I20R{day}_OHLC.tar',map_location=torch.device(device))
    model.load_state_dict(state_dict['model_state_dict'])
    return model