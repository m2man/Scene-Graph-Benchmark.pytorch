import json
import os
import requests
import joblib
from tqdm import tqdm
# 2015-02-23/b00000086_21i6bq_20150223_075557e.jpg 

##### LOAD ALREADY PROCCESSED IMAGES #####
# DATA_FOLDER = '/mnt/DATA/nmduy/graph_matrix'
# images_info_dict = joblib.load(f"{DATA_FOLDER}/sgg_mst_lsc2018.joblib")
# list_processed_days = list(images_info_dict.keys())
# list_processed_days = sorted(list_processed_days)
# del images_info_dict

###########################################

port = '4445'
COMMON_PATH = os.getenv("COMMON_PATH")
# grouped_info = json.load(open(f"{COMMON_PATH}/group_info.json"))
scene_info = json.load(open(f"{COMMON_PATH}/scene_info.json"))

list_days = sorted(list(scene_info.keys()))
start_day = '2015-02-23'# '2016-08-15'
end_day = '2018-05-31' # '2016-09-10'
sample_portion = 0.75

jump_step = int(1/sample_portion)    
idx_start_day = list_days.index(start_day)
idx_end_day = list_days.index(end_day)
list_days_select = list_days[idx_start_day:(idx_end_day+1)]
thres_obj = 0.1
thres_rel = 1e-6
sgg_days = {}

start_day_lsc2018 = '2016-08-15'# '2016-08-15'
end_day_lsc2018 = '2016-09-10' # '2016-09-10'
idx_start_day_lsc2018 = list_days.index(start_day_lsc2018)
idx_end_day_lsc2018 = list_days.index(end_day_lsc2018)
idx_lsc2018 = [x for x in range(idx_start_day_lsc2018, idx_end_day_lsc2018+1)]

for idx_day in range(len(list_days_select)):
    if idx_day in idx_lsc2018:
        continue
    print(f'Processing {list_days_select[idx_day]}') 

    day_info = scene_info[list_days_select[idx_day]]
    list_scene_in_day = list(day_info.keys())
    numb_images_in_each_scene = [len(day_info[x]) for x in list_scene_in_day]
    # list_images_in_scene = day_info[list_scene_in_day[0]]

    
    list_images_perform_sgg = []

    for idx in range(len(numb_images_in_each_scene)):
        numb_images = numb_images_in_each_scene[idx]
        list_images_in_scene = day_info[list_scene_in_day[idx]]
        for i in range(0, numb_images, jump_step):
            list_images_perform_sgg.append(list_images_in_scene[i])

    sgg_days[list_days_select[idx_day]] = {}

    for image_id in tqdm(list_images_perform_sgg):
        #if image_id in list_processed_days:
        #    continue
        response = requests.get(f'http://localhost:{port}/sgg_server/perform_sgg_image/?image_id={image_id}&thres_obj={thres_obj}&thres_rel={thres_rel}')
        response = response.json()
        sgg = response
        del(sgg['human_read'])
        sgg_days[list_days_select[idx_day]][image_id] = sgg
    
    joblib.dump(sgg_days, 'lsc2020_exclude_lsc2018.joblib')

joblib.dump(sgg_days, 'lsc2020_exclude_lsc2018.joblib')
