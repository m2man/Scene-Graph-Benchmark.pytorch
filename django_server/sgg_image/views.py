from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import perform_sgg_on_image, Image, translate_to_human_read
import json

# Create your views here.
from django.http import HttpResponse

DIR_DATA = '/mnt/DATA/lsc2020'

def jsonize(response):
    # JSONize
    response = JsonResponse(response)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def index(request):
    return HttpResponse("Hello, buddy. You're at the sample panel. Please direct to perform_sgg_image/")

@csrf_exempt
def perform_sgg_image_api(request):
    image_id = request.GET.get('image_id')
    thres_obj = request.GET.get('thres_obj')
    thres_rel = request.GET.get('thres_rel')
    if thres_obj:
        thres_obj = float(thres_obj)
    else:
        thres_obj = 0.15
    if thres_rel:
        thres_rel = float(thres_rel)
    else:
        thres_rel = 5e-5

    print(f"Performing SGG on {image_id} with thres_obj: {thres_obj}, thres_rel: {thres_rel}")
    image_path = f"{DIR_DATA}/{image_id}"
    try:
        sample_image = Image.open(image_path).convert("RGB")
        result = perform_sgg_on_image(sample_image, thres_obj=thres_obj, thres_rel=thres_rel)
    except:
        result = {'sgg': [], 'bbox': [], 'human_read': []}
    # response = {'sgg': result['sgg'], 'bbox': result['bbox'], 'human_read': result['human_read'], 'bbox_scores': ...}
    return jsonize(result)

@csrf_exempt
def translate_to_human_read_api(request):
    request_json = json.loads(request.body)
    result = translate_to_human_read(request_json['sgg'])
    response = {'human_read': result}
    return jsonize(response)