import QtQuick 2.0
import QtQuick.Controls 1.4
Rectangle{
    id: trackname
    width:36;
    height: 12;
    color: "black";
    visible: shTag;
    property var tname :"";
    property var shTag : true;
    Label {
        id: track_name
        anchors.fill: parent;
        text: tname;
        color: "white";
        visible: shTag;
        font.pixelSize: 12
    }
}