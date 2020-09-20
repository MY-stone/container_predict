import cv2
import numpy as np
from text_recognition.LeNetdemo import demo


def add_border_w(rec_img):
    rec_img_shape = np.shape(rec_img)
    abs_pix = abs(rec_img_shape[0] - rec_img_shape[1])
    pix_a = abs_pix // 2
    pix_r = abs_pix % 2
    if rec_img_shape[0] > rec_img_shape[1]:
        add_array = np.zeros((rec_img_shape[0], pix_a))
        tmp_array = np.hstack((add_array, rec_img, add_array))
        if pix_r == 1:
            add_array_r = np.zeros((rec_img_shape[0], 1))
            return np.hstack((tmp_array, add_array_r))
        else:
            return tmp_array
    if rec_img_shape[0] < rec_img_shape[1]:
        add_array = np.zeros((pix_a, rec_img_shape[1]))
        tmp_array = np.vstack((add_array, rec_img, add_array))
        if pix_r == 1:
            add_array_r = np.zeros(rec_img_shape[1])
            return np.vstack((tmp_array, add_array_r))
        else:
            return tmp_array
    else:
        return rec_img


def region_threshold(gray_img):
    img_height = gray_img.shape[0]
    section_length = img_height // 10
    final_img = gray_img
    for sec_i in range(9):
        sec_img = gray_img[sec_i * section_length:(sec_i + 1) * section_length, :]
        ret3, img_thre = cv2.threshold(sec_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        final_img[sec_i * section_length:(sec_i + 1) * section_length, :] = img_thre
    sec_img = gray_img[9 * section_length:, :]
    ret3, img_thre = cv2.threshold(sec_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    final_img[9 * section_length:, :] = img_thre
    return final_img


def separate_recognition(single_img_part):
    character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                      'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    img_gray = cv2.cvtColor(single_img_part, cv2.COLOR_BGR2GRAY)  # 将截取的图片灰度化
    img_thre = region_threshold(img_gray)  # 图像分成10个部分进行直方图二值化
    # ret3 返回判断输入是否是图片
    height = img_gray.shape[0]  # 高
    width = img_gray.shape[1]  # 宽
    if 2 * width > height:  # 通过高和宽的关系判断横排，竖排
        direction_flag = 1  # 横排
    else:
        direction_flag = 0  # 竖排

    recognition_crt_list = []  # 最终识别单个字符的代码（0-35）
    if direction_flag == 1:  # 横排识别
        white = 0
        black = 0
        height = img_thre.shape[0]
        # 统计第一列的黑白像素。判断字体颜色。我们最终需要黑背景白字进行处理。
        for height_i in range(height):
            if img_thre[height_i][0] == 255:
                white += 1
            if img_thre[height_i][0] == 0:
                black += 1
        arg = False  # False(font:black, background:white)； True(font:white, background:black)
        if black > white:  # 判断字体为白色还是黑色
            arg = True
        if not arg:
            cv2.bitwise_not(img_thre, img_thre)  # 黑白反转
        img_threshold_copy = img_thre.copy()  # 复制经过二值化后的图像
        img_threshold_b = np.zeros(img_thre.shape, np.uint8)  # 新建一个大小与上图一致全黑的图像
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # 进行膨胀操作所用的元素类型，3*3矩阵

        while img_threshold_copy.any():  # 通过联通域，提取单个字符
            Xa_copy, Ya_copy = np.where(img_threshold_copy > 0)  # thresh_A_copy中值为255的像素的坐标
            min_y_index = np.argmin(Ya_copy)
            img_threshold_b[Xa_copy[min_y_index]][Ya_copy[min_y_index]] = 255

            for dilate_i in range(200):
                dilation_b = cv2.dilate(img_threshold_b, kernel, iterations=1)
                img_threshold_b = cv2.bitwise_and(img_thre, dilation_b)

            Xb, Yb = np.where(img_threshold_b > 0)
            con_pix_num = len(Xb)
            if con_pix_num < 135:
                number = 40
            else:
                number = 110
            if con_pix_num > number:
                min_y = np.argmin(Yb)
                max_y = np.argmax(Yb)
                min_x = np.argmin(Xb)
                max_x = np.argmax(Xb)

                # 解决 第五位 竖杠问题
                if Xb[max_x]-Xb[min_x] == height - 1:
                    img_threshold_copy[Xb, Yb] = 0
                    img_threshold_b[Xb, Yb] = 0
                    continue

                single_c = img_threshold_b[Xb[min_x]:Xb[max_x] + 1, Yb[min_y]:Yb[max_y] + 1]
                single_c_border = add_border_w(single_c)
                single_c_one = cv2.resize(single_c_border, (36, 36))
                recognition_crt_list.append(demo(single_c_one))

                img_threshold_copy[Xb, Yb] = 0
                img_threshold_b[Xb, Yb] = 0
            else:
                img_threshold_copy[Xb, Yb] = 0
                img_threshold_b[Xb, Yb] = 0
    else:  # 竖排识别
        white_max = 0
        black_max = 0
        height = img_thre.shape[0]
        width = img_thre.shape[1]
        for height_i in range(height):
            s = 0  # white
            t = 0  # black
            for width_i in range(width):
                if img_thre[height_i][width_i] == 255:
                    s += 1
                if img_thre[height_i][width_i] == 0:
                    t += 1
                white_max = max(white_max, s)
                black_max = max(black_max, t)

        arg = False  # False(font:black, background:white)； True(font:white, background:black)
        if black_max > white_max:
            arg = True
        if not arg:
            cv2.bitwise_not(img_thre, img_thre)
        img_threshold_copy = img_thre.copy()
        img_threshold_b = np.zeros(img_thre.shape, np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        while img_threshold_copy.any():
            # count_0 += 1
            Xa_copy, Ya_copy = np.where(img_threshold_copy > 0)  # thresh_A_copy中值为255的像素的坐标
            min_x_index = np.argmin(Xa_copy)
            img_threshold_b[Xa_copy[min_x_index]][Ya_copy[min_x_index]] = 255

            # 连通分量算法，先对thresh_B进行膨胀，再和thresh_A执行and操作（取交集）
            for dilate_i in range(200):
                dilation_B = cv2.dilate(img_threshold_b, kernel, iterations=1)
                img_threshold_b = cv2.bitwise_and(img_thre, dilation_B)

            Xb, Yb = np.where(img_threshold_b > 0)
            con_pix_num = len(Xb)
            # if con_pix_num < 135:
            #     number = 40
            # else:
            #     number = 110
            if con_pix_num > 110:

                min_x = np.argmin(Xb)
                max_x = np.argmax(Xb)
                min_y = np.argmin(Yb)
                max_y = np.argmax(Yb)
                single_c = img_threshold_b[Xb[min_x]:Xb[max_x] + 1, Yb[min_y]:Yb[max_y] + 1]
                single_c_border = add_border_w(single_c)
                single_c_one = cv2.resize(single_c_border, (36, 36))
                recognition_crt_list.append(demo(single_c_one))

                img_threshold_copy[Xb, Yb] = 0
                img_threshold_b[Xb, Yb] = 0

            else:
                img_threshold_copy[Xb, Yb] = 0
                img_threshold_b[Xb, Yb] = 0

    if len(recognition_crt_list) == 0:   # 字符空返回
        return ' '
    elif len(recognition_crt_list) == 12:  # 消除框框
        del recognition_crt_list[10]
    elif len(recognition_crt_list) == 11:  # 正确判断字符位数
        pass
    else:
        s = character_list[recognition_crt_list[0]]  # 其他长度 返回原始内容
        for i in range(1, len(recognition_crt_list)):
            s = s + character_list[recognition_crt_list[i]]
        return s

    for ii in range(4):  # 前四位，若识别出错：数字转字母
        if recognition_crt_list[ii] == 8:
            recognition_crt_list[ii] = 11
        elif recognition_crt_list[ii] == 0:
            recognition_crt_list[ii] = 24
        elif recognition_crt_list[ii] == 1:
            recognition_crt_list[ii] = 18
        elif recognition_crt_list[ii] == 2:
            recognition_crt_list[ii] = 35
    for jj in range(4, 11):  # 后7位，若识别出错：字母转数字
        if recognition_crt_list[jj] == 11:
            recognition_crt_list[jj] = 8
        elif recognition_crt_list[jj] == 24:
            recognition_crt_list[jj] = 0
        elif recognition_crt_list[jj] == 18:
            recognition_crt_list[jj] = 1
        elif recognition_crt_list[jj] == 35:
            recognition_crt_list[jj] = 2


    s = character_list[recognition_crt_list[0]]  # 解码
    for i in range(1, len(recognition_crt_list)):  # 字符拼接
        s = s + character_list[recognition_crt_list[i]]
    return s