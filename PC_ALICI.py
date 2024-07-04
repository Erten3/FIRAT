import socket

# Raspberry Pi'den gelen mesajları dinleyecek IP adresi ve port numarası
PC_IP = "192.168.1.10"  # PC'nin IP adresi
PC_PORT = 5005

# UDP soketi oluşturma ve bind işlemi
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PC_IP, PC_PORT))

print(f"{PC_IP}:{PC_PORT} adresinde mesaj bekleniyor...")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Maksimum 1024 byte veri al
        print(f"Gelen mesaj: {data.decode()} - Gönderen: {addr}")
except KeyboardInterrupt:
    print("Alım durduruldu.")
finally:
    sock.close()
