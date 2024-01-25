import threading
import tkinter as tk
from tkinter import scrolledtext
from pubsub import pub
from ftpClient.ftpClient import connectClient, startPushCommands
from utility import FTP_CLIENT_MESSAGE_TOPIC

HEIGHT = 500
WIDTH = 600

socket: any
connection_thread = None

def on_Message_Event(data):
    current_text = scrollable_label.get("1.0", tk.END)
    updated_text = f"{current_text}\n{data}"
    scrollable_label.delete("1.0", tk.END)
    scrollable_label.insert(tk.END, updated_text)
    
    # Scroll to the top after inserting new text
    scrollable_label.yview(tk.MOVETO, 1.0)

def connect_and_start(entry):
    global socket
    socket = connectClient(retry=2)
    if socket is not None:
        button.configure(text="Send", state=tk.NORMAL)
    else:
        button.configure(text="Connect", state=tk.NORMAL)

def publishMsg(entry):
    global connection_thread

    if button.cget("text") == "Send" and not entry:
        scrollable_label.delete("1.0", tk.END)
        scrollable_label.insert(tk.END, "Please enter a Valid entry")
        return

    if button.cget("text") == "Connect":
        button.configure(text="Connecting ...", state=tk.NORMAL)
        connection_thread = threading.Thread(target=lambda: connect_and_start(entry))
        connection_thread.start()

    elif button.cget("text") == "Send":
        if socket is not None:
            startPushCommands(socket, entry)
        else:
            button.configure(text="Connect", state=tk.NORMAL)

pub.subscribe(on_Message_Event, FTP_CLIENT_MESSAGE_TOPIC)
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#ff1100', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Connect", font=40, command=lambda: publishMsg(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)
lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

# Use ScrolledText instead of Label for scrollable text
scrollable_label = scrolledtext.ScrolledText(lower_frame, wrap=tk.WORD, font=("Courier", 10))
scrollable_label.place(relwidth=1, relheight=1)

root.mainloop()
