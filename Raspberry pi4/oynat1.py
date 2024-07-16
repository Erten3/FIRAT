import cv2

# Video dosyasını aç
cap = cv2.VideoCapture('video.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Video', frame)
        
        # 'q' tuşuna basarak videoyu durdurun
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()