import base64

def encode_connection(ip, port):
    raw = f"{ip}:{port}"
    code = base64.urlsafe_b64encode(raw.encode()).decode()
    return code

def decode_connection(code):
    raw = base64.urlsafe_b64decode(code.encode()).decode()
    ip, port = raw.split(":")
    return ip, int(port)

if __name__ == "__main__":
    print("Connection Code Utility")
    choice = input("Encode (e) or Decode (d)? ").strip().lower()
    if choice == 'e':
        ip = input("Enter IP: ")
        port = input("Enter Port: ")
        print("Code:", encode_connection(ip, port))
    elif choice == 'd':
        code = input("Enter code: ")
        ip, port = decode_connection(code)
        print(f"IP: {ip}, Port: {port}")
    else:
        print("Invalid choice.")
