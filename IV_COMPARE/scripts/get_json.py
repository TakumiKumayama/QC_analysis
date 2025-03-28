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

    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)

    l_Baremodule_SN = open('../data/lists/BareModule.txt', 'w')
    l_Module_Bare_sensor_SN = open('../data/lists/Module_Bare_sensor.txt', 'w')
    
    l_Module_Bare_sensor_SN.write(f"ModuleID\tModuleSN\tBaremoduleID\tSensorSN\n")
    
    for index, row in df.iterrows():
        i_Module_ID = row['module id']
        #wafer_lot = row['Sensor information sensor wafer lot ID']
        if mode==0:
            Batch_id = row['Batch ID']
        elif mode==1:
            Batch_id = row['Bare modules information Batch ID']

        i_Module_SN = row['ATLAS Serial Number for parts ATLAS SN (Module)']
        i_Bare_module_SN = row['ATLAS SN (BareModule)']
        i_sensor_SN = row['ATLAS SN (Sensor)']
        

        if not pd.isna(i_Module_SN):
            l_Baremodule_SN.write(f'{i_Bare_module_SN}\n')
            l_Module_Bare_sensor_SN.write(f'{i_Module_ID}\t{i_Module_SN}\t{i_Bare_module_SN}\t{i_sensor_SN}\n')
    


