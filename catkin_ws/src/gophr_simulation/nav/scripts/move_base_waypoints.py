#!/usr/bin/env python3
# license removed for brevity
__author__ = 'fiorellasibona'
import rospy
import math

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Int16


class MoveBaseSeq():

    def __init__(self):

        rospy.init_node('move_base_waypoints')

        # need to only subscribe for an array of data from main.py ui then do all of
        #  the listing
        # JUST SEND A 1 for room one and do an integer string concatnate to use waypointNodes1.csv
        #  example: ("...\waypointNodes%d", x=1)

        rospy.Subscriber("/room_number", Int16, callback=self.click_callback)
        

    
    def click_callback(self, msg: Int16): # change pose to just an integer
        #points_seq = [message.position.x, message.position.y, message.position.z] # recieve the coordinates from coord in a message of type Pose
        wayponint = "/home/tjcc/catkin_ws/src/user_interface/waypoints/waypointNodes%d.csv" % msg.data # number concatnate
        #f = open("/home/tjcc/catkin_ws/src/gophr/nav_scripts/waypointNodes.csv","r")
        f = open(wayponint,"r")
        rawNodes = f.readlines()
        f.close()
        nodes = []
        for i in rawNodes:
            #nodes.append([float(i.split(",")[0]), float(i.split(",")[1])])
            nodes.append(float(i.split(",")[0]))
            nodes.append(float(i.split(",")[1]))
            nodes.append(0.0)
            rospy.loginfo(nodes)
        
        if len(nodes) < 2:
            print("Not enough waypoinys")
            exit()

        points_seq = nodes
        print(points_seq)
        rospy.loginfo(points_seq)

        # Returns a list of lists [[point1], [point2],...[pointn]]
        points = [points_seq[i:i+3] for i in range(0, len(points_seq), 3)] # points = [points_seq[i:i+n] for i in range(0, len(points_seq), n)]
        rospy.loginfo(points)

        #yaweulerangles = [90,0,180]
        #p = 0
        #yaweulerangles_seq = []
        #for i in rawNodes:
        #    if p == 3:
        #        p = 0
        #    yaweulerangles_seq.append(yaweulerangles[p])
        #    p+=1

        yawrad_seq = []
        for i in rawNodes:
            #yaweulerangles_seq.append(float(i.split(",")[2]))
            #yawrad_seq.append(float(i.split(",")[2]))
            yawrad_seq.append([float(i.split(",")[2]), float(i.split(",")[3])])


        #List of goal quaternions:
        quat_seq = list()
        #List of goal poses:
        self.pose_seq = list()
        self.goal_cnt = 0
        for yawrad in yawrad_seq: # for yawanlge in yaweulerangles_seq
            #Unpacking the quaternion list and passing it as arguments to Quaternion message constructor
            #quat_seq.append(Quaternion(*(quaternion_from_euler(0, 0, yawangle*math.pi/180, axes='sxyz')))) # convert angel to radian
            #quat_seq.append(Quaternion(*(quaternion_from_euler(0, 0, yawrad, axes='sxyz')))) # w needs to be accounted for
            quat_seq.append(Quaternion(0,0,yawrad[0],yawrad[1])) # xyzw
        #n = 3
        rospy.loginfo(quat_seq)
        m = len(quat_seq)
        rospy.loginfo(m)
        # Returns a list of lists [[point1], [point2],...[pointn]]
        #points = [points_seq[i:i+3] for i in range(0, len(points_seq), 3)] # points = [points_seq[i:i+n] for i in range(0, len(points_seq), n)]
        #rospy.loginfo(points)
        n = len(points)
        for point in points:
            #Exploit n variable to cycle in quat_seq
            self.pose_seq.append(Pose(Point(*point),quat_seq[n-m])) #quat_seq[n-3]
            n += 1
        rospy.loginfo(self.pose_seq)
        
        #Create action client
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.client.wait_for_server(rospy.Duration(5.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")
        
        self.movebase_client()

    def active_cb(self):
        rospy.loginfo("Goal pose "+str(self.goal_cnt+1)+" is now being processed by the Action Server...")

    def feedback_cb(self, feedback):
        #To print current pose at each feedback:
        #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
        rospy.loginfo("Feedback for goal pose "+str(self.goal_cnt+1)+" received")

    def done_cb(self, status, result):
        self.goal_cnt += 1
    # Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
        if status == 2:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request after it started executing, completed execution!")

        if status == 3:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" reached") 
            if self.goal_cnt< len(self.pose_seq):
                next_goal = MoveBaseGoal()
                next_goal.target_pose.header.frame_id = "map"
                next_goal.target_pose.header.stamp = rospy.Time.now()
                next_goal.target_pose.pose = self.pose_seq[self.goal_cnt]

                rospy.loginfo(str(self.pose_seq[self.goal_cnt])) # not being properly sliced

                rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
                rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
                self.client.send_goal(next_goal, self.done_cb, self.active_cb, self.feedback_cb) 
            else:
                rospy.loginfo("Final goal pose reached!")
                rospy.signal_shutdown("Final goal pose reached!")
                return

        if status == 4:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" was aborted by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" aborted, shutting down!")
            return

        if status == 5:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" has been rejected by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" rejected, shutting down!")
            return

        if status == 8:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request before it started executing, successfully cancelled!")

    def movebase_client(self):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() 
        goal.target_pose.pose = self.pose_seq[self.goal_cnt]
        rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
        rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
        rospy.spin()
    
    

if __name__ == '__main__':
    try:
        #rospy.init_node('move_base_sequence_points')
        #subn = rospy.Subscriber("/coordinates", Pose, callback=MoveBaseSeq())
        #rospy.spin()
        #rospy.loginfo(subn)
        #play = (float) subn
        MoveBaseSeq()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")

