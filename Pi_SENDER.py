import socket
import time

# PC'nin IP adresi ve port numarası
PC_IP = "192.168.1.100"  # Buraya PC'nin IP adresini yazın
PC_PORT = 5005

# UDP soketi oluşturma
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        message = "Merhaba, bu bir test mesajıdır."
        sock.sendto(message.encode(), (PC_IP, PC_PORT))
        print(f"Mesaj gönderildi: {message}")
        time.sleep(1)  # Mesaj gönderim aralığı (1 saniye)
except KeyboardInterrupt:
    print("Gönderim durduruldu.")
finally:
    sock.close()
