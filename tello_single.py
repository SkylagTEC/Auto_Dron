from djitellopy import Tello

tello = Tello()
tello.connect()
print("Conectado al dron")
tello.takeoff()
tello.land()