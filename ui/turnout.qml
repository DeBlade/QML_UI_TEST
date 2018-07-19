import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 1.2

Rectangle{
    id:turnout;
    width: m_l_track;
    height: track_height
    color: "black";

    property var m_l_track;
    property var track_height;
    property var id_track;
    property var type:-1;
    property var sdir: 1;
    property var track_scale:0;
    property var updown;//道岔在track 上下 1 上 -1 下
    property var t_rotation : track_height/m_l_track;
    property var tname :"";
    property var turnoutTrack_color : "gray";
    property var position;
    Rectangle{
        id:turnoutTrack;
        width:Math.sqrt(m_l_track * m_l_track + track_height * track_height);
        y:(track_height-8)/2;
        x:-((Math.sqrt(m_l_track * m_l_track + track_height * track_height)) - m_l_track)/2;
        height: 8;
        visible: true;
        color: turnoutTrack_color;
        rotation:Math.atan(track_height/m_l_track)/Math.PI*180 * (-sdir)
        radius: 8

    }
    function changeTrackRed(){}
    function changeTrackGray(){}
    function changeTrackToLightBlack(){}
    function changeTrackToGray(){}
    function changeTrackToBlack(){}
}