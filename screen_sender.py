import socket
import mss
import pickle
import struct
import cv2
import numpy as np

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[*] Waiting for connection on {HOST}:{PORT}")
    conn, addr = s.accept()
    print(f"[+] Connected by {addr}")

    with conn:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Full screen
            while True:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                data = pickle.dumps(buffer)
                conn.sendall(struct.pack(">L", len(data)) + data)
