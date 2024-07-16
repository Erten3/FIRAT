import socket

# Doğru yerel IP adresinizi buraya yazın
udp_ip = "192.168.1.10"  # Bu adresi kendi IP adresinizle değiştirin
udp_port = 5005

# UDP soketi oluşturma
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))

print("Dinleniyor...")

while True:
    # Veriyi al
    data, addr = sock.recvfrom(1024)  # Maksimum 1024 byte veri alır

    # Veriyi UTF-8 formatında çöz
    message = data.decode('utf-8')

    # Mesajı ekrana yazdır
    print(f"Alındı: {message} from {addr}")

    if message.lower() == 'q':  # 'q' alınırsa döngüden çık
        break

sock.close()
