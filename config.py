#!/usr/bin/env python
# coding=utf-8

#设置弹幕加载完成后是否自动打开
ENALLE_OPEN = 'on'

SCRIPT_INFO = {
	'ScriptType': 'v4.00',
	'Collisions': 'Normal',
	'PlayResX': '384',
	'PlayResY': '288',
	'Timer': '100.0000',
}

V4_STYLES = {
    'Format': 'Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,TertiaryColour,BackColour,Bold,Italic,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,AlphaLevel,Encoding',
    'Style': (
    	'{style},WenQuanYi Micro Hei,10,16777215,4227327,8404992,00000000,0,0,1,1,0,0,0,0,107,0,136',
    	'{style},WenQuanYi Micro Hei,10,{color_code},4227327,8404992,16777215,0,0,1,1,0,0,0,0,107,0,136',
    	'{style},WenQuanYi Micro Hei,10,{color_code},4227327,8404992,16777215,0,0,1,1,0,6,0,0,0,0,136', 
    	'{style},WenQuanYi Micro Hei,10,16777215,4227327,8404992,00000000,0,0,1,1,0,6,0,0,0,0,136',
    	)
}

EVENTS = {
	'rolling': 'Dialogue: Marked=0,{start_time},{end_time},{style},NTP,0000,0000,0000,Banner;25;0;50,{text}',
	'static': 'Dialogue: Marked=0,{start_time},{end_time},{style},NTP,0000,0000,0000,,{text}',
}

