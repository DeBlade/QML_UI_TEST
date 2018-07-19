import QtQuick 2.3
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.0
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.2
import an.qt.Utils 1.0

Rectangle{
    id:mainWidow;
    visible: true;
    width: Screen.desktopAvailableWidth;
    height: Screen.desktopAvailableHeight;
    color: "black";


    property var trackArray:new Array();//存放轨道区段
    property var platformArray: new Array();//存放站台
    property var signalLampArray: new Array();//存放信号机
    property var switchArray: new Array();//存放道岔

    property var trainInfoArray: new Array();//列车显示信息
    
    property var trainHeadArray: new Array();//存放车头
    property var trainCenterArray: new Array();//存放车头
    property var trainTailArray: new Array();//存放车头

    property var train_head_png:"images/train_head.png";
    property var train_center_png:"images/train_center.png";
    property var train_center_open_png:"images/train_center_open.png";
    property var train_tail_png:"images/train_tail.png"; 

    property var train_hei : 14; //列车长度
    property var track_h : 8; //track高度

    MouseArea {//站场图缩放
           id: rootItemMouseArea
           enabled: true//rootItem.visible
           anchors.fill: parent;
           drag.target: station;
           drag.filterChildren: true;
           acceptedButtons: Qt.LeftButton | Qt.RightButton;
           onWheel: {
               if(wheel.angleDelta.y > 0){
                   station.scale = station.scale + 0.1;

               }
               else if(station.scale>0.1){
                   station.scale = station.scale - 0.1;

               }
               else{
                   station.scale = 0.1;
               }
           }
       }

    Utils  {
        id: uiutil;
    }

    Rectangle{
        id:station;
        width: parent.width;
        height: parent.height;
        color: "black";
        property Component trackCompent: null;
        property Component trackNameCompent: null;
        property Component platformCompent: null;
        property Component axleCompent: null;
        property Component signalerCompent: null;
        property Component signalLampCompent: null;
        property Component turnOutCompent: null;
        property Component turnOutTwoCompent: null;
        property Component trainHeadCompent :null;
        property Component trainCenterCompent :null;
        property Component trainTailCompent :null;
        property Component switchbuttonCompent :null;
        //函数 创建track
        function createTrack(x,y,length,id_track,index,isswitch,direction,scale,tname,py_id,ramp){
            if(station.trackCompent==null){
                 station.trackCompent = Qt.createComponent("track.qml");
             }
            var trackObj;
            if(station.trackCompent.status == Component.Ready)
            {
               trackObj =  station.trackCompent.createObject(station,{"x":x,"y":y})
               trackObj.m_l_track = length;
               trackObj.id_track = id_track;
               trackObj.isSwitch = isswitch;
               trackObj.track_direction = direction;
               trackObj.track_scale = scale;
               trackObj.utils = uiutil;
               trackObj.track_name = tname;
               trackObj.track_height = track_h;
               trackObj.py_id = py_id;
               trackObj.ramp = ramp
               trackArray[index] = trackObj;
            }
        }
        //函数 创建switchbutton
        function createSwitchbutton(x,y,sname){
            if(station.switchbuttonCompent==null){
                 station.switchbuttonCompent = Qt.createComponent("switchButton.qml");
             }
            var switchButtonObj;
            if(station.switchbuttonCompent.status == Component.Ready)
            {
               switchButtonObj =  station.switchbuttonCompent.createObject(station,{"x":x,"y":y});
               switchButtonObj.switch_name = sname;
               switchButtonObj.utils = uiutil;
            }
        }

        //函数 创建track 的显示信息
        function showName(x,y,tname){
            if(station.trackNameCompent==null){
                 station.trackNameCompent = Qt.createComponent("showname.qml");
             }
            var trackNameObj;
            if(station.trackNameCompent.status == Component.Ready)
            {
               trackNameObj =  station.trackNameCompent.createObject(station,{"x":x,"y":y});
               trackNameObj.tname = tname.toString();
            }
        }

        //函数 创建列车的显示信息
        function showTrainInformation(x,y,train_id,tIindex){
            if(station.trackNameCompent==null){
                 station.trackNameCompent = Qt.createComponent("showname.qml");
             }
            var trainInfoObj;
            if(station.trackNameCompent.status == Component.Ready)
            {
               trainInfoObj =  station.trackNameCompent.createObject(station,{"x":x,"y":y});
               trainInfoObj.tname = train_id.toString();
               trainInfoObj.shTag = false;
               trainInfoArray[tIindex] = trainInfoObj;
            }
        }

       //函数 创建信号
       function createSignalLamp(x,y,c,p,n,lamp_id,iswhite,sindex){
            if(station.signalLampCompent==null){
                 station.signalLampCompent = Qt.createComponent("signalLamp.qml");
             }
            var signalLampObj;
            if(station.signalLampCompent.status == Component.Ready)
            {
               signalLampObj =  station.signalLampCompent.createObject(station,{"x":x,"y":y});
               signalLampObj.lamp_count = c;
               signalLampObj.lamp_poles = p;
               signalLampObj.lamp_id = lamp_id;
               signalLampObj.iswhite = iswhite;
               signalLampObj.utils = uiutil;
               signalLampArray[sindex] = signalLampObj;
            }
        }

        //函数 创建站台门
        function createPlatform(x,y,d,n,id_plat,index,p_id){
              if(station.platformCompent == null){
                  station.platformCompent = Qt.createComponent("platform.qml");
              }
              var platformObj;
              if(station.platformCompent.status == Component.Ready){
                  platformObj = station.platformCompent.createObject(station,{"x":x,"y":y})
                  platformObj.top_bottom = d;
                  platformObj.plat_name = n;
                  platformObj.id_plat = id_plat;
                  platformObj.utils = uiutil;
                  platformObj.p_id = p_id;
                  platformArray[index] = platformObj
              }
         }

        //函数 创建计轴
        function createAxle(x,y){
             if(station.axleCompent==null){
                 station.axleCompent = Qt.createComponent("axle.qml");
              }
              var axleObj;
             if(station.axleCompent.status == Component.Ready)
             {
                 axleObj = station.axleCompent.createObject(station,{"x":x,"y":y})
             }

         }

        //函数 创建信号机
         function createSignaler(x,y,signaler_name){
             if(station.signalerCompent==null){
                 station.signalerCompent = Qt.createComponent("signaler.qml");
              }
              var axleObj;
             if(station.signalerCompent.status == Component.Ready)
             {
                 axleObj = station.signalerCompent.createObject(station,{"x":x,"y":y});
                 axleObj.signaler_name = signaler_name;
             }
         }

        //函数 创建道岔
        function createTurnOut(x,y,l,h,tuindex,sdir,updown,tname,position){
            if(station.turnOutCompent==null){
                station.turnOutCompent = Qt.createComponent("turnout.qml");
            }
            var turnOutObj;
            if(station.turnOutCompent.status == Component.Ready)
            {
                turnOutObj = station.turnOutCompent.createObject(station,{"x":x,"y":y});
                turnOutObj.m_l_track = l;
                turnOutObj.track_height = h;
                turnOutObj.sdir = sdir;
                turnOutObj.updown = updown;
                turnOutObj.tname = tname;
                turnOutObj.position = position;
                trackArray[tuindex] = turnOutObj;
                //console.log("sdir" ,tuindex,turnOutObj.sdir)
            }

        }

        //函数 创建车头
        function createTrainHead(x,y,train_index,train_png,train_id,train_length){
            if (station.trainHeadCompent ==null){
                station.trainHeadCompent = Qt.createComponent("train.qml");
            }
            var trainheadObj;
            if (station.trainHeadCompent.status == Component.Ready){
                trainheadObj = station.trainHeadCompent.createObject(station,{"x":x,"y":y});
                trainheadObj.train_png = train_png;
                trainheadObj.train_ID = train_id;
                trainheadObj.utils = uiutil;
                trainheadObj.train_label = false;
                trainheadObj.train_l = train_length;
                trainheadObj.train_h = train_hei;
                trainHeadArray[train_index] = trainheadObj;
            }
        }

        //函数 创建车中间
        function createTrainCenter(x,y,train_index,train_png,train_id,train_length){
            if (station.trainCenterCompent ==null){
                station.trainCenterCompent = Qt.createComponent("train.qml");
            }
            var traincenterObj;
            if (station.trainCenterCompent.status == Component.Ready){
                traincenterObj = station.trainCenterCompent.createObject(station,{"x":x,"y":y});
                traincenterObj.train_png = train_png;
                traincenterObj.train_ID = train_id;
                traincenterObj.utils = uiutil;
                traincenterObj.train_l = train_length;
                traincenterObj.trainTip = train_id.toString();
                trainCenterArray[train_index] = traincenterObj;
            }
        }

        //函数 创建车尾
        function createTrainTail(x,y,train_index,train_png,train_id,train_length){
            if (station.trainTailCompent ==null){
                station.trainTailCompent = Qt.createComponent("train.qml");
            }
            var traintailObj;
            if (station.trainTailCompent.status == Component.Ready){
                traintailObj = station.trainTailCompent.createObject(station,{"x":x,"y":y})
                traintailObj.train_png = train_png;
                traintailObj.utils = uiutil;
                traintailObj.train_label = false;
                traintailObj.train_ID = train_id;
                traintailObj.train_l = train_length;
                trainTailArray[train_index] = traintailObj;
            }
        }

        function swapTrainheadAndTail(head_index,tail_index,train_index,trainid){
            if (trackArray[head_index].track_direction == 0)
                if (trainid <50)
                    trainHeadArray[train_index].train_png = train_tail_png;
                else
                    trainHeadArray[train_index].train_png = train_head_png;
            else
                if (trainid <50)
                    trainHeadArray[train_index].train_png = train_head_png;
                else
                    trainHeadArray[train_index].train_png = train_tail_png;
            
            if (trackArray[tail_index].track_direction == 0)
                if (trainid <50)
                    trainTailArray[train_index].train_png = train_head_png;
                else
                    trainTailArray[train_index].train_png = train_tail_png;
            else
                if (trainid <50)
                    trainTailArray[train_index].train_png = train_tail_png;
                else
                    trainTailArray[train_index].train_png = train_head_png;
        }
    }

    //创建track
    Connections{
        target: uiutil;
        onTrackDraw:{
            station.createTrack(x,y,length,id_track,index,isswitch,direction,scale,tname,py_id,ramp);
        }
    }

    //创建站台
    Connections{
        target: uiutil;
        onPlatformDraw:{
            station.createPlatform(x,y,pdir,pname,id_plat,pindex,p_id);
            }
    }

    //创建计轴
    Connections{
        target: uiutil;
        onAxleDraw:{
            station.createAxle(x,y);
            }
    }

    //显示track名字
    Connections{
        target: uiutil;
        onShowTrackName:{
            station.showName(x,y,tname);
            }
    }

    //创建信号机
    Connections{
        target: uiutil;
        onSignalerDraw:{
            station.createSignaler(x,y,signaler_name);
            }
    }

    //创建信号灯
    Connections{
        target: uiutil;
        onSignalLampDraw:{
            station.createSignalLamp(x,y,count,poles,sname,lamp_id,iswhite,sindex);
            if (poles =='1')
                station.showName(x -36,y,sname);
            else
                station.showName(x + 48,y,sname);
            }
    }

    //更新track状态
    Connections{
        target: uiutil;
        onTrackChange:{
            if(status == 0)
                trackArray[tindex].changeTrackGray();
            else if (status == 1)
                trackArray[tindex].changeTrackRed();
            }
    }

    //更新站台
    Connections{
        target: uiutil;
        onPlatFormChange:{
            if(door_status == 0)
                platformArray[pindex].closeTheDoor();
            else if (door_status == 1)
                platformArray[pindex].openTheDoor_yellow();
            else if (door_status == 2)
                platformArray[pindex].openTheDoor();

            if(llamp_status == 0)
                platformArray[pindex].left_tag = false;
            else
                platformArray[pindex].left_tag = true;
        }
    }

    //创建道岔
    Connections{
        target: uiutil;
        onTurnOutDraw:{
            if (updown == 1){
                station.createTurnOut(x,y - h,l,h,tuindex,sdir,updown,tname,position);
            }
            else if (updown == -1){
                station.createTurnOut(x,y + track_h,l,h,tuindex,sdir,updown,tname,position);
            }
        }
    }

    //更新信号灯状态
    Connections{
        target: uiutil;
        onSignalStatusChange:{
            //console.log("zhao",sindex,lamp_one,lamp_three,lamp_two)
            signalLampArray[sindex].lamp_left_color = lamp_one;
            signalLampArray[sindex].lamp_center_color = lamp_two;
            signalLampArray[sindex].lamp_right_color = lamp_three;
        }
    }

    //更新道岔状态
    Connections{
        target: uiutil;
        onUpdateSwitchSataus:{

        }
    }

    //创建列车
    Connections{
        target: uiutil;
        onCreateTrain:{
            var head_pos_y = trackArray[head_index].y - train_hei;
            var tail_pos_y = trackArray[tail_index].y - train_hei;
            
            if(trackArray[head_index].track_direction == 1){
               var head_pos_x = trackArray[head_index].x + trackArray[head_index].m_l_track*head_pos/100;
            }
            else{
               var head_pos_x = trackArray[head_index].x + trackArray[head_index].m_l_track*(100 - head_pos)/100;
            }

            if(trackArray[head_index].track_direction == 1){
                var tail_pos_x = trackArray[tail_index].x + trackArray[tail_index].m_l_track*tail_pos/100;
            }
            else{
                var tail_pos_x = trackArray[tail_index].x + trackArray[tail_index].m_l_track*(100 - tail_pos)/100;
            }

            station.createTrainHead(head_pos_x,head_pos_y,train_index,train_tail_png,train_id,train_len/3*trackArray[head_index].track_scale);
            station.createTrainCenter((head_pos_x+tail_pos_x)/2,(head_pos_y+tail_pos_y)/2,train_index,train_center_png,train_id,train_len/3);
            station.createTrainTail(tail_pos_x,tail_pos_y,train_index,train_head_png,train_id,train_len/3*trackArray[tail_index].track_scale);
            station.swapTrainheadAndTail(head_index,tail_index,train_index,parseInt(train_id))
            //创建列车显示信息Label
            station.showTrainInformation(head_pos_x,head_pos_y - train_len,train_id,train_index)
        }
    }

    //更新列车的坐标
    Connections{
        target: uiutil;
        onUpdateTrainPosition:{
           
        }
    }
    
    //删除列车 此处列车数组并没有做清除操作
    Connections{
        target: uiutil;
        onDeleteTrainObject:{
            console.log("delete train id ",tindex);
            trainHeadArray[tindex].deleteTrainObj();
            trainTailArray[tindex].deleteTrainObj();
            trainCenterArray[tindex].deleteTrainObj();
        }
    }

    Connections{
        target: uiutil;
        onShowHideTrainInformation:{
            console.log("delete train id ",tindex,tag);
            if(tag == 0)
                trainInfoArray[tindex].shTag = false;
            else
                trainInfoArray[tindex].shTag = true;
        }
    }
    
    Component.onCompleted: ate_mianWindow.mapReady(uiutil);
}
