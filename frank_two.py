import cv2
import time
from simple_pid import PID
from FlyLib3.control.tello import Tello
from FlyLib3.vision.apriltag import ApriltagDetector

drone = Tello()
yaw_pid = PID(0.2, 0.1, 0, setpoint=0)
height_pid = PID(0.2, 0.00024, 0, setpoint=0)
detector = ApriltagDetector(nthreads=4)

last_time = time.time()

def main():
    drone.connect()
    drone.streamon()
    print(drone.get_battery())
    time.sleep(0.25)
    #drone.takeoff()
    frame_read = drone.get_frame_read()

    while True:
        global last_time
        now_time = time.time()
        frame = frame_read.frame
        frame = cv2.resize(frame,(320,240))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        x_center_frame = frame.shape[1] // 2
        y_center_frame = frame.shape[0] // 2

        detections = detector.detect(gray, estimate_tag_pose=True)
        
        if len(detections) > 0:
            for detection in detections:
                tag_id = detection.tag_id
                errorX = x_center_frame - detection.center[0]
                errorY = y_center_frame - detection.center[1]
                print(detection.corners)
                drone.send_rc_control(0, 0, -int(height_pid(errorY, now_time - last_time)), int(yaw_pid(errorX, now_time - last_time)))
                if abs(errorX)<10 and abs(errorY)<10:
                    if tag_id == 1:
                        drone.move_forward(75)
                    elif tag_id == 2:
                        drone.move_right(75)
                    elif tag_id ==3 :
                        drone.move_left(80)
                    elif tag_id == 0:
                        drone.land()
                                    
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break

        last_time = now_time
        
    time.sleep(0.1)
    
if __name__ == "__main__":
    main()