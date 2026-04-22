#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import run
import rospy
from std_msgs.msg import Int8
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
    do_id = msg.do_id

    if(msg.f is None):
        arg_f = "-f=0"
    else:
        arg_f = "-f={}".format(msg.f)

    if(msg.g is None):
        arg_g = "-g=2.5"  # factory default
    else:
        arg_g = "-g={}".format(msg.g)

    if(msg.t is None):
        arg_t = "-t=0.3"
    else:
        arg_t = "-t={}".format(msg.t)

    arg_sw = "-switch=true"  # always true

    if(msg.name is None):
        arg_name = "test_sample"
    else:
        arg_name = "-name={}".format(msg.name)
    # arg_name = "-name=polyethy_10G"

    # Note for arg_file:
    # - /mnt/c/.. cannot be used in the measurement software
    if(msg.file is None):
        arg_file = "test.csv"
    else:
        arg_file = "-file={}".format(msg.file)
    #arg_file = "-file=C:/Users/test/Desktop/asano/20230728.csv"

    #rospy.loginfo("[DIELECTROMETER] recieved parameters. do_id:%d, f:%d, g:%f, t:%f, switch:%d, name:%s, file:%s", do_id, arg_f, arg_g, arg_t, arg_sw, arg_name, arg_file)

    # measure blank
    if(do_id == 0):
        rospy.loginfo("[DIELECTROMETER][measureblank] do_id:%d, f:%d, switch:%d", msg.do_id, msg.f, msg.switch)
        arg_do = "-domeasureblank"
        run([exe, arg_f, arg_sw, arg_do])
    # measure target
    elif(do_id == 1):
        rospy.loginfo("[DIELECTROMETER][measuretarget] do_id:%d, f:%d, g:%f, t:%f, switch:%d", msg.do_id, msg.f, msg.g, msg.t, msg.switch)
        arg_do = "-domeasuretarget"
        run([exe, arg_f, arg_g, arg_t, arg_sw, arg_do])
    # calc and save
    elif(do_id == 2):
        rospy.loginfo("[DIELECTROMETER][calc] do_id:%d, f:%d, t:%f, switch:%d, name:%s, file:%s", msg.do_id, msg.f, msg.t, msg.switch, msg.name, msg.file)
        arg_do   = "-docalc"
        run([exe, arg_f, arg_t, arg_sw, arg_do, arg_name, arg_file])
    else:
        rospy.logwarn("not registerd func %d", do_id)
        run(['/mnt/c/Windows/System32/notepad.exe'])


def callback(msg):
    rospy.loginfo("[DIELECTROMETER] recieved do_id: %d", msg.do_id)
    rospy.loginfo("[DIELECTROMETER] recieved t    : %d", msg.t)
    # rospy.loginfo("[DIELECTROMETER] recieved command. do_id:%d, f:%d, g:%f, t:%f, switch:%d, name:%s, file:%s", msg.do_id, msg.f, msg.g, msg.t, msg.switch, msg.name, msg.file)  # for debug
    execute(msg)


def subscriber():
    rospy.init_node('subscriber', anonymous=True)
    #rospy.Subscriber("dielectrometer_cmd", Int8, callback)
    rospy.Subscriber("dielectrometer_cmd", Dielectrometer, callback)

    rospy.spin()


if __name__ == "__main__":
    subscriber()
