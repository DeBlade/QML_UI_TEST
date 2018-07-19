import QtQuick 2.3
import QtQuick.Window 2.0
import QtQuick.Controls 1.2

Rectangle{
    id:platform;
    width: centern.width+right_lamp.width*2;
    height: 36;
    color: "black";
    property var plat_name;
    property var top_bottom;
    property var id_plat;
    property var left_tag:true;
    property var right_tag:true;
    property var utils;
    property var p_id;
    //中间站台
    Rectangle{
        id:centern;
        width:72;
        height: 28;
        x:16;
        y:4;
        color: "black";
        border.width: 1;
        border.color: "white";
        Text {
            id: centern_name
            anchors.fill: parent;
            verticalAlignment: Text.AlignVCenter;
            horizontalAlignment: Text.AlignHCenter;
            text: qsTr(plat_name)
            color: "white";
            font.pixelSize: 12
            }
    }
    //左边信号灯
    Button{
        id:left_lamp;
        width:16;
        height: 16;
        x:0;
        y:(centern.height - left_lamp.height)/2+4;

        Image {
            anchors.fill: parent
            source: left_tag ? "images/green.png":"images/red.png"
        }
        onClicked: {
            console.log("left button click");
        }
    }
    //右边信号灯
    Button{
        id:right_lamp;
        width:16;
        height: 16;
        x:centern.x+centern.width;
        y:(centern.height - left_lamp.height)/2+4;
        Image {
            anchors.fill: parent
            source: right_tag ? "images/purple.png":"images/red.png"
        }
        onClicked: {
            //console.log("right button click",id_plat)
        }
    }
    Rectangle{
        id:top_door;
        width:centern.width;
        height: 4;
        x:left_lamp.width;
        visible:top_bottom == '2'? true:false;
        y:0;

        //上左边门
        Rectangle{
            id:left_top_door;
            width:centern.width/3;
            height: parent.height;
            x:0;
            y:0;
            color: "red";
        }
        //上中间门
        Rectangle{
            id:center_top_door;
            width:centern.width/3;
            height: parent.height;
            anchors.left: left_top_door.right;
            color: "red";
        }
        //上右边门
        Rectangle{
            id:right_top_door;
            width:centern.width/3;
            height: parent.height;
            anchors.left: center_top_door.right;
            color: "red";
        }
    }
    Rectangle{
        id:bottom_door;
        width:centern.width;
        height: 4;
        x:left_lamp.width;
        anchors.top: centern.bottom
        color: "red";
        visible:top_bottom == '1'? true:false;

        //下左边门
        Rectangle{
            id:left_bottom_door;
            width:centern.width/3;
            height: left_top_door.height;
            x:0;
            y:0;
            color: "red";
        }
        //下中间门
        Rectangle{
            id:center_bottom_door;
            width:centern.width/3;
            height: left_top_door.height;
            anchors.left: left_bottom_door.right;
            color: "red";
        }
        //下右边门
        Rectangle{
            id:right_bottom_door;
            width:centern.width/3;
            height: left_top_door.height;
            anchors.left: center_bottom_door.right;
            color: "red";
        }
    }
    function openTheDoor(){
        left_top_door.color = "green";
        center_top_door.color = "black";
        right_top_door.color = "green";

        left_bottom_door.color = "green";
        center_bottom_door.color = "black";
        right_bottom_door.color = "green";
    }
    function openTheDoor_yellow(){
        left_top_door.color = "yellow";
        center_top_door.color = "black";
        right_top_door.color = "yellow";

        left_bottom_door.color = "yellow";
        center_bottom_door.color = "black";
        right_bottom_door.color = "yellow";
    }
    function closeTheDoor(){
        left_top_door.color = "red";
        center_top_door.color = "red";
        right_top_door.color = "red";

        left_bottom_door.color = "red";
        center_bottom_door.color = "red";
        right_bottom_door.color = "red";
    }
    MouseArea {
       id: plat_area
       enabled: true;
       anchors.fill: parent;
       drag.target: parent;
       drag.filterChildren: true;
       acceptedButtons: Qt.RightButton;
       onClicked: {
           console.log("plat id",id_plat)
           platformMenu.popup()
       }
    }

   Menu { // 右键菜单
        id: platformMenu
        MenuItem {
            text:"人工设置开门1"
            onTriggered: {
                console.log("人工设置开门1")
            }
        }
        MenuItem {
            text:"人工设置关门"
            onTriggered: {
                console.log("人工设置关门")
            }
        }
    }
}
