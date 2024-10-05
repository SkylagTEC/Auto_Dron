import cv2
import time
from FlyLib3.control.tello import Tello
from FlyLib3.vision.apriltag import ApriltagDetector

drone = Tello()
detector = ApriltagDetector(nthreads=4)

last_time = time.time()

def main():
    drone.connect()
    drone.streamon()
    print(drone.get_battery())
    time.sleep(0.25)
    drone.takeoff()

    while True:
        global last_time
        now_time = time.time()
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame,(370,290))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections = detector.detect(gray, estimate_tag_pose=True)
        
        if len(detections) > 0:
            for detection in detections:
                tag_id = detection.tag_id

                
                if tag_id == 1:
                    drone.move_up(75)
                    drone.move_forward(200)
                    drone.rotate_clockwise(180)
                    drone.move_down(80)
                    drone.move_forward(150)
                    drone.rotate_clockwise(180)
                    drone.move_left(50)
                elif tag_id == 2:
                    drone.move_right(120)
                elif tag_id ==3 :
                    drone.move_left(80)
                    
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break

        last_time = now_time
        
    time.sleep(0.1)

if __name__ == "__main__":
    main()
