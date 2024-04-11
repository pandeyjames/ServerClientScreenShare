import socket
from PIL import Image, ImageTk
import io
import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("Received Image")

# Create a label to display the image
label = tk.Label(root)
label.pack()

# Function to receive and display the screen image
def receive_and_display_image(s):
    try:
        while True:
            # Receive image size first
            img_size_bytes = s.recv(4)
            if not img_size_bytes:
                print("Connection closed by server.")
                break
            img_size = int.from_bytes(img_size_bytes, byteorder='big')
            print("Expecting image of size:", img_size, "bytes")

            # Receive image data based on image size
            screen_data = b''
            while len(screen_data) < img_size:
                chunk = s.recv(min(4096, img_size - len(screen_data)))
                if not chunk:
                    print("Connection closed by server.")
                    break
                screen_data += chunk

            if len(screen_data) == img_size:
                # Convert image data to PIL Image object
                img = Image.open(io.BytesIO(screen_data))
                # Resize the image if needed to fit the window
                img.thumbnail((800, 600))
                # Convert the image to Tkinter PhotoImage
                img_tk = ImageTk.PhotoImage(img)
                # Update the label with the new image
                label.img_tk = img_tk  # Store a reference to prevent garbage collection
                label.config(image=img_tk)
                # Update the Tkinter window
                root.update()
            else:
                print("Incomplete image data received from server.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Program terminated by user.")
        root.destroy()  # Destroy the Tkinter window before exiting
        raise  # Raise the exception again to exit the program

if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 12345))  # IP address and port of the server
            receive_and_display_image(s)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Program terminated by user.")

# Start the Tkinter event loop
root.mainloop()
