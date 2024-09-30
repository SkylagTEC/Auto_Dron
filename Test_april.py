#!/usr/bin/env python
# -*- coding: utf-8 -*-
#                   ---- Pendientes codigo ----                     #
#--- 1- Poder hacer que se mantenga elevado el tiempo que quiera ---#
#--- 2- Probar la camara si ya no presenta retraso ----              #

import copy
import time
import argparse
import threading

import cv2 as cv
from pupil_apriltags import Detector
from dron_tello import DroneController

## Optimizar el proceso del video
class VideoStream():
    def __init__(self, drone):
        self.drone = drone
        self.frame = None
        self.stopped = False
        self.stream_thread = threading.Thread(target=self.update, args=())
        self.stream_thread.daemon = True  # Para cerrar con el programa principal
    
    def start(self):
        self.stopped = False
        self.stream_thread.start()
        return self
    
    def update(self):
        while not self.stopped:
            self.frame = self.drone.get_frame_read().frame
    
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True
        self.stream_thread.join()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)  # Dispositivo camara
    parser.add_argument("--width", help='cap width', type=int, default=2592) #Ancho de la camara
    parser.add_argument("--height", help='cap height', type=int, default=1936) #Altura de la camara

    parser.add_argument("--families", type=str, default='tag36h11')  # Familia de Apriltag (cada apriltags tienen su familia)
    parser.add_argument("--nthreads", type=int, default=1)  #Numero de hilos para el detector
    parser.add_argument("--quad_decimate", type=float, default=2.0) # Decima la resolución de la imagen antes de la detección para mejorar la velocidad
    parser.add_argument("--quad_sigma", type=float, default=0.0) # Aplica un suavizado a la imagen antes de la detección.
    parser.add_argument("--refine_edges", type=int, default=1) #Determina si se deben refinar los bordes de los AprilTags durante la detección.
    parser.add_argument("--decode_sharpening", type=float, default=0.25) #Ajusta el nivel de afilado de la imagen antes de intentar decodificar el tag.
    parser.add_argument("--debug", type=int, default=0) #Activa el modo de depuración (debug) no tocar plis

    args = parser.parse_args()

    return args


def main():
    #Inicializador el controlador del dron
    drone = DroneController()
    drone.connect_drone()

    
    #Transmicion del video  
    frame_reader = drone.start_video_stream()
    
    args = get_args()
    
    
    
    
    #cap_device = scren_tello()
    #cap_width = args.width
    #cap_height = args.height
    
    families = args.families
    nthreads = args.nthreads
    quad_decimate = args.quad_decimate
    quad_sigma = args.quad_sigma
    refine_edges = args.refine_edges
    decode_sharpening = args.decode_sharpening
    debug = args.debug

    #cap = cv.VideoCapture(cap_device)
    #cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    #cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Inicializacion del detector de apriltag
    at_detector = Detector(
        families=families,
        nthreads=nthreads,
        quad_decimate=quad_decimate,
        quad_sigma=quad_sigma,
        refine_edges=refine_edges,
        decode_sharpening=decode_sharpening,
        debug=debug,
    )

    elapsed_time = 0
    drone.take_off_fun()
    drone.rot_fun()

    while True:
        start_time = time.time()
        frame = frame_reader.frame
        if frame is None:
            print("No se puede conectar al frame de la camara ")
            break
        
        #Escala de grises
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
        #Detectar los AprilTags
        tags = at_detector.detect(
            gray,
            estimate_tag_pose=False,
            camera_params=None,
            tag_size=None,
        )

        debug_image = draw_tags(frame, tags, elapsed_time)
        elapsed_time = time.time() - start_time
        
        #Tecla de escape
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        
        cv.imshow('AprilTag Detect Demo', debug_image)
    
    
    drone.stop_video_stream()
    cv.destroyAllWindows()


def draw_tags(image,tags,elapsed_time,):
    for tag in tags:
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners

        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        # 中心
        cv.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)

        # 各辺
        cv.line(image, (corner_01[0], corner_01[1]),
                (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv.line(image, (corner_02[0], corner_02[1]),
                (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv.line(image, (corner_03[0], corner_03[1]),
                (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv.line(image, (corner_04[0], corner_04[1]),
                (corner_01[0], corner_01[1]), (0, 255, 0), 2)

        # タグファミリー、タグID
        # cv.putText(image,
        #            str(tag_family) + ':' + str(tag_id),
        #            (corner_01[0], corner_01[1] - 10), cv.FONT_HERSHEY_SIMPLEX,
        #            0.6, (0, 255, 0), 1, cv.LINE_AA)
        cv.putText(image, str(tag_id), (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)

    # 処理時間
    cv.putText(image,
               "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
               cv.LINE_AA)
    
    return image


if __name__ == '__main__':
    main()