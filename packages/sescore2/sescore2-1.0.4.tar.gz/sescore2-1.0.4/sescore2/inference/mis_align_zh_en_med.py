import pandas as pd
import numpy as np
import json

data = pd.read_csv('zh-en_align_validation.tsv', delimiter='\t', header=None)
id_mapping_lines = open('zhen_mapping.txt', 'r').readlines()
id_mapping = {ele.split('\t')[1][:-1]: int(ele.split('\t')[0]) for ele in id_mapping_lines}
raw_id_mapping = {int(ele.split('\t')[0]): ele.split('\t')[1][:-1] for ele in id_mapping_lines}

# verify if all testing ids are valid
load_srcs_ls = open('medline_zh2en_zh.txt', 'r').readlines()[:100]
load_refs_ls = open('medline_zh2en_en.txt', 'r').readlines()
src_doc_ids = [ele.split('\t')[0]+'_'+ele.split('\t')[1] for ele in load_srcs_ls]

src_doc_ids_1000 = []
for i in range(10):
    src_doc_ids_1000 += src_doc_ids
print(len(src_doc_ids_1000))

src_id_txt_dict = {ele.split('\t')[0]+'_'+ele.split('\t')[1]: ele.split('\t')[2][:-1] for ele in load_srcs_ls}
ref_id_txt_dict = {ele.split('\t')[0]+'_'+ele.split('\t')[1]: ele.split('\t')[2][:-1] for ele in load_refs_ls}

# 1 -> raw doc id, 2 -> src seg id, 3 -> ref seg id 
src_ref_mapping_dict = {}
for check, id, src_seg_id, ref_seg_id in zip(data[0], data[1], data[2], data[3]):
    src_ref_mapping_dict[raw_id_mapping[id]+'_'+src_seg_id] = {}
    src_ref_mapping_dict[raw_id_mapping[id]+'_'+src_seg_id]['check'] = check
    src_ref_mapping_dict[raw_id_mapping[id]+'_'+src_seg_id]['ref_loc'] = raw_id_mapping[id]+'_'+ref_seg_id

# doc53->5,6; doc56->2,3,4; doc62->4,5
# print(src_ref_mapping_dict['doc53_5,6'])
# print(src_ref_mapping_dict['doc56_2,3,4'])
# print(src_ref_mapping_dict['doc62_4,5'])
# print()

data = pd.read_excel('英德_中英翻译模型评估-英语.xlsx', header=None, \
                   sheet_name=['中-英全数据-1','中-英全数据-2', '中-英全数据-3'])
ori_data = pd.read_excel('annotated_zh_en_bio_med_1000.xlsx')
out_ls = list(ori_data['translation'])

annotations = ['中-英全数据-1','中-英全数据-2', '中-英全数据-3']
scores_arr = 0
# from 1 to 4: 1->src, 2->output, 3->score, 4->annotations   
for anno in annotations:
    cur_ls = list(data[anno][3])[:-1]
    print(np.isnan(np.array(cur_ls).any()))
    scores_arr += np.array(cur_ls)
all_scores_ls = list(scores_arr/3)

src_ls, ref_ls, scores_ls, outs_ls = [], [], [], []
for ele, score, out in zip(src_doc_ids_1000, all_scores_ls, out_ls):
    if ele in src_ref_mapping_dict:
        if src_ref_mapping_dict[ele]['check'] == 'OK':
            src_ls += [src_id_txt_dict[ele]]
            doc_id = src_ref_mapping_dict[ele]['ref_loc'].split('_')[0]
            ref_seg_ids = src_ref_mapping_dict[ele]['ref_loc'].split('_')[1].split(',') 
            ele_ref_txt_ls = [ref_id_txt_dict[doc_id+'_'+id] for id in ref_seg_ids]
            ref_ls += [' '.join(ele_ref_txt_ls)]
            scores_ls += [score]
            outs_ls += [out]

bio_gt_dict = {}
bio_gt_dict['src'], bio_gt_dict['ref'], bio_gt_dict['out'], bio_gt_dict['score'] = \
src_ls, ref_ls, outs_ls, scores_ls

with open(f'gt_zh-en_biomed.json', 'w') as f:
    json.dump(bio_gt_dict, f)

print("File is saved!")
