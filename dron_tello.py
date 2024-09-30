from djitellopy import Tello
import cv2 as cv


class DroneController:
    def __init__(self):
        self.drone = Tello()
        
    def connect_drone(self):
        self.drone.connect()
        bateria = self.drone.get_battery()
        print(f"Nivel bateria {bateria}%")
        return bateria
    
    def start_video_stream(self):
        self.drone.streamon()
        frame_reader = self.drone.get_frame_read()
        frame_reader.frame = cv.resize(frame_reader.frame, (640, 480))  ## realize cambio aqui para voltear la camara
        return self.drone.get_frame_read()
    
    def stop_video_stream(self):
        self.drone.streamoff()
    
    def take_off_fun(self):
        self.drone.takeoff()
        self.drone.move_up(30)
        
    def move_foward_fun(self):
        self.drone.move_forward(100)
    
    def move_back_fun(self):
        self.drone.move_back(100)
    
    def rot_fun(self):
        self.drone.rotate_clockwise(125)
    
        
    

if __name__ == "__main__":
    drone = DroneController()
    drone.connect_drone()