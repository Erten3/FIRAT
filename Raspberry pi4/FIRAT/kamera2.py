import socket
import cv2
import numpy as np
import threading

# Sunucu bilgileri
HOST = '192.168.172.56'  # Tüm IP adreslerinden gelen bağlantılara izin verir
PORT = 9999

def handle_client_connection(conn, addr):
    print(f'Bağlantı kabul edildi: {addr}')
    data = b''

    while True:
        # Veri alımı
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet

        # Görüntü çerçevesini ayıklama
        if len(data) >= 4:
            frame_len = int.from_bytes(data[:4], byteorder='big')
            if len(data) >= 4 + frame_len:
                frame_data = data[4:4 + frame_len]
                data = data[4 + frame_len:]

                # Görüntü çerçevesini çözme ve gösterme
                frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow(f'Sunucu - Alinan Goruntu {addr}', frame)

                if cv2.waitKey(1) == 27:  # ESC tuşuna basıldığında çık
                    break

    # Kaynakları serbest bırakma
    conn.close()

# Socket oluşturma
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print('Sunucu başlatıldı, bağlantı bekleniyor...')

try:
    while True:
        # Bağlantı kabul etme
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
        client_thread.start()
finally:
    server_socket.close()
    cv2.destroyAllWindows()
