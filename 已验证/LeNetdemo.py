import os
from PIL import Image
import time
import cv2
import torchvision
import numpy as np
from torch.utils.data import DataLoader
from torch import device,cuda,nn,optim,load,unsqueeze
from torch.autograd import Variable
from torchvision import transforms

from text_recognition.LeNet5 import LeNet5
from text_recognition.dataset import Mydata
start_time = time.time()

# 输入参数 训练集，训练标签，测试集，测试标签
root_dir = "text_recognition/train_character2"
labels_train = open("text_recognition/idx.txt")
test_dir = "text_recognition/textdata"
labels_test = open("text_recognition/idx.txt")


# 数据集集成打包+ 数据集批量化。

labelList = []
for line in labels_train:
    word = line.split()[0]  # 读取每行的第一个字符。
    labelList.append(word)  # 添加每一个类的标签。
dataset_train = Mydata(root_dir, labelList[0])  # 第一类数据集 集成。
for i in range(1, 36):
    dataset_train += Mydata(root_dir, labelList[i])  # 训练数据集36类 叠加集成。

labelList1 = []
for line in labels_test:
    word1 = line.split()[0]  # # 读取每行的第一个字符。
    labelList1.append(word1)  # 添加每个类的标签。
dataset_test = Mydata(test_dir, labelList1[0])  # 第一类测试集 集成。
for i in range(1, 36):
    dataset_test += Mydata(test_dir, labelList1[i])  # 测试数据集36类 叠加集成。


BATCH_SIZE = 10  # 定义批量化大小batch_size。
EPOCHS = 10  # 总共训练批次。
DEVICE = device("cuda" if cuda.is_available() else "cpu")  # 使用gpu。

# 根据batch_size,epochs，使用dataloader 实现：从集成好的数据集中，批量化提取工作。
# 训练数据集批量化提取：
train_loader = DataLoader(dataset=dataset_train,
                          batch_size=BATCH_SIZE,
                          shuffle=True)

# 测试数据集批量化提取：
test_loader = DataLoader(dataset=dataset_test,
                         batch_size=BATCH_SIZE,
                         shuffle=True)


# 在装载完成后，我们可以选取其中一个批次的数据进行预览。
images, labels = next(iter(train_loader))
img = torchvision.utils.make_grid(images)

img = img.numpy().transpose(1, 2, 0)

std = [0.5, 0.5, 0.5]
mean = [0.5, 0.5, 0.5]

img = img * std + mean
# print([labels[i] for i in range(10)])
# cv2.imshow('win', img)
# key_pressed = cv2.waitKey(0)


# 实例化一个网络
model = LeNet5()

# 定义损失函数和优化器
loss_function = nn.CrossEntropyLoss()   # 交叉熵
optimizer = optim.SGD(  # SGD优化器
    model.parameters(),
    lr=0.001,
    momentum=0.9
)


def preproccess(data):  # 定义一个数据类型转换子类。
    toTensor = transforms.ToTensor()
    data = toTensor(data)
    return data


# def demo(pre_img):  # 预测任务
#     checkpoint = "model_epoch_0.95.pth"   # 权重加载
#     decode = open("decode.txt")  # 解码
#     decode = list(decode)
#     checkpoint = torch.load(checkpoint, map_location='cpu')  # 加载checkpoint
#     model.load_state_dict(checkpoint)  # 权重输入模型
#     model.eval()  # 测试模式
#     tensor = preproccess(pre_img)  # 将图片转化成tensor
#     tensor = Variable(torch.unsqueeze(tensor, dim=0).float(), requires_grad=False)  # 转换格式
#     predict = model(tensor)[0].detach().numpy()  # 预测
#     label = np.argmax(predict[:], axis=0)
#     label = decode[int(label)]   # 输出标签
#     return label

def demo(img):
    checkpoint = "text_recognition/model_epoch_0.95.pth"  # 权重加载
    checkpoint = load(checkpoint, map_location='cpu')  # 加载checkpoint
    model.load_state_dict(checkpoint)  # 权重输入模型
    model.eval()  # 测试模式
    tensor = preproccess(img)  # 将图片转化成tensor
    tensor = Variable(unsqueeze(tensor, dim=0).float(), requires_grad=False)  # 转换格式
    predict = model(tensor)[0].detach().numpy()  # 预测
    label = np.argmax(predict[:], axis=0)
    return label



# if __name__ == '__main__':
    # 识别文件夹下文件
    # image_path = "images"  # 输入图片路径
    # img_path = os.listdir(image_path)
    # img_path.sort()
    # img_path.sort(key=lambda x: int(x[:-4]))
    # labels = []
    # label1 = []
    # for i in img_path:   # 遍历路径
    #     label = demo(Image.open(image_path + '/' + i))  # 找到图片输送到预测demo，生成标签
    #     print("picture:{}, label:{}".format(i, label))
    #     labels.append(label)
    # for line in labels:
    #     word = line.split()[0]
    #     label1.append(word)
    # labelx = label1[0]
    # for i in label1[1:]:
    #     labelx += i
    # print("labels:{}".format(labelx))

    # 识别单个图片
    # image_path = "123.png"
    # single_image = Image.open(image_path)
    # label_single_image = demo(single_image)
    # print("image:{},label:{}".format(image_path, label_single_image))

