import torch
import numpy as np
from PIL import Image
import PIL
from torchvision import datasets, transforms, models
from torch.autograd import Variable
import numpy as np

class RecogClass():
    def __init__(self,path:str,device='cpu'):
        self.img_dict={
            '0':'水稻稻瘟病',
            '1':'水稻细菌性褐斑病',
            '2':'水稻纹枯病',
            '3':'水稻东格鲁病毒病',
            '4':'水稻白叶枯病',
        }
        #导入训练好的模型
        self.model = torch.load(path,map_location=device)

    def get_result_by_PIL(self,img):
        #图像预处理
        transform = transforms.Compose([
            #图像缩放
            transforms.Resize((64,64), interpolation=2),
            #转Tensor形式
            transforms.ToTensor(),
            #归一化，标准化操作
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        m=transform(img)
        m=np.expand_dims(m,0) #将维度为3的图片扩充到4维，解决单张图片预测时因维度不一致报错

        img_v=Variable(torch.Tensor(m))
        #预测
        outputs = self.model(img_v)
        #获得预测标签
        _,pred_labels = torch.max(outputs, 1)
        #转换成标签所对应的中文名称，返回其结果
        item = pred_labels.item()
        return self.img_dict[str(item)]

    def get_result_by_path(self,img_path:str):
        img = Image.open(img_path)
        result_str = self.get_result_by_PIL(img)

        return result_str

if __name__ == '__main__':
    #测试...
    R = RecogClass(r'D:\GitHub\RiceDiseasesWeb\recognition\vgg_save.pt')
    print(R.get_result_by_path(r'D:\GitHub\RiceDiseasesWeb\recognition\dataset\blight\blight__0_85.jpg'))
    # pass