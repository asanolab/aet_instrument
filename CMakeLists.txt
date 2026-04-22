cmake_minimum_required(VERSION 2.8.3)
project(aet_instrument)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

#catkin_python_setup()

add_message_files(
  FILES
  Dielectrometer.msg
  )

generate_messages(
  DEPENDENCIES
  std_msgs
  )

catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime
  )

install(DIRECTORY www
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
