from djitellopy import Tello

tello = Tello()
tello.connect()
print(f"Nivel de bateria {tello.get_battery}")
tello.takeoff()
tello.land()
