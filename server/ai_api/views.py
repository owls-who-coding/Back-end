from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from keras.models import load_model
from keras.preprocessing import image
from io import BytesIO

import os
import base64
import numpy as np, base64
import PIL.Image 

MODEL_PATH = './ai_api/class_model/'
WEIGHT = os.listdir(MODEL_PATH)

try :
    models = {}
    for weight in WEIGHT :
        dis_name = weight.split('_')[0]
        models[dis_name] = load_model(MODEL_PATH + weight)

    print("모델 불러오기 성공!\n", models)
except :
    print("Not Fount Models, 모델을 찾을 수 없습니다. 팀원에게 받아주세요.")


def decode_img(img_base64) :
    file_like = BytesIO(base64.b64decode(img_base64))
    img=PIL.Image.open(file_like)
    rgb_img = img.convert("RGB")
    return rgb_img



def get_img_batch(img_rgb) :
    img_array = image.img_to_array(img_rgb)
    img_batch = np.expand_dims(img_array, axis = 0)
    img_batch = np.divide(img_batch, 255.0)
    return img_batch



def predict(img_batch) :
    predict_res={}
    
    for dis_name, model in models.items() :
        pred = model.predict(img_batch, verbose = 1)
        pred = pred[0]
        if pred[1] > 0.5 :
            predict_res[dis_name] = f'{round(pred[1] * 100, 2)}'

    if(len(predict_res) == 0) :
        predict_res["증상 없음"] = "100"
    print(predict_res)
    return predict_res


class Predict_Image(APIView) :

    def get(self, request) :
        img_path = './ai_api/test_img/무1'
        try :
            img_rgb=image.load_img(f'{img_path}.jpg', target_size=(224,224))
        except :
            img_rgb=image.load_img(f'{img_path}.png', target_size=(224,224))

        img_batch = get_img_batch(img_rgb)

        predict_res = predict(img_batch)
        return JsonResponse(predict_res, json_dumps_params={'ensure_ascii' : False})
    


    def post(self, request) :
        #f=open('./test.txt', 'w')
        img_base64 = str(request.body).split('"')[1]

        img_rgb = decode_img(img_base64)
        img_batch = get_img_batch(img_rgb)

        predict_res = predict(img_batch)

        return JsonResponse(predict_res, json_dumps_params={'ensure_ascii' : False})

            
