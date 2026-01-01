import socket
import sys

# Configuration
SERVER_IP = "192.168.1.100"  # Your board's IP address
SERVER_PORT = 7              # Echo server port
TIMEOUT = 5                  # Socket timeout in seconds

def send_and_receive(message):
    """
    Connect to the board, send a message, and receive the response.
    """
    client_socket = None
    
    try:
        # Create TCP socket
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        
        # Connect to server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected successfully!\n")
        
        # Send message
        print(f"Sending: {message}")
        client_socket.sendall(message.encode('utf-8'))
        print("Message sent.\n")
        
        # Receive response
        print("Waiting for response...")
        response = b""
        while True:
            try:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                response += chunk
                # If we've received the end marker, break
                if b"=====================" in response:
                    break
            except socket.timeout:
                # No more data coming
                break
        
        # Print response
        if response:
            print("Response received:")
            print("=" * 60)
            print(response.decode('utf-8', errors='replace'))
            print("=" * 60)
        else:
            print("No response received from server.")
        
        return response
        
    except socket.timeout:
        print(f"Error: Connection timed out after {TIMEOUT} seconds")
        print("Check if the board is powered on and connected to the network.")
        return None
        
    except ConnectionRefusedError:
        print(f"Error: Connection refused by {SERVER_IP}:{SERVER_PORT}")
        print("Check if the server application is running on the board.")
        return None
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return None
        
    finally:
        # Close socket
        if client_socket:
            client_socket.close()
            print("\nConnection closed.")

def main():
    """
    Main function - send "Hello" to the board
    """
    print("=" * 60)
    print("TCP Client - Sending message to board")
    print("=" * 60)
    print()
    
    # Send the message
    message = "Hello, Server!"
    send_and_receive(message)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()