from djitellopy import Tello
import cv2 as cv


def finish_command(confirmo):
    if confirmo:
        return True
        
class DroneController:
    def __init__(self):
        self.drone = Tello()
        self.frame_reader = None
        
    def connect_drone(self):
        self.drone.connect()
        print("Conectado ----- exitosamente")
        bateria = self.drone.get_battery()
        print(f"Nivel bateria {bateria}%")
        return bateria
    
    def esta_volando(self):
        return self.drone.query_speed() > 0
        #return self.drone.is_flying
    
    def start_video_stream(self):
        self.drone.streamon()
        self.frame_reader = self.drone.get_frame_read()
        #frame_reader.frame = cv.resize(frame_reader.frame, (640, 480))  ## realize cambio aqui para voltear la camara
        return self.frame_reader
        
    
    def stop_video_stream(self):
        self.drone.streamoff()
        
    def take_off_fun(self):
        self.drone.takeoff()
        self.drone.move_up(40)
        
    def move_foward_fun(self):
        self.drone.move_forward(100)
        finish_command(True)
    
    def move_right_fun(self):
        self.drone.move_right(50)
        
    def move_left_fun(self):
        self.drone.move_left(150)
    
    def move_back_fun(self):
        self.drone.move_back(100)
    
    def rot_fun(self):
        self.drone.rotate_clockwise(125)

        
    

if __name__ == "__main__":
    drone = DroneController()
    drone.connect_drone()