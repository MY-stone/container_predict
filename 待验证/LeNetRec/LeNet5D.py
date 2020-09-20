import torch
import torch.nn as nn


class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, stride=1),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1),
            nn.MaxPool2d(kernel_size=2)
        )
        self.fc1 = nn.Sequential(
            nn.Linear(in_features=6 * 6 * 16, out_features=120)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=120, out_features=84)
        )
        self.fc3 = nn.Sequential(
            nn.Linear(in_features=84, out_features=2)
        )

    def forward(self, input):
        conv1_output = self.conv1(input)  # [,1,36,36]--->(convolution)[,6,32,32]--->(pooling)[,6,16,16]
        conv2_output = self.conv2(conv1_output)  # [,6,16,16]--->(convolution)[,16,12,12]--->(pooling)[,16,6,6]
        conv2_output = conv2_output.view(-1, 6 * 6 * 16)  # 将[n,6,6,16]维度转化为[n,6*6*16]
        fc1_output = self.fc1(conv2_output)  # [n,576]--->[n,120]
        fc2_output = self.fc2(fc1_output)  # [n,120]-->[n,84]
        fc3_output = self.fc3(fc2_output)  # [n,84]-->[n,2]
        return fc3_output


# input1 = torch.rand([32, 1, 36, 36])
# model = LeNet()
# print(model)
# output = model(input1)