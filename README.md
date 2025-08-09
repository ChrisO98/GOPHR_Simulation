# GOPHR_Simulation
Contains the GOPHR simulation for the Texas A&M senior capstone project in one folder (catkin_ws)

Uses Gazebo Simulator and CAD files with reduced polygons to simulate the base of GOPHR for figuring out Lidar and Mapping

Simulation was used on Ubuntu Desktop using tasksel and LightDM, and ROS Noetic.




user_interface - Simple user interface using PyQt5 combined with an RFID handle and ROS

gophr (Ground Operating Patient Helper Robot) - Simulation folder using gazebo and rviz for navigation with RPLidar A1M8, and soon to add obstacle detection. This will help in understanding what will happen and integrate with actual hardware. Have Ubuntu 20.04 Desktop installed, ROS Noetic full desktop, robot_pose_ekf, and rplidar_ros, then run the command 'roslaunch gophr gophr_robot.launch'

gophr_hardware - Used on the actual robot

opencv - Text detection using opencv and pytesseract (handled by teammate)

robot_pose_ekf - ROS package for publishing odometry to base_footprint of the robot to fully connect map->odom->base_footprint->base_link

rplidar_ros - ROS package for RPLidar A1M8
