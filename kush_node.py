import rclpy
from rclpy.node import Node
from swarm_interfaces.msg import RobotState
import math

class KushNode(Node):
    def __init__(self):
        super().__init__('kush_bot')
        self.my_id = 2  # Corrected ID for Kush
        
        # Dummy Goal (The Areca Nut Task)
        self.goal_x, self.goal_y = 50.0, 50.0
        
        # Initial Position (Starts closer than Luv)
        self.x, self.y = 0.0, 0.0
        self.role = "SEARCHING"
        
        # We track LUV'S distance here to compare
        self.luv_dist_to_goal = 999.9  

        self.pub = self.create_publisher(RobotState, 'swarm_status', 10)
        self.sub = self.create_subscription(RobotState, 'swarm_status', self.callback, 10)
        self.timer = self.create_timer(1.0, self.brain_loop)

    def callback(self, msg):
        if msg.id == self.my_id:
            return
        
        # Kush calculates Luv's distance from the incoming message
        self.luv_dist_to_goal = math.sqrt((self.goal_x - msg.x)**2 + (self.goal_y - msg.y)**2)

    def brain_loop(self):
        my_dist = math.sqrt((self.goal_x - self.x)**2 + (self.goal_y - self.y)**2)

        # ROLE LOGIC: Whoever is closer is the Leader
        if my_dist < self.luv_dist_to_goal:
            self.role = "LEADER"
            self.x += 2.0  
            self.y += 2.0
        else:
            self.role = "FOLLOWER"
            self.x += 1.0  
            self.y += 1.0

        # Publish status
        msg = RobotState()
        msg.id = self.my_id
        msg.x = self.x
        msg.y = self.y
        msg.status = self.role
        self.pub.publish(msg)

        # Corrected log to say KUSH instead of LUV
        self.get_logger().info(f'KUSH: I am {self.role}. Dist to Goal: {my_dist:.2f}')

def main(args=None):
    rclpy.init(args=args)
    # Using the KushNode class here
    node = KushNode()
    rclpy.spin(node)
    rclpy.shutdown()
