import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(Image, 'image_topic', self.image_callback, 10)
        self.subscription

    def image_callback(self, msg):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

        edges = cv.Canny(cv_image, 100, 200)
        
        # edges_resized = cv.resize(edges, (cv_image.shape[1], cv_image.shape[0]))

        # if edges_resized.shape != cv_image.shape[:2]:
        #     print("Error: Resized image size does not match the original BGR image size.")
        #     return

        edges_bgr = np.zeros_like(cv_image)
        edges_bgr[:,:,0] = edges
        edges_bgr[:,:,1] = edges
        edges_bgr[:,:,2] = edges
        print(cv_image.shape, edges_bgr.shape)


        if edges_bgr.shape != cv_image.shape:
            print("Error: Resized image size does not match the original BGR image size.")
            return
    
        result = cv.hconcat([cv_image, edges_bgr])

        cv.imshow("Image Processing", result)
        cv.waitKey(1)

def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
