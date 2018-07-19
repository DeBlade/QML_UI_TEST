import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 1.2

Rectangle{
    id:trackLine;
    width: m_l_track;
    height: track_height;
    color: "black";

    property var m_l_track;
    property var id_track;
    property var test:1;
    property var isSwitch:0;
    property var track_direction : "0";
    property var track_scale : 0;
    property var utils; 
    property var track_name;
    property var track_height;
    property var switching : 1;
    property var switch_use : 0;
    property var t_rotation : 0; 
    property var sdir : 0;
    property var py_id :0
    property var ramp;

    Rectangle{
        id:trackhead;
        width:trackLine.width/2;
        height: trackLine.height;
        color: isSwitch == 0 ? "gray":"#FF00FF";
    }

    Rectangle{
        id:trackTail;
        width:trackLine.width/2;
        height: trackLine.height;
        anchors.left: trackhead.right;
        color: isSwitch == 0 ? "gray" : "#FF00FF";
    }
    
    Text {
        id: centern_name
        anchors.fill: parent;
        verticalAlignment: Text.AlignVCenter;
        horizontalAlignment: Text.AlignHCenter;
        text: ramp;
        color: "white";
        font.pixelSize: 12
    }

    MouseArea {
        id: track_menu
        enabled: true//rootItem.visible
        anchors.fill: parent;
        drag.target: parent;
        drag.filterChildren: true;
        acceptedButtons: Qt.RightButton;
        onClicked: {
            console.log("track id",id_track)
            trackMenu.popup()
        }
    }
    Menu { // 右键菜单
        id: trackMenu
        MenuItem {
            text:"占用"
            onTriggered: {
                console.log("占用")
            }
        }
        MenuItem {
            text:"非占用"
            onTriggered: {
                console.log("非占用")
            }
        }
    }
}
