import socket
import threading

# List to hold all client connections and their usernames
clients = []
usernames = []

# Broadcast function to send messages to all clients
def broadcast(message, client, username):
    formatted_message = f"{username}: {message.decode('utf-8')}"
    for c in clients:
        if c != client:
            try:
                c.send(formatted_message.encode('utf-8'))
            except:
                clients.remove(c)

# Handle each client connection
def handle(client):
    username = None
    try:
        # Receive the first message as the username
        username = client.recv(1024).decode('utf-8')
        
        # Append username to the list and acknowledge the connection
        usernames.append(username)
        clients.append(client)
        print(f"Username of the client is {username}!")
        
        # Acknowledge the username to the client (Do not broadcast the first message)
        client.send("You are now connected!".encode('utf-8'))  
        
        # Broadcast that the user has joined the chat (excluding their first message)
        broadcast(f"{username} has joined the chat!".encode('utf-8'), client, "Server")
        
        # Now, only broadcast actual chat messages (after username is set)
        while True:
            message = client.recv(1024)
            if message:
                broadcast(message, client, username)  # Broadcast regular chat message
            else:
                break  # If no message, client has disconnected

    except Exception as e:
        print(f"Error with client: {e}")
        if username:
            index = usernames.index(username)
            usernames.remove(username)
            clients.remove(client)
            broadcast(f"{username} has left the chat!".encode('utf-8'), client, "Server")
    finally:
        client.close()

# Accept new client connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connection from {address} has been established!")
        
        # Handle the client in a separate thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to 127.0.0.1 for local testing
server.bind(('127.0.0.1', 12345))  # This binds to the loopback address (localhost)
server.listen()

# Print server's IP address (this will be '127.0.0.1')
print("Server is listening on IP address: 127.0.0.1, port: 12345")

# Start receiving clients
receive()
