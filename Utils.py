#!/usr/bin/env python
# -*- coding: utf-8 -*-
import TestSupport
from PyQt5.QtCore import *
import collections
import sqlite3
from MapData import *
from station import *

class Utils(QObject):
    trackDraw = pyqtSignal(float,float,float,int,int,int,str,float,str,str,int,int,str,
                           arguments=['x','y','length','id_track','index','isswitch','direction','scale','tname',
                                      'switch_button_name','switch_ud','py_id','ramp'])
    showTrackName = pyqtSignal(float,float,str,arguments=['x','y','tname'])
    axleDraw = pyqtSignal(float, float,arguments=['x', 'y'])
    platformDraw = pyqtSignal(float, float , int ,str ,int, int, int ,arguments=['x', 'y','pdir','pname','id_plat','pindex','p_id'])
    signalerDraw = pyqtSignal(float, float,str,arguments=['x', 'y','signaler_name'])
    signalLampDraw = pyqtSignal(float, float, str,str,str,int,str,int,float,arguments=['x', 'y','count','poles','sname','lamp_id','iswhite','sindex','slength'])
    turnOutDraw =  pyqtSignal(float, float,float,float,int,int,int,str,int,arguments=['x', 'y','l','h','tuindex','sdir','updown','tname','position'])
    trackChange = pyqtSignal(int,int,arguments=['tindex','status'])
    platFormChange = pyqtSignal(int,int,int,arguments=['pindex','door_status','llamp_status'])
    signalStatusChange = pyqtSignal(int,int,int,int,arguments=['sindex','lamp_one','lamp_three','lamp_two'])
    createTrain = pyqtSignal(int,float,int,float,int,str,float,arguments=['head_index','head_pos','tail_index','tail_pos','train_index','train_id','train_len'])
    updateTrainPosition = pyqtSignal(int,float,int,float,int,int,str,float,int,arguments=['head_index','head_pos','tail_index','tail_pos','train_index','door_status','train_show_msg','train_len','trainid'])
    updateSwitchSataus = pyqtSignal(int,int,int,arguments = ['sindex','code','tindex'])
    deleteTrainObject = pyqtSignal(int,arguments = ['tindex'])
    showHideTrainInformation = pyqtSignal(int,int,arguments = ['tindex','tag'])
    turnOutTwoDraw = pyqtSignal(float, float,float,float,int,int,int,arguments = ['x', 'y','l','h','tuindex','sdir','updown'])
    def __init__(self,a):
        super().__init__()
        self.tag1 = False;
        self.tag2 = False;
        self.map_list = {};
        self.tag1 = True;

        self.station_list = {}#collections.OrderedDict()
        self.track_list = {}#collections.OrderedDict()
        self.balise_list = {}
        self.balise_list = {}
        self.platform_list = {}
        self.slop_list = {}
        self.signal_list = {}

        self.initAllDict()
        self.initTrackInfo()

        self.train_ID_list = {};
        self.trackArray = {};
        self.platArray = {};
        self.singnalArray = {};
        self.switchArray = {};
        self.trackSwitchArray = {};
        self.sindex = 0;
        self.train_index = 0;
        self.station_chart = Station_chart();
        self.drawStationMap();
        # 信号槽链接 从station_chart()中接收udp的接收到的数据
        self.station_chart.sendTrackStatusData.connect(self.receiveTrackData);
        self.station_chart.sendTrainStatusData.connect(self.receiveTrainData);
        self.station_chart.sendSignalStatusData.connect(self.receiveSignalData);
        self.station_chart.sendSwitchStatusData.connect(self.receiveSwitchData);
        self.station_chart.sendSignalCiStatusData.connect(self.receiveSignalCiData);
        self.station_chart.sendPsdStatusData.connect(self.receivePsdStatusData);
        self.station_chart.sendMsg.connect(self.receiveMsg)

    def receiveMsg(self, str):
        msg_box = QMessageBox(QMessageBox.Warning, "ATE Msg!!!", str)
        msg_box.exec()

    def qmlInitReady(self):
        self.tag2 = True;
        self.drawStationMap()

    @pyqtSlot(str,int)
    def switchButtonClick(self,sname,code):
        self.station_chart.qqjbtn(sname,code)

    @pyqtSlot(int)
    def deleteTrain(self,trainid):
        print("delete train id",trainid,self.train_ID_list)
        self.deleteTrainObject.emit(self.train_ID_list[str(trainid)])
        if str(trainid) in self.train_ID_list:
            self.train_ID_list.pop(str(trainid))
        else:
            pass
        print("train_ID_list",self.train_ID_list,self.station_chart.carnameList)
        self.station_chart.deleteTrainCmd(trainid)
        if str(trainid) in self.station_chart.carnameList:
            self.station_chart.carnameList.remove(str(trainid))

    @pyqtSlot(str)
    def forceMove(self,trainid):
        self.station_chart.forceMove(int(trainid))
    
    @pyqtSlot(str)
    def showTrainInfo(self,trainid):
        self.showHideTrainInformation.emit(self.train_ID_list[trainid],1)

    @pyqtSlot(str)
    def hideTrainInfo(self,trainid):
        self.showHideTrainInformation.emit(self.train_ID_list[trainid],0)

    @pyqtSlot(str,int,int)
    def send_command_toSc(self,type,command,status):
        print("send_command_toSc",type,command,status)
    #接收到Track的状态数据并传给track 处理
    def receiveTrackData(self, trackData):
        print("trackData",trackData)
    
    #更新列车位置
    def receiveTrainData(self, traindata):
        print(traindata)
    # 列车信息

    
    # 接收到signal的状态数据并发个signal解析处理
    def receiveSignalData(self,signalData):
       print(signalData)

    # 接收到switch的状态数据解析并处理
    def receiveSwitchData(self,switchData):
        print("switchData", switchData,self.switchArray,self.trackSwitchArray)

    #接收SignalCi 数据 不做处理
    def receiveSignalCiData(self,signalciData):
        #print("signalciData  ",signalciData)
        pass

    # 接收到psd的状态数据并传给plat处理
    def receivePsdStatusData(self,psdData):
        print("psdData",psdData,self.platArray)


    def drawStationMap(self):
        if self.tag1 == True and self.tag2 ==True:
            tindex = 0
            pindex = 0
            for track in self.map_list:
                track_x = self.map_list[track][1][0]
                track_y = self.map_list[track][1][1]
                track_l = self.map_list[track][1][2]
                #创建track
                slop = ""
                self.trackDraw.emit(track_x,track_y,track_l,int(self.map_list[track][2][0],16),tindex,int(self.map_list[track][0][3]),
                                    self.map_list[track][0][2],self.map_list[track][0][1],track,self.map_list[track][0][4],
                                    TRACK_NAME_UP_DOWN,int(self.map_list[track][2][2],16),slop)
                self.trackArray[track] = tindex
                tindex = tindex + 1
                if self.map_list[track][0][7]== "1":
                    self.showTrackName.emit(track_x +(track_l - 36)/2,track_y + 10 +12 +12,track)
                elif self.map_list[track][0][7]== "0":
                    self.showTrackName.emit(track_x +(track_l - 36)/2,track_y - 10 - 12 -12,track)
                else:
                     pass

                #创建道岔 1 上 -1 位置下方
                if self.map_list[track][0][3]== '3': # 道岔在左边还是右边
                   self.trackArray[self.map_list[track][0][4]] = tindex
                   self.switchArray[self.map_list[track][0][4]] = [tindex,track]
                   self.trackSwitchArray[track] = self.map_list[track][0][4]
                   self.turnOutDraw.emit(track_x,track_y,21,(TRACK_TWO_SPACE- 8)/2,tindex,-1,int(self.map_list[track][0][6]),self.map_list[track][0][4],0)
                   tindex = tindex + 1
                elif self.map_list[track][0][3]== '4': # 道岔在左边还是右边
                   self.trackArray[self.map_list[track][0][4]] = tindex
                   self.switchArray[self.map_list[track][0][4]] = [tindex,track]
                   self.trackSwitchArray[track] = self.map_list[track][0][4]
                   self.turnOutDraw.emit(track_x + 21,track_y,21,(TRACK_TWO_SPACE- 8)/2,tindex,-1,int(self.map_list[track][0][6]),self.map_list[track][0][4],1)
                   tindex = tindex + 1

                elif self.map_list[track][0][3]== '1':
                   self.trackArray[self.map_list[track][0][4]] = tindex
                   self.turnOutDraw.emit(track_x,track_y,track_l - 15,TRACK_TWO_SPACE,tindex,1,int(self.map_list[track][0][6]),self.map_list[track][0][4],0)
                   self.switchArray[self.map_list[track][0][4]] = [tindex,track]
                   self.trackSwitchArray[track] = self.map_list[track][0][4]
                   tindex = tindex + 1
                else:
                    pass

                #创建计轴
                if self.map_list[track][0][5] == '1':
                    self.axleDraw.emit(track_x - 24 / 2 -2,track_y - 6)
                elif self.map_list[track][0][5] == '2':
                    self.axleDraw.emit(track_x + track_l - 24 / 2 +2, track_y - 6)
                else:
                    pass

                #创建信号机
                if self.balise_list.get(track) != None:
                    for child in self.balise_list[track]:
                        self.signalerDraw.emit(track_x + child[1]/100,track_y + 8,child[0])
                else:
                    pass
                #
                if self.signal_list.get(track)!=None:
                    self.analyseLampDict(track_x,track_y,track_l,self.signal_list[track],self.map_list[track][0][1])
                else:
                    pass
                # #创建站台
                if self.platform_list.get(track) != None:
                    if self.platform_list[track][1] == '0x55':
                        self.platformDraw.emit(track_x + (track_l -104)/2,track_y - 36 - 6 - 40,1,self.platform_list[track][0],
                                               int(self.platform_list[track][2],16),pindex,self.platform_list[track][3])
                    elif self.platform_list[track][1] == '0xAA':
                        self.platformDraw.emit(track_x + (track_l -104)/2, track_y + 8 + 6 + 40,2,self.platform_list[track][0],
                                               int(self.platform_list[track][2],16),pindex,self.platform_list[track][3])
                    else:
                        pass
                    self.platArray[str(int(self.platform_list[track][2],16))] = pindex
                    pindex = pindex + 1
                else:
                    pass
        else:
            pass

    # 创建信号灯 信号灯名0, id1, 上下2,  信号灯个数3,  信号柱位置4, 信号灯位置5, 是否为白灯6]
    def analyseLampDict(self,x,y,track_l,lamp_list,scale):
        for signalLamp in lamp_list:
            # 信号灯 上下位置 1 上 2 下
            if signalLamp[3] == '0xAA':
                pos_y = y - 12 - 6
            elif signalLamp[3] == '0x55':
                pos_y = y + 12 + 8
            else:
                pass

            lamp_length = 44
            # #信号柱位置 1 左 2 右
            lamp_length = lamp_length - 4 - (3 - int(signalLamp[4])) * 12
            #信号灯位置加上信号灯长度大于轨道长度 靠右对齐
            if signalLamp[2]*scale/100 + lamp_length > track_l:
                pos_x = x + track_l - lamp_length
            else:
                pos_x = x +signalLamp[2]*scale/100
            #['V0305', '0x03400305', '1', '3', '2', 0.0, '']
            self.signalLampDraw.emit(pos_x, pos_y, signalLamp[4], signalLamp[5], signalLamp[1],int(signalLamp[0],16),signalLamp[6],self.sindex,lamp_length)
            self.singnalArray[signalLamp[1]] = self.sindex
            self.sindex = self.sindex +1

    def initAllDict(self):
        self.opendb()

        s_list = self.query_all1('select t_index,t_name,t_scale,t_direction,switch_type,switch_name,alxe_pos,switch_pos,tname_pos from stationmap')
        for child in s_list:
            self.station_list[child[0]] = [child[1],child[2],child[3],child[4],child[5],child[6],child[7],child[8]]

        t_list = self.query_all('select name ,id,len,physical_id from track')
        for child in t_list:
            self.track_list[child[0]] = child[1],child[2],child[3]

        p_list = self.query_all('select track_name,name,station_dir,esb_id,id from station')
        for child in  p_list:
            self.platform_list[child[0]] = [child[1],child[2],child[3],int(child[4])]
        self.closedb()

    def opendb(self):
        self.con = sqlite3.connect('data/ga_psldata.db')
        self.cur = self.con.cursor()

        self.con1 = sqlite3.connect('data/ga_station.db')
        self.cur1 = self.con1.cursor()

    def query_all(self, cmd):
        self.cur.execute(cmd)
        total = self.cur.fetchall()
        return total

    def query_all1(self, cmd):
        self.cur1.execute(cmd)
        total = self.cur1.fetchall()
        return total

    def closedb(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

        self.cur1.close()
        self.con1.commit()
        self.con1.close()

    # 初始化线路上track的位置 遍历停车场new_list对返回的track的位置等信息增加到new_list 并把属于道岔的track信息记录到self.switch_list
    def initTrackInfo(self):
        for list_child in self.station_list:
            a = self.station_list[list_child]
            b = self.gettrackpos(list_child, TRACK_BEGIN_X, TRACK_BEGIN_Y, self.station_list)
            c = self.getTrackInformation(self.station_list[list_child][0])
            self.map_list[self.station_list[list_child][0]] = [a,b,c]

    # 计算返回线路上track的位置 '0,0': ['LT0203', 1, '0', '', '', '2'],
    def gettrackpos(self, list, init_x, init_y, track_dict):
        pos = []
        # 将字符串初始化为列表['0','0']
        key = list.split(",")
        #track 的实际长度 * 缩放倍数
        track_l = self.gettrackLength(track_dict[list][0]) * track_dict[list][1]
        length = 0
        if key[1] == '0':
            pos.append(init_x)
        else:
            while key[1] != '0':
                key[1] = str(int(key[1]) - 1)
                list = ",".join(key)
                name = track_dict[list]
                length = length + self.gettrackLength(name[0]) * track_dict[list][1] + TRACK_SPACE
            pos.append(length + init_x)
        pos_y = init_y + int(key[0]) * TRACK_TWO_SPACE
        pos.append(pos_y)
        pos.append(track_l)
        return pos

    # 从psl 获取track长度,ID,信号机列表,信号灯列表,站台门列表
    def getTrackInformation(self, name):
        info = []
        info.append(self.track_list[name][0])
        info.append(self.track_list[name][1])
        info.append(self.track_list[name][2])
        return info

    # 传入track位置 获取track 名称 如 [0,0] 返回T0102
    def gettrackLength(self, name):
        return self.track_list[name][1]/100;