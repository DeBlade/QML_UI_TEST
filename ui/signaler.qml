import QtQuick 2.0
import QtQuick.Controls 1.2

Rectangle {
    id:signaler;
    width: 8;
    height: 12;
    property var signaler_name;
    Button{
        id:signaler_png;
        anchors.fill: parent;
        tooltip: signaler_name;
        Image {
            anchors.fill: parent
            source: "images/signaler-white.png";
        }
    }
}
