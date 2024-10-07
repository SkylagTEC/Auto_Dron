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
    frame_read = drone.get_frame_read()
    
    

    while True:
        global last_time
        now_time = time.time()
        frame = frame_read.frame
        
        #while frame_read.stopped:
         #   frame_read = None
          #  frame= frame_read.frame
    
        frame = cv2.resize(frame,(320,240))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_centerX = frame.shape[1] // 2
        frame_centerY = frame.shape[0] // 2
        
        cv2.line(frame, (frame_centerX - 20, frame_centerY), (frame_centerX + 20, frame_centerY), (0, 0, 255), 2)  # Línea horizontal en rojo
        cv2.line(frame, (frame_centerX, frame_centerY - 20), (frame_centerX, frame_centerY + 20), (0, 0, 255), 2)  # Línea vertical en rojo

        detections = detector.detect(gray, estimate_tag_pose=True)
        
        if len(detections) > 0:
            for detection in detections:
                tag_id = detection.tag_id
                
                (ptA, ptB, ptC, ptD) = detection.corners
                
                centerX =int((ptA[0] + ptB[0] + ptC[0] + ptD[0]) / 4)
                centerY = int((ptA[1] + ptB[1] + ptC[1] + ptD[1]) / 4)
                
                cv2.line(frame,(centerX, centerY),(centerX + 20, centerY),(0, 255, 0), 2)
                cv2.line(frame,(centerX, centerY -20),(centerX, centerY ), (255, 0, 0), 2)
                
                errorX = frame_centerX - centerX
                errorY = frame_centerY - centerY
                
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
                    
        if (now_time -last_time) > 0.0000001:
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break

        last_time = now_time
        
    time.sleep(0.03)
    

if __name__ == "__main__":
    main()