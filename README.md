# GOPHR_Simulation-Hardware
Contains the entire top portion of GOPHR, simulation & hardware, for the Texas A&M CAPSTONE project in one folder (catkin_ws)

Simulation:<br>
Uses Gazebo Simulator and CAD files with reduced polygons to simulate the base of GOPHR for figuring out Lidar and Mapping

Hardware:<br>
Final code version used on the Raspberry Pi 4 Ubuntu-20.04 LTS

Simulation was used on Ubuntu Desktop using tasksel and LightDM, and ROS Noetic.




user_interface - Simple user interface using PyQt5 combined with an RFID handle and ROS

gophr (Ground Operating Patient Helper Robot) - Simulation folder using gazebo and rviz for navigation with RPLidar A1M8, and soon to add obstacle detection. This will help in understanding what will happen and integrate with actual hardware. Have Ubuntu 20.04 Desktop installed, ROS Noetic full desktop, robot_pose_ekf, and rplidar_ros, then run the command 'roslaunch gophr gophr_robot.launch'

gophr_hardware - Used on the actual robot

opencv - Text detection using opencv and pytesseract (handled by teammate)<br>
Download and place the 'froze_east_text_detection.pb' file into gophr_hardware/scripts https://github.com/oyyd/frozen_east_text_detection.pb

robot_pose_ekf - ROS package for publishing odometry to base_footprint of the robot to fully connect map->odom->base_footprint->base_link

rplidar_ros - ROS package for RPLidar A1M8

Make sure to enable UART2 and SPI on the Raspberry Pi 4 with Ubuntu
