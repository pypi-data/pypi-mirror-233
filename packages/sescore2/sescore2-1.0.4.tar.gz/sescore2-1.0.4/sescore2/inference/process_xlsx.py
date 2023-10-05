import pandas as pd
import json
import numpy as np

data = pd.read_excel('英德_中英翻译模型评估-英语.xlsx', header=None, \
                   sheet_name=['中-英全数据-1','中-英全数据-2', '中-英全数据-3'])

ori_data = pd.read_excel('annotated_zh_en_bio_med_1000.xlsx')

annotations = ['中-英全数据-1','中-英全数据-2', '中-英全数据-3']
src_ls, out_ls, scores_ls, ref_ls, ele_src_ls, ele_ref_ls = [], [], [], [], [], []

load_refs_ls = open('medline_zh2en_en.txt', 'r').readlines()
load_srcs_ls = open('medline_zh2en_zh.txt', 'r').readlines()

refs_dict = {}
for line in load_refs_ls:
    doc_id, seg_id, txt = line.split('\t')[0], line.split('\t')[1], line.split('\t')[2][:-1]
    refs_dict[doc_id+"_"+seg_id] = txt

for line in load_srcs_ls[:100]:
    doc_id, seg_id, txt = line.split('\t')[0], line.split('\t')[1], line.split('\t')[2][:-1]
    ele_src_ls += [txt]
    ele_ref_ls += [refs_dict[doc_id+"_"+seg_id]]

for i in range(10):
    ref_ls += ele_ref_ls
    src_ls += ele_src_ls

out_ls = list(ori_data['translation'])

scores_arr = 0
# from 1 to 4: 1->src, 2->output, 3->score, 4->annotations   
for anno in annotations:
    cur_ls = list(data[anno][3])[:-1]
    print(np.isnan(np.array(cur_ls).any()))
    scores_arr += np.array(cur_ls)
scores_ls = list(scores_arr/3)

print(src_ls[90:100])
print(ref_ls[90:100])

bio_gt_dict = {}
bio_gt_dict['src'], bio_gt_dict['ref'], bio_gt_dict['out'], bio_gt_dict['score'] = src_ls, ref_ls, out_ls, scores_ls

with open(f'gt_zh-en_biomed.json', 'w') as f:
    json.dump(bio_gt_dict, f)

print("File is saved!")