def get_option(argparser):
    argparser.add_argument('-l', '--serialNumberlist', type=str,
                           required=False,
                           default='../data/lists/BareModule.txt',
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
    l_Bare_SN = args.serialNumberlist
    debug = args.verbose
    do_plt = args.outputPlot
    chst=localDBtools.LocalDBtools()

    with Path(l_Bare_SN).open(encoding="utf-8") as f:
        for line in f.readlines():
            i_Bare_SN=line.replace("\n","")
            try:
                i_Bare_json, i_sen_json, i_sen_sn = chst.getBMIVData(i_Bare_SN,debug)
            except ValueError:
                print(f"samething is WRONG ...")
                continue
            
            with open(f"../data/json/BareModule/{i_Bare_SN}.json", 'w', encoding='utf-8') as f:
                json.dump(i_Bare_json, f, ensure_ascii=False, indent=4)
                print(f"BareModule : {i_Bare_SN} Listed!!")
                
            with open(f"../data/json/sensor/{i_sen_sn}.json", 'w', encoding='utf-8') as f:
                json.dump(i_sen_json, f, ensure_ascii=False, indent=4)
                print(f"Sensor : {i_sen_sn} Listed!!")
                
    return do_plt
                
                
                
def plot_IVCURVE():
    
    module_Info_path = "../data/lists/Module_Bare_sensor.txt"
    Info_df = pd.read_csv(module_Info_path, sep='\t')
    l_module_SN = Info_df['ModuleSN'].tolist()
    l_bare_SN = Info_df['BaremoduleID'].tolist()
    l_sensor_SN = Info_df['SensorSN'].tolist()
    
    l_checked_Module = []
    l_checked_Bare = []
    l_checked_sensor = []
    
    l_Not_registered_module = []    # Data has not yet been registered in the local database.
    
    with open("../data/results/Module_Jugde_result.list", "w") as f:
        f.write(f"ModuleSN\tBareModuleSN\tSensorSN\tMODULE_CUR_AT120\tBARE_CUR_AT120\tSEN_CUR_AT120\tMODULE_CRI1\tBARE_CRI1\tMODULE_CUR_PER_AREA\tBARE_CUR_PER_AREA\tMODULE_CRI2\tBARE_CRI2\n")
        for idx, i_module_SN in enumerate(l_module_SN):

            i_bare_SN = l_bare_SN[idx]
            i_sensor_SN = l_sensor_SN[idx]

        
            print("++++++++++ Module Info ++++++++++")
            print(f" Module     :  {i_module_SN}")
            print(f" Baremodule :  {i_bare_SN}")
            print(f" sensor     :  {i_sensor_SN}")
            #print("+++++++++++++++++++++++++++++++++")

            try:
                # Module Info
                i_module_df = pd.read_json(f"../data/json/Module/{i_module_SN}.json")
                l_module_vol = i_module_df["IV_ARRAY"]["voltage"]
                l_module_cur = i_module_df["IV_ARRAY"]["current"]
                l_module_sigmacur = i_module_df["IV_ARRAY"]["sigma current"]

                # Baremodule Info
                i_baremodule_df = pd.read_json(f"../data/json/BareModule/{i_bare_SN}.json")
                l_baremodule_vol = i_baremodule_df["IV_ARRAY"]["voltage"]
                l_baremodule_cur = i_baremodule_df["IV_ARRAY"]["current"]
                l_baremodule_sigmacur = i_baremodule_df["IV_ARRAY"]["sigma current"]

                # Sensor Info
                with open(f"../data/json/sensor/{i_sensor_SN}.json", 'r', encoding='utf-8-sig') as file:
                    i_sensor_content = file.read()
                i_sensor_dict = json.loads(i_sensor_content)
                l_sensor_vol = i_sensor_dict["IV_ARRAY"]["voltage"]
                l_sensor_cur = i_sensor_dict["IV_ARRAY"]["current"]
                l_sensor_sigmacur = i_sensor_dict["IV_ARRAY"]["sigma current"]

                plt.errorbar(l_module_vol, l_module_cur, yerr=l_module_sigmacur, fmt='o', capsize=3, label=f'Module {i_module_SN}', color='red')
                plt.errorbar(l_baremodule_vol, l_baremodule_cur, yerr=l_baremodule_sigmacur, fmt='s', capsize=3, label=f'Baremodule {i_bare_SN}', color='navy')
                plt.scatter(l_sensor_vol, l_sensor_cur, marker='^', label=f'Sensor {i_sensor_SN}', color='darkgreen')

                plt.title(f"{i_module_SN}")
                plt.xlabel('Voltage [V]')
                plt.ylabel('Current [uA]')

                plt.grid(True)
                plt.legend()
                plt.savefig(f"../data/img/{i_module_SN}.pdf")

                plt.clf()

                dir_result = evaluate_IVCURVE(l_module_vol, l_module_cur, l_baremodule_vol, l_baremodule_cur, l_sensor_vol, l_sensor_cur)
                
                i_module_cur_at120 = format(dir_result['MODULE_CUR_AT120'], ".4f")
                i_bare_cur_at120 = format(dir_result['BARE_CUR_AT120'], ".4f")
                i_sen_sur_at120 = format(dir_result['SEN_CUR_AT120'], ".4f")
                i_module_cri1 = dir_result['MODULE_CRI1']
                i_bare_cri1 = dir_result['BARE_CRI1']
                i_module_cur_area = format(dir_result['MODULE_CUR_PER_AREA'], ".4f")
                i_bare_cur_area = format(dir_result['BARE_CUR_PER_AREA'], ".4f")
                i_module_cri2 = dir_result['MODULE_CRI2']
                i_bare_cri2 = dir_result['BARE_CRI2']
                
                f.write(f"{i_module_SN}\t{i_bare_SN}\t{i_sensor_SN}\t{i_module_cur_at120}\t{i_bare_cur_at120}\t{i_sen_sur_at120}\t{i_module_cri1}\t{i_bare_cri1}\t{i_module_cur_area}\t{i_bare_cur_area}\t{i_module_cri2}\t{i_bare_cri2}\n")
                
                l_checked_Module.append(i_module_SN)
                l_checked_Bare.append(i_bare_SN)
                l_checked_sensor.append(i_sensor_SN)

            except FileNotFoundError:
                l_Not_registered_module.append(i_module_SN)
                print(f"{i_module_SN} has not yet been registered.")
                continue
        

def find_Vdep(l_vol):
    full_dep_vol = 70
    target_vol = full_dep_vol+50
    
    closest_idx = min(range(len(l_vol)), key=lambda i: abs(l_vol[i] - target_vol))
    return closest_idx


def evaluate_IVCURVE(l_module_vol, l_module_cur, l_bare_vol, l_bare_cur, l_sen_vol, l_sen_cur):
    
    dir_result = {}
    
    module_Vdep_idx = find_Vdep(l_module_vol)
    module_cur_at120 = l_module_cur[module_Vdep_idx]
    dir_result["MODULE_CUR_AT120"] = l_module_cur[module_Vdep_idx]
    
    bare_Vdep_idx = find_Vdep(l_bare_vol)
    bare_cur_at120 = l_bare_cur[bare_Vdep_idx]
    dir_result["BARE_CUR_AT120"] = l_bare_cur[bare_Vdep_idx]
    
    sen_Vdep_idx = find_Vdep(l_sen_vol)
    sen_cur_at120 = l_sen_cur[sen_Vdep_idx]
    dir_result["SEN_CUR_AT120"] = l_sen_cur[sen_Vdep_idx]
    
    # criteria1(I_{module, baremodule} < 2I_{sensor} @V_{dep}+50V)
    if(bare_cur_at120 < 2*sen_cur_at120):
        bare_cri1 = True
    else:
        bare_cri1 = False
        
    if(module_cur_at120 < 2*sen_cur_at120):
        module_cri1 = True
    else:
        module_cri1 = False
        
    dir_result["MODULE_CRI1"] = module_cri1
    dir_result["BARE_CRI1"] = bare_cri1
        
    # criteria2(I_{module, baremodule}[uA/cm^2] <  0.75 @V_{dep}+50V)
    sensor_size = 4.11*3.94 # [cm^2]
    
    module_cur_PerArea = module_cur_at120/sensor_size
    bare_cur_PerArea = bare_cur_at120/sensor_size
    
    dir_result["MODULE_CUR_PER_AREA"] = module_cur_PerArea
    dir_result["BARE_CUR_PER_AREA"] = bare_cur_PerArea
    
    if(module_cur_PerArea < 0.75):
        module_cri2 = True
    else:
        module_cri2 = False
    
    if(bare_cur_PerArea < 0.75):
        bare_cri2 = True
    else:
        bare_cri2 = False
        
    dir_result["MODULE_CRI2"] = module_cri2
    dir_result["BARE_CRI2"] = bare_cri2
        
    return dir_result
    
    

if __name__ == "__main__":
    
    mklist()
    do_plt = get_json()
    
    if(do_plt):
        plot_IVCURVE()
    