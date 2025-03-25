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
#import matplotlib.pyplot as plt
import localDBtools
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
#import ROOT

def mklist():
    mode = 0    # Production
    #mode = 1   # Preproduction
    
    # Google スプレッドシートのURL
    SHEET_ID = '1BrP1ZUhfLx81iy4winwhAItocJb6Eg7z8EUW_kOVk5g'
    if mode==0:
        SHEET_NAME = 'Production%20module'
    elif mode==1:
        SHEET_NAME = 'Preproduction%20module'

    # CSV形式のデータ
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)

    # 結果を保存するテキストファイル
    l_Module_SN = open('../data/lists/Module.txt', 'w')
    l_Module_Bare_sensor_SN = open('../data/lists/Module_Bare_sensor.txt', 'w')
    
    l_Module_Bare_sensor_SN.write(f"ModuleID\tModuleSN\tBaremoduleID\tSensorSN\n")
    
    for index, row in df.iterrows():
        i_Module_ID = row['module id']
        #wafer_lot = row['Sensor information sensor wafer lot ID']
        if mode==0:
            Batch_id = row['Batch ID']
        elif mode==1:
            Batch_id = row['Bare modules information Batch ID'] # Preproductionだとこっち。

        i_Module_SN = row['ATLAS Serial Number for parts ATLAS SN (Module)']
        i_Bare_module_SN = row['ATLAS SN (BareModule)']
        i_sensor_SN = row['ATLAS SN (Sensor)']
        

        if not pd.isna(i_Module_SN):
            # 結果をテキストファイルに記入
            #output_file.write(f'{i_Module_SN}\t{int(Batch_id)}\n')
            l_Module_SN.write(f'{i_Module_SN}\n')
            l_Module_Bare_sensor_SN.write(f'{i_Module_ID}\t{i_Module_SN}\t{i_Bare_module_SN}\t{i_sensor_SN}\n')
    

def get_option(argparser):
    argparser.add_argument('-l', '--serialNumberlist', type=str,
                           required=False,
                           default='../data/lists/Module.txt',
                           help='specify serial nubmer list file name')
    argparser.add_argument('-v', '--verbose', required=False,
                           default=False,action='store_true',
                           help='use this option to dump stage name')
    return argparser.parse_args()


def get_json():
    argparser = ArgumentParser()
    args = get_option(argparser)
    l_Module_SN = args.serialNumberlist
    debug = args.verbose
    chst=localDBtools.LocalDBtools()

    with Path(l_Module_SN).open(encoding="utf-8") as f:
        l_Module_vol=[]
        l_Module_cur=[]
        l_checked_Module_SN=[]
        for line in f.readlines():
            i_Module_SN=line.replace("\n","")
            l_checked_Module_SN.append(i_Module_SN)
            i_module_json = chst.get_ModuleIVData(i_Module_SN,debug)
            
            if i_module_json is None:
                    print(f"{i_Module_SN} IV Data is null")
            else:
                with open(f"../data/json/Module/{i_Module_SN}.json", 'w', encoding='utf-8') as f:
                    json.dump(i_module_json, f, ensure_ascii=False, indent=4)
                    print(f"Module : {i_Module_SN} Listed!!")
    
            
         
    

if __name__ == "__main__":
    mklist()
    get_json()
    