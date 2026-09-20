import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Create a global client socket variable
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = None  # Define the username variable globally

# Function to connect to the server
def connect_to_server():
    global username  # Ensure we're using the global username variable
    ip = ip_entry.get()  # Get IP from the user input
    port = 12345  # Use the same port as the server
    try:
        client.connect((ip, port))  # Try connecting to the server
        username = simpledialog.askstring("Username", "Enter your username:")
        client.send(username.encode('utf-8'))  # Send the username to the server
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        # After connecting, show the message input box
        message_box.pack()
        send_button.pack()

        # Disable the IP entry and connect button after successful connection
        ip_entry.config(state='disabled')
        connect_button.config(state='disabled')
    except Exception as e:
        chat_box.insert(tk.END, f"Error: {e}\nFailed to connect. Please try again.\n")

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_box.insert(tk.END, message + '\n')  # Insert received message into chat box
        except Exception as e:
            chat_box.insert(tk.END, f"Error receiving message: {e}\n")
            break

# Function to send messages to the server
def send_message():
    global username  # Ensure we're using the global username variable
    message = message_box.get()
    if message:
        formatted_message = f"{message}"  # Include username with message
        client.send(formatted_message.encode('utf-8'))
        message_box.delete(0, tk.END)
        chat_box.insert(tk.END, "Me: "+formatted_message + '\n')  # Show own message in chat

# Create GUI window
window = tk.Tk()
window.title("Python Chat")

# Chat display box
chat_box = tk.Text(window, height=20, width=50)
chat_box.pack()

# IP address input field
ip_label = tk.Label(window, text="Enter Server IP:")
ip_label.pack()

ip_entry = tk.Entry(window, width=40)
ip_entry.insert(0, "127.0.0.1")  # Default to localhost
ip_entry.pack()

# Connect button
connect_button = tk.Button(window, text="Connect", command=connect_to_server)
connect_button.pack()

# Message input field (hidden until connected)
message_box = tk.Entry(window, width=40)
message_box.pack_forget()

# Send button (hidden until connected)
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack_forget()

# Start the GUI loop
window.mainloop()
