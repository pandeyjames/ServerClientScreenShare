import socket
from PIL import Image
import io
import mss

# Function to capture the screen
def capture_screen():
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[1]  # In case of multiple monitors, adjust the index
        screenshot = sct.grab(monitor)
        return screenshot

# Function to send the screen image over socket
def send_screen(conn):
    try:
        with io.BytesIO() as output:
            img = capture_screen()
            # Convert the ScreenShot object to a PIL Image
            img_pil = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            img_pil.save(output, format='PNG')
            img_data = output.getvalue()
            # Send image size first
            conn.sendall(len(img_data).to_bytes(4, byteorder='big'))
            # Then send the image data
            conn.sendall(img_data)
        return True
    except ConnectionAbortedError:
        print("Client disconnected.")
        return False


# Server code
def server():
    HOST = '127.0.0.1'  # Server IP address
    PORT = 12345        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening on", (HOST, PORT))
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        if not send_screen(conn):
                            break
            except KeyboardInterrupt:
                print("Server terminated by user.")
                break


if __name__ == "__main__":
    server()
