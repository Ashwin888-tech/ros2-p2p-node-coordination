import rclpy
from rclpy.node import Node
from swarm_interfaces.msg import RobotState
import math

class LuvNode(Node):
    def __init__(self):
        super().__init__('luv_bot')
        self.my_id = 1  # Luv's ID
        
        # Dummy Goal (The Areca Nut Task)
        self.goal_x, self.goal_y = 50.0, 50.0
        
        # Initial Position
        self.x, self.y = 10.0, 10.0
        self.role = "SEARCHING"
        self.kush_dist_to_goal = 999.9  # Assume Kush is far away initially

        self.pub = self.create_publisher(RobotState, 'swarm_status', 10)
        self.sub = self.create_subscription(RobotState, 'swarm_status', self.callback, 10)
        self.timer = self.create_timer(1.0, self.brain_loop)

    def callback(self, msg):
        if msg.id == self.my_id:
            return
        
        # Calculate how close Kush is to the goal
        self.kush_dist_to_goal = math.sqrt((self.goal_x - msg.x)**2 + (self.goal_y - msg.y)**2)

    def brain_loop(self):
        my_dist = math.sqrt((self.goal_x - self.x)**2 + (self.goal_y - self.y)**2)

        # ROLE LOGIC: Whoever is closer is the Leader
        if my_dist < self.kush_dist_to_goal:
            self.role = "LEADER"
            self.x += 2.0  # Move faster toward goal
            self.y += 2.0
        else:
            self.role = "FOLLOWER"
            self.x += 1.0  # Move slower
            self.y += 1.0

        # Publish status
        msg = RobotState()
        msg.id = self.my_id
        msg.x = self.x
        msg.y = self.y
        msg.status = self.role
        self.pub.publish(msg)

        self.get_logger().info(f'LUV: I am {self.role}. Dist: {my_dist:.2f}')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LuvNode())
    rclpy.shutdown()
