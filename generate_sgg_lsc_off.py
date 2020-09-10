from server_sggfunctions import perform_sgg_on_image
from server_myfunctions import Image, translate_to_human_read

import json
import os
import requests
import joblib
from tqdm import tqdm

DIR_DATA = '/mnt/DATA/lsc2020'
COMMON_PATH = os.getenv("COMMON_PATH")
# grouped_info = json.load(open(f"{COMMON_PATH}/group_info.json"))
scene_info = json.load(open(f"{COMMON_PATH}/scene_info.json"))

list_days = sorted(list(scene_info.keys()))
start_day = '2016-08-29'# '2016-08-15'
end_day = '2016-09-10' # '2016-09-10'
sample_portion = 0.75

jump_step = int(1/sample_portion)    
idx_start_day = list_days.index(start_day)
idx_end_day = list_days.index(end_day)
list_days_select = list_days[idx_start_day:(idx_end_day+1)]
thres_obj = 0.1
thres_rel = 1e-6
sgg_days = {}

def perform_sgg_one_day(idx_day, day): # day = list_days_select[idx_day]
    day_info = scene_info[day]
    list_scene_in_day = list(day_info.keys())
    numb_images_in_each_scene = [len(day_info[x]) for x in list_scene_in_day]

    list_images_perform_sgg = []

    for idx in range(len(numb_images_in_each_scene)):
        numb_images = numb_images_in_each_scene[idx]
        list_images_in_scene = day_info[list_scene_in_day[idx]]
        for i in range(0, numb_images, jump_step):
            list_images_perform_sgg.append(list_images_in_scene[i])

    temp = {}

    for image_id in list_images_perform_sgg:
        image_path = f"{DIR_DATA}/{image_id}"
        try:
            sample_image = Image.open(image_path).convert("RGB")
            response = perform_sgg_on_image(sample_image, thres_obj=thres_obj, thres_rel=thres_rel)
        except:
            response = {'sgg': [], 'bbox': [], 'human_read': []}
            raise
        sgg = response
        del(sgg['human_read'])
        temp[image_id] = sgg
        
    return (idx_day, temp)
        
import multiprocessing as mp
try:
    mp.set_start_method('spawn')
except RuntimeError:
    raise

pool = mp.Pool(2)

# call apply_async() without callback
result_objects = [pool.apply_async(perform_sgg_one_day, args=(i, day)) for i, day in enumerate(list_days_select)]

# result_objects is a list of pool.ApplyResult objects
results = [r.get()[1] for r in result_objects]

pool.close()
pool.join()

for idx_day in range(len(results)):
    sgg_days[list_days_select[idx_day]] = results[idx_day]

joblib.dump(sgg_days, 'lsc2018_08_29_09_10.joblib')

# for idx_day in range(len(list_days_select)): 
#     print(f'Processing {list_days_select[idx_day]}') 

#     day_info = scene_info[list_days_select[idx_day]]
#     list_scene_in_day = list(day_info.keys())
#     numb_images_in_each_scene = [len(day_info[x]) for x in list_scene_in_day]
#     # list_images_in_scene = day_info[list_scene_in_day[0]]

#     list_images_perform_sgg = []

#     for idx in range(len(numb_images_in_each_scene)):
#         numb_images = numb_images_in_each_scene[idx]
#         list_images_in_scene = day_info[list_scene_in_day[idx]]
#         for i in range(0, numb_images, jump_step):
#             list_images_perform_sgg.append(list_images_in_scene[i])

#     sgg_days[list_days_select[idx_day]] = {}

#     for image_id in tqdm(list_images_perform_sgg):
#         image_path = f"{DIR_DATA}/{image_id}"
#         try:
#             sample_image = Image.open(image_path).convert("RGB")
#             response = perform_sgg_on_image(sample_image, thres_obj=thres_obj, thres_rel=thres_rel)
#         except:
#             response = {'sgg': [], 'bbox': [], 'human_read': []}
#         sgg = response
#         del(sgg['human_read'])
#         sgg_days[list_days_select[idx_day]][image_id] = sgg

joblib.dump(sgg_days, 'lsc2018_08_29_09_10.joblib')
