import os
import numpy as np
import cv2
from torch.utils.data import Dataset
from torchvision import transforms



# 数据集载入内存。继承torch下Dataset类，再继承Dataloader类进行数据集批量化。
# 训练时，根据批量化大小batch_size 循环更新loss 。
class Mydata(Dataset):

    def __init__(self, root_dir, label_dir):  # 修改类下初始化任务。
        self.root_dir = root_dir  # 初始化地址
        self.label_dir = label_dir  # 初始化标签地址
        self.path = os.path.join(self.root_dir, self.label_dir)  # 将数据集加载进路径。
        self.img_path = os.listdir(self.path)  # 数据集列表。
        self.toTensor = transforms.ToTensor()

    def __len__(self):
        return len(self.img_path)  # 返回路径下数据集总长度。 后续batch_size分组用到。

    def __getitem__(self, idx):  # 修改类下读取数据集任务。
        img_name = self.img_path[idx]  # 根据索引读取数据名称。
        img_item_path = os.path.join(self.root_dir, self.label_dir, img_name)  # 读取单个数据路径。
        img = cv2.imread(img_item_path)  # cv读取图片数据。
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化，统一通道数为1。
        img = np.array(img)  # 图片转换为numpy数据类型。
        img = self.data_preproccess(img)   # numpy转换为tensor类型。
        label = self.label_dir  # 标签就为输入的标签名。
        label = int(label)  # 标签转换为int类型。
        return img, label  # 返回数据+标签。

    def data_preproccess(self, data):  # 定义一个数据类型转换子类。
        data = self.toTensor(data)
        return data

# 以上完成了数据集加载进内存工作。