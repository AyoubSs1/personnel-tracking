import cv2


def open_camera(camera):

    source_type = camera["source_type"]
    source = camera["source"]

    if source_type == "webcam":

        cap = cv2.VideoCapture(int(source))

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

    elif source_type in ["ip", "rtsp"]:

        cap = cv2.VideoCapture(source)

    else:

        raise ValueError(
            f"Type de caméra inconnu : {source_type}"
        )

    if not cap.isOpened():

        raise RuntimeError(
            f"Impossible d'ouvrir la caméra : "
            f"{camera['camera_name']}"
        )

    return cap