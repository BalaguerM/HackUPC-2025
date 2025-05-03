import socket
import cv2
import pickle
import struct

HOST = 'localhost'  # Replace with sender IP
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = b''
    payload_size = struct.calcsize(">L")

    while True:
        while len(data) < payload_size:
            data += s.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += s.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow("Remote Screen", frame)
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
