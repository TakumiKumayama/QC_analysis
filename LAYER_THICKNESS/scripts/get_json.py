import datetime
from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
import pprint
import sys
import json
import logging
import traceback
from pathlib import Path
import jsonschema
from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt
import localDBtools
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
import os
#import ROOT



def mkPCB_SNlist():
    SHEET_ID = '1BrP1ZUhfLx81iy4winwhAItocJb6Eg7z8EUW_kOVk5g'
    SHEET_NAME = 'Yamashita%20PCB%20Production'
    
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)
    l_PCB_SN = open('../data/lists/PCB.txt', 'w')
    #print(df.columns.tolist())
    
    for index, row in df.iterrows():
        i_PCB_SN = row['SN']
        i_is_LDB_uploaded = row['DB BARE']
        
        if(i_is_LDB_uploaded=='Uploaded to PDB'):
            l_PCB_SN.write(f'{i_PCB_SN}\n')
            #print(f"{i_PCB_SN} is Listed!!")



def get_option(argparser):
    argparser.add_argument('-l', '--serialNumberlist', type=str,
                           required=False,
                           default='../data/lists/PCB.txt',
                           help='specify serial nubmer list file name')
    argparser.add_argument('-v', '--verbose', required=False,
                           default=False,action='store_true',
                           help='use this option to dump stage name')
    argparser.add_argument('-p', '--outputPlot', required=False,
                           default=False,action='store_true',
                           help='use this option to output plot_file')
    return argparser.parse_args()



def get_json():
    argparser = ArgumentParser()
    args = get_option(argparser)
    l_PCB_SN = args.serialNumberlist
    debug = args.verbose
    do_plt = args.outputPlot
    chst=localDBtools.LocalDBtools()

    with Path(l_PCB_SN).open(encoding="utf-8") as f:
        for line in f.readlines():
            i_PCB_SN=line.replace("\n","")
            i_PCB_json = chst.get_aLayerThicknessData(i_PCB_SN,debug)
            
            with open(f"../data/json/{i_PCB_SN}.json", 'w', encoding='utf-8') as f:
                json.dump(i_PCB_json, f, ensure_ascii=False, indent=4)
                print(f"PCB : {i_PCB_SN} Listed!!")
                
    return do_plt
                
                
                
def list_json_files(directory):
    l_path = [os.path.join(directory, f) for f in os.listdir(directory)]
    json_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
    return json_files



if __name__ == "__main__":
    mkPCB_SNlist()
    do_plt = get_json()
    
    base_dir = '../data/json'
    json_paths = list_json_files(base_dir)
    with open('../data/results/LayerThickness.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(f"SERIALNUMBER\tBOTTOM\tCOVERLAY\tDIELECTRIC\tINNER\tALL\n")
        for path in json_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    i_SN = os.path.basename(path)[:14]
                    i_data = json.load(f)
                    if i_data is None:
                        print(f"{path}: Json is null ... continued")
                        continue
                    #i_SN = i_data['Metadata']['MODULE_SN']
                    i_top = format(i_data['TOP_LAYER_THICKNESS'], ".2f")
                    i_inn = format(i_data['INNER_LAYER_THICKNESS'], ".2f")
                    i_bot = format(i_data['BOTTOM_LAYER_THICKNESS'], ".2f")
                    i_die = format(i_data['DIELECTRIC_THICKNESS'], ".2f")
                    i_cov = format(i_data['COVERLAY_WITH_ADHESIVE_THICKNESS'], ".2f")
                    i_all = format(i_data['THICKNESS'], ".2f")
                    f_out.write(f"{i_SN}\t{i_bot}\t{i_cov}\t{i_die}\t{i_inn}\t{i_all}\t{i_top}\n")
                    
            except json.JSONDecodeError:
                print(f"{path}: JSON の解析に失敗しました")

            except Exception as e:
                print(f"{path}: エラーが発生しました - {e}")
                
    if(do_plt):
        root_script = "mkhist.cpp"
        os.system(f"root -l {root_script}")
                
        