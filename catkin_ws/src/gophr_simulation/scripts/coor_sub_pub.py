#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped, Pose, PoseStamped

#coordinate_array = [0,0,0]

def click_callback(msg: PoseStamped): ## message is a point used to be PointStamped
    # append coordinates
    coord = Pose() # going to publish a pose
    coord.position.x = msg.pose.position.x #msg.point.x
    coord.position.y = msg.pose.position.y
    coord.position.z = 0
    coord.orientation.z = msg.pose.orientation.z
    coord.orientation.w = msg.pose.orientation.w
    coordinate_array = [coord.position.x, coord.position.y, coord.position.z, coord.orientation.z, msg.pose.orientation.w]
    pub.publish(coord) # publish coord to the topic /coordinate, coord holds the x,y coordinates to the 
    rospy.loginfo(coordinate_array)
    f = open("/home/tjcc/catkin_ws/src/gophr/nav_scripts/waypointNodes.csv","a+")
    #f.write(str(msg.point.x)+","+str(msg.point.y)+"\n") # may need to add yaw
    f.write(str(msg.pose.position.x)+","+str(msg.pose.position.y)+","+str(msg.pose.orientation.z)+","+str(msg.pose.orientation.w)+"\n")
    f.close()



if __name__ == '__main__':
    rospy.init_node("coordinates_grab") # node name
    f = open("/home/tjcc/catkin_ws/src/gophr/nav_scripts/waypointNodes.csv","w+")
    f.close()
    pub = rospy.Publisher("/coordinates", Pose, queue_size=10)
    #sub = rospy.Subscriber("/clicked_point", PointStamped, callback=click_callback)
    sub = rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback=click_callback)

    rospy.loginfo("Node has been started.")

    rospy.spin() # blocks until ROS node is shutdown
    
