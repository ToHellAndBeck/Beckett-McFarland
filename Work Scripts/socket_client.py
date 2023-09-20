import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify the server's IP address and port to connect to
server_name = 'low-0734330'
server_ip = socket.gethostbyname(server_name)  # Replace with the actual IP address of the server
server_port = 12345  # Use the same port as in the server script

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Send a message to the server
    message = input("Enter your message: ")
    client_socket.send(message.encode('utf-8'))

    # Receive a response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received from server: {response}")

# Close the socket
client_socket.close()
