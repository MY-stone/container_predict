import cv2
from text_recognition.preprocess import separate_recognition

#image:图片地址str
def txt_predicte(image):
    
    single_img = cv2.imread(image)  # 读取地址
    single_img_rec_result = separate_recognition(single_img)
    return single_img_rec_result

if __name__ == "__main__":
    txt = txt_predicte('text_recognition/2.png')
    print(txt)