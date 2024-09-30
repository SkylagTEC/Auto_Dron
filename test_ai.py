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

    parser.add_argument("--device", type=int, default=0)  # Dispositivo cámara
    parser.add_argument("--width", help='cap width', type=int, default=2592)  # Ancho de la cámara
    parser.add_argument("--height", help='cap height', type=int, default=1936)  # Altura de la cámara
    parser.add_argument("--families", type=str, default='tag36h11')  # Familia de AprilTag
    parser.add_argument("--nthreads", type=int, default=1)  # Número de hilos para el detector
    parser.add_argument("--quad_decimate", type=float, default=2.0)  # Decimación de la imagen
    parser.add_argument("--quad_sigma", type=float, default=0.0)  # Suavizado antes de la detección
    parser.add_argument("--refine_edges", type=int, default=1)  # Refinar bordes
    parser.add_argument("--decode_sharpening", type=float, default=0.25)  # Afilado antes de decodificar
    parser.add_argument("--debug", type=int, default=0)  # Modo depuración

    args = parser.parse_args()

    return args


def main():
    # Inicializar el controlador del dron
    drone = DroneController()
    drone.connect_drone()

    # Iniciar transmisión de video
    frame_reader = drone.start_video_stream()

    args = get_args()

    # Configuración del detector de AprilTag
    families = args.families
    nthreads = args.nthreads
    quad_decimate = args.quad_decimate
    quad_sigma = args.quad_sigma
    refine_edges = args.refine_edges
    decode_sharpening = args.decode_sharpening
    debug = args.debug

    # Inicializar el detector de AprilTag
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
    drone.take_off_fun()  # Despegar el dron

    detect_id = []
    ids_detects = []

    while True:
        start_time = time.time()
        frame = frame_reader.frame
        if frame is None:
            print("No se puede conectar al frame de la cámara")
            break

        # Convertir a escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detectar los AprilTags
        tags = at_detector.detect(
            gray,
            estimate_tag_pose=False,
            camera_params=None,
            tag_size=None,
        )

        debug_image, nums_tag = draw_tags(frame, tags, elapsed_time)
        detect_id.append(nums_tag)

        if nums_tag == 1:
            drone.rot_fun()  # Rotar el dron
            while drone.esta_volando():
                if nums_tag not in ids_detects:
                    ids_detects.append(nums_tag)
                pass

        elapsed_time = time.time() - start_time

        # Tecla de escape
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        cv.imshow('AprilTag Detect Demo', debug_image)

    print(detect_id)

    drone.stop_video_stream()
    cv.destroyAllWindows()


def draw_tags(image, tags, elapsed_time):
    tag_ids = 0
    for tag in tags:
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners
        tag_ids = tag_id

        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        # Dibujo del centro
        cv.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)

        # Dibujo de las esquinas
        cv.line(image, (corner_01[0], corner_01[1]),
                (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv.line(image, (corner_02[0], corner_02[1]),
                (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv.line(image, (corner_03[0], corner_03[1]),
                (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv.line(image, (corner_04[0], corner_04[1]),
                (corner_01[0], corner_01[1]), (0, 255, 0), 2)

        # Dibujo de la familia y el ID del tag
        cv.putText(image, str(tag_id), (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)

    # Tiempo transcurrido
    cv.putText(image,
               "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
               cv.LINE_AA)

    return image, tag_ids


def move_dron(x, drone):
    if x == 1:
        drone.move_foward_fun()
        while drone.esta_volando():
            pass


if __name__ == '__main__':
    main()
