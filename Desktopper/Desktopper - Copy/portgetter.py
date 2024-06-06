import socket
import concurrent.futures

# Target IP address (Change it to the IP address you want to scan)
target_ip = "184.190.104.254"
# Start and end of the port range to scan
start_port = 5000
end_port = 8999
def check_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout for the socket connection in seconds
            # Attempt to connect to the port
            connection = s.connect_ex((target_ip, port))
            if connection == 0:
                return port
            else:
                ...
    except socket.error as err:
        ...

def get_open_ports():
    # Using ThreadPoolExecutor to scan ports concurrently for faster execution
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, port) for port in range(start_port, end_port + 1)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return open_ports

if __name__ == '__main__':
    for port in get_open_ports():
        print(f"{target_ip}:{port}")