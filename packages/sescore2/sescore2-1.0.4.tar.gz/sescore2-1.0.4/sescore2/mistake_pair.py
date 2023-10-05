import json
from process_results import *
import itertools
import numpy as np
from tqdm.auto import tqdm
import click
import math

# key question: 
# why BLEURT, COMET and GPT3 all dropped around 6% in Kendall correlation, does this 6%
# shares some similarities in the mistakes or just coincidence
# /Users/wendaxu/opt/anaconda3/lib/python3.9/site-packages/mt_metrics_eval/stats.py

def Agreement(vect1, vect2, vect_names):
  """Compute pairwise agreement over two vectors, vect1 assumed to be gold."""
  agree, num_pairs, dis_ls, T, U, P, Q = 0, 0, [], 0, 0, 0, 0
  count, cor_count = 0, 0
  pairs_ls = list(itertools.combinations(zip(vect1, vect2, vect_names), 2))
  with tqdm(total=len(pairs_ls)) as pbar:
    for a, b in pairs_ls:
        pbar.update(1)
        if a[0] is None or b[0] is None:
            continue

        if (a[0] - b[0]) == 0:
            count += 1

        if np.sign(a[0] - b[0]) == np.sign(a[1] - b[1]):
            agree += 1
            if (a[1] - b[1]) == 0:
                cor_count+=1
        else:
            dis_ls += [(a[2], b[2])]

        if (a[0] - b[0] > 0 and a[1] - b[1] > 0) or (a[0] - b[0] < 0 and a[1] - b[1] < 0):
            P += 1
        elif (a[0] - b[0] > 0 and a[1] - b[1] < 0) or (a[0] - b[0] < 0 and a[1] - b[1] > 0):
            Q += 1
        else:
            if (a[0] - b[0]) == 0 and (a[1] - b[1]) != 0:
                T += 1
            elif (a[0] - b[0]) != 0 and (a[1] - b[1]) == 0:
                U += 1  
        num_pairs += 1  
    cor = (P-Q)/math.sqrt((P+Q+T)*(P+Q+U))
  
  print("Tie accuracy: ", cor_count/count)
  print("Total ties: ", count)
  print("tie accounts total: ", count/num_pairs)
  print("P: ", P)
  print("Q: ", Q)
  print("T: ", T)
  print("U: ", U)
  return agree, num_pairs, dis_ls, cor

@click.command()
@click.option('-wmt', default='wmt21.news')
@click.option('-lang', default='zh-en')
@click.option('-start', type=int)
@click.option('-end', type=int)
def main(wmt, lang, start, end):
    metric_names = ['comet', 'bleurt', 'gpt3', 'sescore2', 'bleu', 'bertscore', 'prism', 'yisi', 'comet-src-only-mqm', \
    'comet-mqm', 'chrf', 'ter']
    save_dict = {}
    for metric_name in metric_names:
        if metric_name == 'gpt3':
            scores_dict = json.load(open('wmt21.news_zh-en_0_300_gpt3.json'))
            scores_dict = {key: scores_dict[key][start:end] for key in scores_dict}
        elif metric_name == 'sescore2':
            sescore2_dict = json.load(open('baseline_results/zh-en_wmt21.news_contrascore.json'))
            scores_dict = {}
            for sys, scores_ls in sescore2_dict.items():
                scores_dict[sys] = []
                for index in indices_set:
                    scores_dict[sys] += [scores_ls[index]]
            scores_dict = {key: scores_dict[key][start:end] for key in scores_dict}
        else:
            if metric_name == 'comet':
                lines = open('baseline_results/COMET-DA_2020-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'bleurt':
                lines = open('baseline_results/bleurt-20-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'bleu':
                lines = open('baseline_results/sentBLEU-refB.seg.score', 'r').readlines()

            elif metric_name == 'bertscore':
                lines = open('baseline_results/BERTScore-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'prism':
                lines = open('baseline_results/Prism-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'yisi':
                lines = open('baseline_results/YiSi-1-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'comet-src-only-mqm':
                lines = open('baseline_results/COMET-QE-MQM_2021-src.seg.score', 'r').readlines()

            elif metric_name == 'comet-mqm':
                lines = open('baseline_results/COMET-MQM_2021-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'chrf':
                lines = open('baseline_results/chrF-refB.seg.score', 'r').readlines()
            
            elif metric_name == 'ter':
                lines = open('baseline_results/TER-refB.seg.score', 'r').readlines()

            else:
                print("metric name is not supported!")
                exit(1)

            evs = data.EvalSet(wmt, lang)
            gt_scores, indices_set, num_sys = process_gt_metric_outs(evs, start, end)

            pre_scores_dict = {}
            num_segs = int(len(lines)/num_sys)
            for line in lines:
                sys_name, score = line.split('\t')[0], float(line.split('\t')[1][:-1])
                if sys_name not in pre_scores_dict:
                    pre_scores_dict[sys_name] = []
                pre_scores_dict[sys_name]+=[score]
            scores_dict = {}
            for sys, scores_ls in pre_scores_dict.items():
                scores_dict[sys] = []
                for index in indices_set:
                    scores_dict[sys] += [scores_ls[index]]
            scores_dict = {key: scores_dict[key][start:end] for key in scores_dict}

        gt_scores_ls, baseline_ls, sys_index_ls = [], [], []
        sys_names = set(gt_scores) - {evs.std_ref} 

        for sys in sys_names:
            gt_scores_ls += gt_scores[sys]
            baseline_ls += scores_dict[sys]
            indices_ls = [sys+'_'+str(i) for i in range(len(gt_scores[sys]))]
            sys_index_ls += indices_ls

        agree, num_pairs, dis_ls, cor = Agreement(gt_scores_ls, baseline_ls, sys_index_ls)
        save_dict[metric_name] = dis_ls

        print("metric name: ", metric_name)
        print("Agree: ", agree)
        print("Disagree", len(dis_ls))
        print("Total: ", num_pairs)
        print("Accuracy: ", agree/num_pairs)
        print("Kendall Tau-Like: ", (agree-len(dis_ls))/num_pairs)
        print("Kendall: ", cor)
        print("-----------------------------------------")
        print()

    with open(f'metrics_{start}_{end}_mistake_pairs.json', 'w') as f:
        json.dump(save_dict, f)
    print("File is saved")

if __name__ == "__main__":
    main()  