from torch import nn


# 定义我们需要用到的网络模型。采用LeNet5 双层卷积神经网络模型。


# class LeNet5(nn.Module):
#     def __init__(self):
#         super(LeNet5, self).__init__()
#         self.conv1 = nn.Sequential(
#             nn.Conv2d(  # (1, 36, 36) 我们输入的图片为36*36通道为1. 如果我们输入其他尺寸的图片，需要修改每一层输出的大小。
#                 in_channels=1,  # 输入通道数为1
#                 out_channels=6,  # 输出通道数为6个特征层
#                 kernel_size=5,  # 卷积核大小5*5
#                 stride=1,  # 步长为1
#                 padding=0  # 不填充
#             ),  # ->(6, 32, 32) 卷积核大小为5. 卷积核扫描过后，长宽各减少4.
#             nn.ReLU(),  # 激活函数
#             nn.AvgPool2d(kernel_size=2)  # ->(6, 16, 16) 经过一个平均池化层，下采样卷积核2*2.长宽各缩小一倍。
#         )
#         self.conv2 = nn.Sequential(  # 第二层卷积层
#             nn.Conv2d(6, 16, 5, 1, 0),  # (16, 12, 12) 参数类型跟第一层一样，内容修改为输出16个特征层。长宽继续减小4.
#             nn.ReLU(),  # 激活函数
#             nn.AvgPool2d(2)              # (16, 6, 6) 再经过一个2*2的平均池化层，下采样一倍。输出16通道，6*6特征图。
#         )
#         self.out = nn.Sequential(   # 输出层
#             nn.Linear(16 * 6 * 6, 120),
#             nn.ReLU(),
#             nn.Linear(120, 84),
#             nn.ReLU(),
#             nn.Linear(84, 36),  # 全连接，最终输出我们需要的分类数。
#         )
class LeNet5(nn.Module):
    def __init__(self):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(  # (1, 36, 36) 我们输入的图片为36*36通道为1. 如果我们输入其他尺寸的图片，需要修改每一层输出的大小。
                in_channels=1,  # 输入通道数为1
                out_channels=6,  # 输出通道数为6个特征层
                kernel_size=5,  # 卷积核大小5*5
                stride=1,  # 步长为1
                padding=0  # 不填充
            ),  # ->(6, 32, 32) 卷积核大小为5.
            nn.ReLU(),  # 激活函数
            nn.MaxPool2d(kernel_size=2)  # ->(6, 16, 16) 经过一个最大池化层，下采样卷积核2*2.长宽各缩小一倍。
        )
        self.conv2 = nn.Sequential(  # 第二层卷积层
            nn.Conv2d(6, 16, 3, 1, 0),  # (16, 14, 14) 内容修改为输出16个特征层。长宽减小2.
            nn.ReLU(),  # 激活函数
            nn.MaxPool2d(2)              # (16, 7, 7) 再经过一个2*2的平均池化层，下采样一倍。输出16通道，8*8特征图。
        )
        self.out = nn.Sequential(   # 输出层
            nn.Linear(16 * 7 * 7, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 36),  # 全连接，最终输出我们需要的分类数。
        )

    def forward(self, x):  # 整个模型前向传播。
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # 将输出化成一维向量。
        output = self.out(x)  # 全连接输出。
        return output