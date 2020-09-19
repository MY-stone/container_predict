from torch import max,save
from LeNetdemo import model, train_loader, optimizer, loss_function, EPOCHS
from torch.autograd import Variable

#  定义训练函数：
from LeNetdemo import test_loader


def train(epochs):  # 定义每个epoch的训练细节。
    model.train()  # 设置为training模式。
    train_acc = 0  # 初始化精确度。
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)  # 把数据转换成Variable。
        optimizer.zero_grad()  # 优化器梯度初始化为零。
        output = model(data)  # 把数据输入网络并得到输出，即进行前向传播。
        loss = loss_function(output, target)  # 交叉熵损失函数。
        loss.backward()  # 反向传播梯度。
        optimizer.step()  # 结束一次前传+反传之后，更新参数。
        pred = max(output, 1)[1]
        train_acc += pred.eq(target.data.view_as(pred)).cpu().sum()  # 精确度叠加。
        if batch_idx % 10 == 0:  # 训练完成，准备打印相关信息。
            # 输出epoch，训练进度，loss，精确度。
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}, Accuracy: ({:.0f}%)\n'.format(
                epochs, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item(), 100. * train_acc / len(train_loader.dataset)))


# 定义测试函数：


def test():
    model.eval()  # 设置为test模式。
    test_loss = 0  # 初始化测试损失值为0。
    correct = 0  # 初始化预测正确的数据个数为0。
    for data, target in test_loader:
        data, target = Variable(data), Variable(target)  # 计算前要把变量变成Variable形式，因为这样子才有梯度。

        output = model(data)  # 前向传播。
        test_loss += loss_function(output, target).item()  # sum up batch loss 把所有loss值进行累加。
        pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()  # 对预测正确的数据个数进行累加。

    test_loss /= len(test_loader.dataset)  # 因为把所有loss值进行过累加，所以最后要除以总得数据长度才得平均loss
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    # 训练：
    for epoch in range(1, EPOCHS + 1):  # 以epoch为单位进行循环
        train(epoch)

    # 测试：
        test()

    # 保存权重文件
        save(model.state_dict(), "model.pth")  # 保存参数


    # # 保存模型：
    # # torch.save(model, 'LeNet.pth')  # 保存模型
