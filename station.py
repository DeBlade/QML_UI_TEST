#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import *
import threading
import time
import MapData as staConf

class Station_chart(QtCore.QObject):
    sendTrackStatusData = pyqtSignal(dict)
    sendTrainStatusData = pyqtSignal(dict)
    sendSignalStatusData = pyqtSignal(dict)
    sendSwitchStatusData = pyqtSignal(dict)
    sendSignalCiStatusData = pyqtSignal(dict)
    sendPsdStatusData = pyqtSignal(dict)
    #sendBaliseStatusData = pyqtSignal(dict)
    sendMsg = pyqtSignal(str)

    def __init__(self):
        super(Station_chart, self).__init__()

        self.receiveData = None
        self.trackTemp = None
        self.lampTemp = None
        self.objMSGList = None
        self.addCarList = None
        self.establish_route_list = None
        self.switchCmdList = None
        self.trainTemp = None
        self.switchTemp = None
        self.signalCiTemp = None
        self.psdData = None
        self.psdTemp = None
        #self.baliseTemp = None

        self.trigerButtonData = None
        self.setsignalDate = None
        self.trackData = None
        self.carnameList = []

        # self.push_client = push_client()

    def clearReceiveDataTemp(self):
        if self.trainTemp != None:
            self.trainTemp.clear()
        if self.trackTemp != None:
            self.trackTemp.clear()

    def update_stationchart(self,receiveData):
        if receiveData is not None:
            for key in sorted(receiveData):
                if key == 'track':
                    if receiveData['track'] == None or receiveData['track'] == {} or receiveData['track'] ==self.trackTemp:
                        pass
                    else:
                        self.trackTemp = receiveData['track']
                        self.sendTrackStatusData.emit(self.trackTemp)
                elif key == 'train':
                    if receiveData['train'] == None or receiveData['train'] == {} or receiveData['train'] == self.trainTemp:
                        pass
                    else:
                        self.trainTemp = receiveData['train']
                        self.sendTrainStatusData.emit(self.trainTemp)
                elif key == 'signal':
                    if receiveData['signal'] == None or receiveData['signal'] == {} or receiveData['signal'] == self.lampTemp:
                        pass
                    else:
                        self.lampTemp = receiveData['signal']
                        self.sendSignalStatusData.emit(self.lampTemp)
                elif key == 'switch':
                    if receiveData['switch'] == None or receiveData['switch'] =={} or receiveData['switch'] == self.switchTemp:
                        pass
                    else:
                        self.switchTemp = receiveData['switch']
                        self.sendSwitchStatusData.emit(self.switchTemp)

                elif key == 'signal_ci':
                    if receiveData['signal_ci'] == None or receiveData['signal_ci'] =={} or receiveData['signal_ci'] == self.signalCiTemp:
                        pass
                    else:
                        self.signalCiTemp = receiveData['signal_ci']
                        self.sendSignalCiStatusData.emit(self.signalCiTemp)

                elif key == 'station':
                    if receiveData['station'] == None or receiveData['station'] =={} or receiveData['station'] == self.psdTemp:
                        pass
                    else:
                        self.psdTemp = receiveData['station']
                        self.sendPsdStatusData.emit(self.psdTemp)

    # def receive_psl(self):
    #     self.sub_client = sub_client("station", self.call_back)

    def call_back(self, type, data):
        receiveData = pickle.loads(data)
        if receiveData != None or receiveData != {}:
            if isinstance(receiveData,dict):
                self.update_stationchart(receiveData)
            elif isinstance(receiveData,str):
                self.sendMsg.emit(receiveData)
            else:
                print("receiveData",receiveData)
        else:
            print("receiveData is None")

    def clean_msg(self):
        time.sleep(3)

    def addCarMenu(self,str_trainID,str_routeID,str_trackID,offs,len, head_dir, tail_dir,track_len=80):
        print("----add a car")
        print(str_trainID, str_routeID,str_trackID, offs, len)
        if int(str_trainID) <= 0 or int(str_trainID) >30 or str_trainID in self.carnameList :
            msg = "请检查参数"
            self.sendMsg.emit(msg)
        else:
            if offs > track_len or offs < cfg.CAR_LEN:
                msg = "请检查参数：位置偏移需大于20,小于区段长度"+str(track_len)
                self.sendMsg.emit(msg)
            else:
                print("加车成功")
                self.carnameList.append(str_trainID)
                self.addCarList = ['add_car', str_trainID, str_routeID, str_trackID, offs, len, head_dir,
                                   tail_dir]
                self.push_client.send("psl_cmd", self.addCarList)


    def establish_route_cmd(self, rout_name, routeID, init_signal_id, end_signal_id):
        print("establish_route_cmd",rout_name, routeID, init_signal_id, end_signal_id)
        self.establish_route_list = ['establish_route', rout_name, routeID, init_signal_id, end_signal_id]
        self.push_client.send("psl_cmd", self.establish_route_list)

    def establishAllRoute(self):
        self.establish_allroute_list = ['establish_allroute']
        self.establish_allroute_list.extend(staConf.temp_list)
        print(self.establish_allroute_list)
        self.push_client.send("psl_cmd", self.establish_allroute_list)

    def cancel_route_cmd(self, rout_name, routeID, init_signal_id, end_signal_id):
        print('cancel_route_cmd',rout_name, routeID, init_signal_id, end_signal_id)
        self.cancel_route_list = ['cancel_route', rout_name, routeID, init_signal_id, end_signal_id]
        self.push_client.send("psl_cmd", self.cancel_route_list)

    def cmdsend(self,type,id):
        print('cmdsend',type,id)
        self.cmdsendlist = ['cmdsend',type,id]
        self.push_client.send("psl_cmd", self.cmdsendlist)

    def leadRoute(self,type,id,init_signal_id, end_signal_id):
        print('leadRoute',type,id,init_signal_id, end_signal_id)
        self.lead_route_list = ['leadroute',type,id]
        self.push_client.send("psl_cmd", self.lead_route_list)

    def cancel_route_cmd_byp(self, rout_name, routeID, init_signal_id, end_signal_id):
        print('cancel_route_cmd_byp',rout_name, routeID, init_signal_id, end_signal_id)
        self.cancel_route_list_p = ['cancel_route_people', rout_name, routeID, init_signal_id, end_signal_id]
        self.push_client.send("psl_cmd", self.cancel_route_list_p)

    def cancel_route_all(self):
        print('cancel_route_all')
        self.cancel_allroute_list = ['cancel_allroute']
        self.cancel_allroute_list.extend(staConf.temp_list)
        print(self.cancel_allroute_list)
        self.push_client.send("psl_cmd", self.cancel_allroute_list)


    def establish_route_all(self, routeID_2, routeID_3, routeID_4, routeID_5):
        print('establish_route_all',routeID_2, routeID_3, routeID_4, routeID_5)
        self.establish_route_all_list = ['establish_route_all', routeID_2, routeID_3, routeID_4, routeID_5]
        self.push_client.send("psl_cmd", self.establish_route_all_list)

    def changeSwitch(self,switch_name,switch_cmd):
        print('changeSwitch',switch_name,switch_cmd)
        self.switchCmdList = ['switch_cmd', switch_name,switch_cmd]
        print(self.switchCmdList)
        self.push_client.send("psl_cmd", self.switchCmdList)

    def autoButton(self,buttonID, state):
        print("----Auto Triger", buttonID, state)
        self.trigerButtonData = ['autoButton',buttonID, state]
        self.push_client.send("psl_cmd", self.trigerButtonData)

    def changeSignal(self, signalID, state):
        print('setSignal',signalID,state)
        self.setsignalDate = ['setSignal', signalID, state]
        self.push_client.send("psl_cmd", self.setsignalDate)

    def changeSignalp(self, signalID, state):
        print('changeSignalp',signalID, state)
        self.setsignalpDate = ['changeSignalp', signalID, state]
        self.push_client.send("psl_cmd", self.setsignalpDate)

    def emgButton(self, psdID, state):
        print('emgButton',psdID,state)
        self.setemgDate = ['emgButton', psdID, state]
        self.push_client.send("psl_cmd", self.setemgDate)

    def qqjbtn(self, name, state):
        print('qqjbtn',name, state)
        setData = ['switch_qqj', name, state]
        self.push_client.send("psl_cmd", setData)

    def switchsetting(self, name, state):
        print('switchsetting',name,state)
        setData = ['switchsetting', name, state]
        self.push_client.send("psl_cmd", setData)

    def changeTrack(self, trackID, state):
        print('changeTrack',trackID, state)
        self.trackData = ['setTrack', trackID, state]
        self.push_client.send("psl_cmd", self.trackData)

    def testNet(self, num):
        print('testNet',num)
        self.testNetData = ['testNet',num]
        self.push_client.send("psl_cmd", self.testNetData)

    def setBalise(self, id,color,num,id_num,balise_len,balise_objs):
        print('setBalise',id,color,num,id_num,balise_len)
        if id not in balise_objs or color not in range(0, 11) or num not in [0, 1]:
            msg = "应答器设置失败1，请检查参数"
            self.sendMsg.emit(msg)
        else:
            try :
                # balise_objs[id][1].changeSignalerToBlue()
                a = id_num%0b11111111111111 + 2
                if a >= 2:
                    if balise_len <= (balise_objs[id][1].length / balise_objs[id][1].scale):
                        self.setBaData = ['setBalise', id,color,num,int(id_num),balise_len]
                        self.push_client.send("psl_cmd", self.setBaData)
                        msg = "应答器设置成功"
                        self.sendMsg.emit(msg)
                    else:
                        msg = "应答器设置失败4，请检查参数"
                        self.sendMsg.emit(msg)
                else:
                    msg = "应答器设置失败2，请检查参数"
                    self.sendMsg.emit(msg)
            except:
                msg = "应答器设置失败3，请检查参数"
                self.sendMsg.emit(msg)

    def injectBalise(self, balise_id, trian_id):
        self.baliseData = ['injectBalise', balise_id, trian_id]
        self.push_client.send("psl_cmd", self.baliseData)

    def setRoutestate(self, rout_name, routeID,num):
        print('setRoutestate',rout_name, routeID,num)
        self.setRoData = ['setRoutestate', rout_name, routeID, num]
        self.push_client.send("psl_cmd", self.setRoData)

    def bypassButton(self,psdID, num):
        print('bypassButton',psdID, num)
        self.setbpbData = ['setbypassstate', psdID, num]
        self.push_client.send("psl_cmd", self.setbpbData)

    def changePSD(self, PSDID, code):
        print('changePSD', PSDID, code)
        self.PSDData = ['setPSD', PSDID, code]
        self.push_client.send("psl_cmd", self.PSDData)

    def changeTrain(self, trainID, integrity):
        print('changeTrain', trainID, integrity)
        self.TINData = ['setTrainIn', trainID, integrity]
        self.push_client.send("psl_cmd", self.TINData)


    def changeTrainDoor(self, trainID, door):
        print('changeTrainDoor', trainID, door)
        self.TDOORData = ['setTrainDoor', trainID, door]
        self.push_client.send("psl_cmd", self.TDOORData)

    def autoTrigger(self,routeID):
        print('autoTrigger', routeID)
        sendList = ['autoTrigger',routeID]
        self.push_client.send("psl_cmd", sendList)

    def cancelAutoTrigger(self,routeID):
        print('cancelAutoTrigger', routeID)
        sendList = ['cancelAutoTrigger',routeID]
        self.push_client.send("psl_cmd", sendList)

    def autoPass(self,routeID):
        print('autoPass', routeID)
        sendList = ['autoPass',routeID]
        self.push_client.send("psl_cmd", sendList)

    def cancelAutoPass(self,routeID):
        print('cancelAutoPass', routeID)
        sendList = ['cancelAutoPass',routeID]
        self.push_client.send("psl_cmd", sendList)

    def deleteTrainCmd(self, trainID):
        print('deleteTrainCmd', trainID)
        sendList = ['deleteTrainCmd', trainID]
        self.push_client.send("psl_cmd", sendList)

    def pulsePcSet(self,trainId, isStopChecked, isAdcChecked,adc1,adc2,isDirChecked,dir1,dir2,dirnum,isNumChecked,num1,num2,numnum):
        print("pulsePcSet", trainId, isStopChecked,isAdcChecked,adc1,adc2,isDirChecked,dir1,dir2,dirnum,isNumChecked,num1,num2,numnum)
        sendList = ['pulseSetCmd', "PC", trainId, isStopChecked,isAdcChecked,adc1,adc2,isDirChecked,dir1,dir2,dirnum,isNumChecked,num1,num2,numnum]
        self.push_client.send("psl_cmd", sendList)

    def pulseScSet(self,trainId, isStopChecked, isSpeedChecked, speed1, speed2, speed3, speed4, speednum,isPhaseChecked, phase12_1, phase12_2, phase34_1, phase34_2, phasenum):
        print("pulseScSet", trainId, isStopChecked,isSpeedChecked, speed1, speed2, speed3, speed4, speednum,isPhaseChecked, phase12_1, phase12_2, phase34_1, phase34_2, phasenum)
        sendList = ['pulseSetCmd', "SC", trainId, isStopChecked,isSpeedChecked, speed1, speed2, speed3, speed4, speednum,isPhaseChecked, phase12_1, phase12_2, phase34_1, phase34_2, phasenum]
        self.push_client.send("psl_cmd", sendList)

    def wheelDiameterSet(self,trainId, wheelDiameter):
        print("wheelDiameterSet", trainId, wheelDiameter)
        sendList = ['wheelDiameterSetCmd', trainId, wheelDiameter]
        self.push_client.send("psl_cmd", sendList)
        msg = "轮径值设置成功"
        self.sendMsg.emit(msg)

    def btmSet(self,trainId, isStopChecked, isVersionChecked, version):
        print("btmSet", trainId, isStopChecked, isVersionChecked, version)
        sendList = ['btmSetCmd', trainId, isStopChecked, isVersionChecked, version]
        self.push_client.send("psl_cmd", sendList)

    def changeSPKS(self, status):
        print('changeSPKS', status)
        sendList = ['setSPKS', status]
        self.push_client.send("psl_cmd", sendList)
