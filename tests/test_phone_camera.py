import cv2


PHONE_CAMERA_URL = "http://192.168.11.103:8080/video"

cap = cv2.VideoCapture(PHONE_CAMERA_URL)

if not cap.isOpened():
    print(" Impossible de se connecter à la caméra du téléphone")
    exit()

print(" Connexion à la caméra réussie")

while True:

    ret, frame = cap.read()

    if not ret:
        print(" Impossible de lire une frame")
        break

    cv2.imshow("Phone Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()