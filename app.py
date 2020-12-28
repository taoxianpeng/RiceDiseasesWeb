from os.path import join
from typing import List
from flask import Flask,render_template,redirect,sessions
from flask import request as flask_request
import os
import glob
import math
import urllib.parse
from flask.globals import request
from flask.helpers import url_for
from werkzeug.exceptions import MethodNotAllowed

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def processing_list(list:List,step=4):
    return [list[i*step-step:i*step] for i in range(1,math.ceil(len(list)/step))]
@app.route('/')
def index():
    '''
    页面一启动，就自动加载所有病害图片进行展示。

    数据由字典组装再封装到list中，格式如下：
    dict = { 'path': ..., 'name': ..., 'abstract': ...} #其中abstact暂时未启用
    list = [dict1, dict2, dict3, ...]
    '''
    row_max_cards = 4
    images_paths_list = glob.glob("./static/diseasesImage/*.png")
    full_row_nums = math.ceil(len(images_paths_list))
    images_names_list = [name.split('\\')[-1].split('.')[0] for name in images_paths_list]

    res_list = []
    for path,name in zip(images_paths_list, images_names_list):
        img_dict={}
        img_dict['path'] = path
        img_dict['name'] = name
        res_list.append(img_dict)

    res_list = processing_list(res_list)

    return render_template('index.html',nums=full_row_nums,image_lists=res_list)

@app.route('/diseases',methods=['GET'])
def diseases():
    name = urllib.parse.unquote(flask_request.values.get('name'))
    return render_template('diseases.html',name = name)
@app.route('/recognition', methods = ['GET', 'POST'])
def recognition():
    # f = request.form
    # s = request.form
    # print(f,s)
    f = request.files  
    print(f)

    return 'success'
    # print(request.values['size'])
if __name__ == '__main__':
    app.run()