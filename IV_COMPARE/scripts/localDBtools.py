import datetime
from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
import pprint
import copy
import sys
import os
import json
from bson import json_util
import logging
import traceback
from pathlib import Path
import jsonschema
from datetime import date, datetime

#sys.path.append("/home/itkqc/localdb-tools")
#from viewer.pages.qc import recycle_analysis_core
#from viewer.functions.common import create_message

logger = logging.getLogger("localdb")


class LocalDBtools():
    def __init__(self):
        try:
#            client = MongoClient(host='atlasdb01.kek.jp', port=27017)
            client = MongoClient(host='127.0.0.1', port=27017)
            self.localDB = client.localdb
            self.localDBtools = client.localdbtools
        except:
            print("cannot connect to localDB")

    def parse_json(self,data):
        return json.loads(json_util.dumps(data))
    
    def checkStage(self, sn, stage):
        component = self.localDB.component.find_one({'serialNumber': sn})
        qcStatus = self.localDB.QC.module.status.find_one({"component": str(component["_id"])})
        if qcStatus['currentStage'] != stage :
            print(sn," : change stage from ",qcStatus['currentStage']," to ",stage)
            self.localDB.QC.module.status.update_one(
                {"component": str(component["_id"])},
                {'$set': {'currentStage':stage}}
            )
        else :
            print(sn," : current stage is already  ",stage)



    def reanalyseTestData(self, sn,stages,debug):
        component = self.localDB.component.find_one({'serialNumber': sn})
        if component == None :
            print(sn,"\t","not pulled yet")
            exit(1)
        qcStatus = self.localDB.QC.module.status.find_one(
            {"component": str(component["_id"])}
        )
        #pprint.pprint(qcStatus.get('QC_results'))

        for stage in stages:
            for key, val in  qcStatus.get('QC_results').get(stage).items():
                if val == "-1":
                    print("NoData")
                    continue
                else :

                    res=recycle_analysis_core(self,val)
                    return res

    def getBMIVData(self, sn,  debug):
        stage='BAREMODULERECEPTION'
        component= self.localDB.component.find_one({'serialNumber': sn})
        if component == None :
            print(sn,"\t","not pulled yet")
            exit(1)
            #return 0
            #raise ValueError("Negative value encountered.")
        
        if debug:
            pprint.pprint(component)
            print('*******************************************')

        qcStatus = self.localDB.QC.module.status.find_one(
            {"component": str(component["_id"])}
        )
        val=qcStatus.get('QC_results').get(stage).get('BARE_MODULE_SENSOR_IV')
        if debug :
            print("==QC_resutls==")
            pprint.pprint(val)

        if val == "-1":
            a={}
            sensn=0
            #return {}, {}
        else:
            test = self.localDB.QC.result.find_one({"_id": ObjectId(val)})
            testIV = self.localDB.QC.result.find_one({"_id": ObjectId(test['results']['LINK_TO_SENSOR_IV_TEST'])})
            if debug:
                print('*******************************************')
                print("!!!!! KUMAYAMA DEBUG !!!!!")
                pprint.pprint(testIV['prodDB_record']['components'][0]['serialNumber'])
                #print(json.dumps(testIV['prodDB_record']['components'], indent=4, ensure_ascii=False))
                print("!!!!! KUMAYAMA DEBUG !!!!!")
            if 'value' in testIV['results']:
                a=testIV['results'][value]
            else:
                a=testIV['results']

            if 'serialNumber' in testIV:
                sensn=testIV['serialNumber']
            elif 'components' in testIV['prodDB_record']:
                if 'serialNumber' in testIV['prodDB_record']['components'][0]:
                    sensn=testIV['prodDB_record']['components'][0]['serialNumber']
                else:
                    sensn=0
                    #None

            if debug :
                print("==IV result==")
                pprint.pprint(testIV)
                print("==sensor SN==")
                if sensn!=0:
                    print(sensn)

            
            if sensn!=0:
                sencomponent= self.localDB.component.find_one({'serialNumber': sensn})
                if component == None :
                    print(sn,"\t","not pulled yet")
                    exit(1)
                if debug:
                    pprint.pprint(sencomponent)
                senqcStatus = self.localDB.QC.module.status.find_one(
                    {"component": str(sencomponent["_id"])}
                )
                senval=senqcStatus.get('QC_results').get('sensor_manufacturer').get('IV_MEASURE')
                if debug :
                    print('===================sensor results===================')
                    #pprint.pprint(senval)
                sentestIV = self.localDB.QC.result.find_one({"_id": ObjectId(senval)})
                if debug :
                    print('===================sensor IV===================')
                    pprint.pprint(sentestIV)
                    #pprint.pprint(sentestIV['results'])



        if sensn!=0:
            #return testIV['results'],sentestIV['results']
            return a, sentestIV['results'], sensn
        else:
            #return a, sentestIV['results']
            return {}, {} #kumayama

    def getParameterValue(self, sn,compType, stage, testName, parName , debug):
        component= self.localDB.component.find_one({'serialNumber': sn})
        #print('parName = '+ parName)
        if component == None :
            #print(sn,"\t","not pulled yet")
            #exit(1)
            return 0
            #raise ValueError("Negative value encountered.")
        qcStatus = self.localDB.QC.module.status.find_one(
            {"component": str(component["_id"])}
        )
        if debug :
            print("==QC_resutls==")
            pprint.pprint(qcStatus.get('QC_results').get(stage))
        rawdata=[]
        for key, val in  qcStatus.get('QC_results').get(stage).items():
            if key == testName:
                if val == "-1":
                    #print("NoData",end="\t")
                    continue
                else :
                    test = self.localDB.QC.result.find_one({"_id": ObjectId(val)})
                    if debug:
                        pprint.pprint(test)
                    if "raw_id" in test:
                        if test["raw_id"] is not None:
                            raw = (
                                self.localDB.QC.testRAW.find_one({"_id": test["raw_id"]})
                                if test["raw_id"] is not None
                                else None
		            )
                            if debug:
                                pprint.pprint(raw['raw'][0])
                            rawdata=self.parse_json(raw['raw'][0])
                        else :
                            rawdata=test['results']
                                
                    else:
                        raw = None
        if rawdata:
            if debug :
                print("==rawdata==")
                pprint.pprint(rawdata)
            try:
                a=rawdata[parName]
            except:
                if 'results' in rawdata:
                    a=None
                    if parName in rawdata['results']:
                        #print('1')
                        a=rawdata['results'][parName]
                    if ('Measurements' in rawdata['results']) and (parName in rawdata['results']['Measurements']) and (a is None):
                        #a=rawdata['results']['metadata']['Measurement'][parName]
                        #print('2')
                        a=rawdata['results']['Measurements'][parName]
                    elif ('metadata' in rawdata['results']) and (parName in rawdata['results']['metadata']) and (a is None):
                        a=rawdata['results']['metadata'][parName]
                        #print('3')
                    elif ('metadata' in rawdata['results']) and (parName in rawdata['results']['metadata']['Measurement']) and (a is None):
                        a=rawdata['results']['metadata']['Measurement'][parName]
                        #print('4')
                    elif ('Metadata' in rawdata['results']) and ('Measurement' in rawdata['results']['Metadata']) and (parName in rawdata['results']['Metadata']['Measurement']) and (a is None):
                        a=rawdata['results']['Metadata']['Measurement'][parName]
                        #print('5')
                    elif a is None:
                        print('a is None.')
                elif parName in rawdata:
                    a=rawdata[parName]
                    #print('6')
                else:
                    a = 0

            #print(type(a))
            return a
        else :
            return 0


        
    def getTestData(self, sn, stages, debug):
        component = self.localDB.component.find_one({'serialNumber': sn})
        if component == None :
            print(sn,"\t","not pulled yet")
            exit(1)
        qcStatus = self.localDB.QC.module.status.find_one(
            {"component": str(component["_id"])}
        )
        #pprint.pprint(qcStatus.get('QC_results'))

        for stage in stages:
            for key, val in  qcStatus.get('QC_results').get(stage).items():
                if val == "-1":
                    #print("NoData",end="\t")
                    continue
                else :
                    #print("OK : ",val,end="\t")
                    test = self.localDB.QC.result.find_one({"_id": ObjectId(val)})
                    if "raw_id" in test:
                        if test["raw_id"] is not None:
                            raw = (
                                self.localDB.QC.testRAW.find_one({"_id": test["raw_id"]})
                                if test["raw_id"] is not None
                                else None
		            )
                            if debug:
                                pprint.pprint(raw['raw'][0])
                            rawdata=self.parse_json(raw['raw'][0])
                        else :
                            rawdata=test['results']

                    else:
                        raw = None
                    #pprint.pprint(raw['raw'][0])
                    #rawdata=self.parse_json(raw['raw'][0])
                    jsonfilename="../results/json"+sn+"_"+stage+"_"+key+".json"
                    with open(jsonfilename,'wt') as f:
                        res=json.dump(rawdata,f, indent=2,ensure_ascii=False)


            #print("")
        
        
    def checkStageTestData(self, sn, stages,debug):
        component = self.localDB.component.find_one({'serialNumber': sn})
        if component == None :
            print(sn,"\t","not pulled yet")
            exit(1)
        qcStatus = self.localDB.QC.module.status.find_one(
            {"component": str(component["_id"])}
        )
        #pprint.pprint(qcStatus.get('QC_results'))
        if debug :
            print("SerialNumber",end="\t")
            for stage in stages:
                #print(stage)
                for key, val in  qcStatus.get('QC_results').get(stage).items():
                    print(key,end="\t")
            print("")
                
        print(sn,end="\t")
        for stage in stages:
            #pprint.pprint(qcStatus.get('QC_results').get(stage).items())
            for key, val in  qcStatus.get('QC_results').get(stage).items():
                if val == "-1":
                    print("NoData",end="\t")
                else :
                    test = self.localDB.QC.result.find_one({"_id": ObjectId(val)})
                    #pprint.pprint(test)
                    if test['passed'] is True:
                        print("PASSED",end="\t")
                    else:
                        print("FAILED",end="\t")
        print("")
                    