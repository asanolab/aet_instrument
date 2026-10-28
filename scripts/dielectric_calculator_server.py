#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import run
import time
import roslibpy
import rospy
from aet_instrument.msg import Dielectrometer

# command memo
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=0 -switch=true -domeasureblank
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=1 -switch=true -domeasureblank
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=2 -switch=true -domeasureblank

#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=0 -g=2.5 -t=0.306 -switch=true -domeasuretarget
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=0 -t=0.306 -switch=true -docalc -name=polyethy_10G -file="C:\Users\test\Desktop\asano\20230606.csv"

#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=1 -g=2.5 -t=0.306 -switch=true -domeasuretarget
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=1 -t=0.306 -switch=true -docalc -name=polyethy_28G -file="C:\Users\test\Desktop\asano\20230606.csv"

#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=2 -g=2.5 -t=0.306 -switch=true -domeasuretarget
#"/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe" -f=2 -t=0.306 -switch=true -docalc -name=polyethy_40G -file="C:\Users\test\Desktop\asano\20230606.csv"


def execute(msg):
    exe = "/mnt/c/Program Files (x86)/DielectricCalculator/DielectricCalculator.exe"
    msg_do_id = msg['do_id']
    msg_f     = msg['f']
    msg_g     = msg['g']
    msg_t     = msg['t']
    msg_sw    = msg['switch']
    msg_name  = msg['name']
    msg_file  = msg['file']

    if(msg_do_id is None):
        arg_f = "-f=0"
    else:
        arg_f = "-f={}".format(msg_f)

    if(msg_g is None):
        arg_g = "-g=2.5"  # factory default
    else:
        arg_g = "-g={}".format(msg_g)

    if(msg_t is None):
        arg_t = "-t=0.3"
    else:
        arg_t = "-t={}".format(msg_t)

    arg_sw = "-switch=true"  # always true

    if(msg_name is None):
        arg_name = "test_sample"
    else:
        arg_name = "-name={}".format(msg_name)
    # arg_name = "-name=polyethy_10G"

    # Note for arg_file:
    # - /mnt/c/.. cannot be used in the measurement software
    if(msg_file is None):
        arg_file = "test.csv"
    else:
        arg_file = "-file={}".format(msg_file)

    #rospy.loginfo("[DIELECTROMETER] recieved parameters. do_id:%d, f:%d, g:%f, t:%f, switch:%d, name:%s, file:%s", do_id, arg_f, arg_g, arg_t, arg_sw, arg_name, arg_file)

    # measure blank
    if(msg_do_id == 0):
        rospy.loginfo("[DIELECTROMETER][measureblank] do_id:%d, f:%d, switch:%d", msg_do_id, msg_f, msg_sw)
        arg_do = "-domeasureblank"
        run([exe, arg_f, arg_sw, arg_do])
    # measure target
    elif(msg_do_id == 1):
        rospy.loginfo("[DIELECTROMETER][measuretarget] do_id:%d, f:%d, g:%f, t:%f, switch:%d", msg_do_id, msg_f, msg_g, msg_t, msg_sw)
        arg_do = "-domeasuretarget"
        run([exe, arg_f, arg_g, arg_t, arg_sw, arg_do])
    # calc and save
    elif(do_id == 2):
        rospy.loginfo("[DIELECTROMETER][calc] do_id:%d, f:%d, t:%f, switch:%d, name:%s, file:%s", msg_do_id, msg_f, msg_t, msg_sw, msg_name, msg_file)
        arg_do   = "-docalc"
        run([exe, arg_f, arg_t, arg_sw, arg_do, arg_name, arg_file])
    else:
        rospy.logwarn("not registerd func %d", do_id)
        run(['/mnt/c/Windows/System32/notepad.exe'])


def callback(msg):
    msg_do_id = msg['do_id']
    msg_t     = msg['t']
    rospy.loginfo("[DIELECTROMETER] recieved do_id: %d", msg_do_id)
    rospy.loginfo("[DIELECTROMETER] recieved t    : %d", msg_t)
    # rospy.loginfo("[DIELECTROMETER] recieved command. do_id:%d, f:%d, g:%f, t:%f, switch:%d, name:%s, file:%s", msg_do_id, msg_f, msg_g, msg_t, msg_sw, msg_name, msg_file)  # for debug
    execute(msg)


# ros
client_ip="192.168.0.44"
client_port=9090
ros = roslibpy.Ros(host=client_ip, port=client_port)
ros.run()

topic = roslibpy.Topic(
    ros,
    '/dielectrometer_cmd',
    'aet_instrument/Dielectrometer',
    throttle_rate=100,  # 100 ms間隔（最大約10 Hz）
)

topic.subscribe(callback)

try:
    while ros.is_connected:
        time.sleep(0.1)  # continue to connect
except KeyboardInterrupt:
    print('[roslibpy] Interrupted, shutting down service...')
    pass
finally:
    topic.unsubscribe()
    ros.terminate()
    print('[roslibpy] Disconnected from ROS.')
