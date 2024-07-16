from gpiozero import PWMOutputDevice, DigitalOutputDevice, DigitalInputDevice, Servo, DistanceSensor
from time import sleep, time

# Motor sürücü pinleri
ENA = PWMOutputDevice(17, frequency=1000)
IN1 = DigitalOutputDevice(22)
IN2 = DigitalOutputDevice(27)
ENB = PWMOutputDevice(25, frequency=1000)
IN3 = DigitalOutputDevice(23)
IN4 = DigitalOutputDevice(24)

# Encoder pinleri
# ENCODER1_PIN = 5  # Sol Encoder
# ENCODER2_PIN = 6  # Sağ Encoder

# Servo motor ve ultrasonik sensör pinleri
SERVO_PIN = 13
# TRIG_PIN = 16
# ECHO_PIN = 26

# Encoder'lar için DigitalInputDevice nesneleri
# encoder1 = DigitalInputDevice(ENCODER1_PIN)
# encoder2 = DigitalInputDevice(ENCODER2_PIN)

# Servo motor nesnesi
servo = Servo(SERVO_PIN)

# Ultrasonik sensör nesnesi
# ultrasonic = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

# Değişkenler
encoder1_count = 0
encoder2_count = 0
last_time = time()

# Encoder geri çağırma fonksiyonları
def encoder1_pulse():
    global encoder1_count
    encoder1_count += 1

def encoder2_pulse():
    global encoder2_count
    encoder2_count += 1

# Encoder geri çağırmalarını ayarlayın
# encoder1.when_activated = encoder1_pulse
# encoder2.when_activated = encoder2_pulse

def calculate_rpm(encoder_count, interval):
    # 20 pulse per revolution
    return (encoder_count / 20) * (60 / interval)

def sweep_servo():
    for angle in range(-100, 101, 5):
        servo.value = angle / 100.0
        sleep(0.05)
#         distance = ultrasonic.distance * 100  # Mesafeyi cm cinsinden al
#         print(f"Servo Angle: {angle}, Distance: {distance:.2f} cm")
    for angle in range(100, -101, -5):
        servo.value = angle / 100.0
        sleep(0.05)
#         distance = ultrasonic.distance * 100  # Mesafeyi cm cinsinden al
#         print(f"Servo Angle: {angle}, Distance: {distance:.2f} cm")
    
    servo.value = 0  # Servoyu ortalıyoruz

def print_rpm():
    global last_time, encoder1_count, encoder2_count
    current_time = time()
    elapsed_time = current_time - last_time
    if elapsed_time >= 1:
#         rpm1 = calculate_rpm(encoder1_count, elapsed_time)
#         rpm2 = calculate_rpm(encoder2_count, elapsed_time)
#         print(f"Motor 1 RPM: {rpm1}")
#         print(f"Motor 2 RPM: {rpm2}")
        encoder1_count = 0
        encoder2_count = 0
        last_time = current_time

IN1.on()
IN2.off()
IN3.on()
IN4.off()

print("Servo control script started.")
sweep_servo()  # Servo motoru belirli açılarda hareket ettir ve mesafe ölç
sleep(1)
print("Motor control script started.")

try:
    while True:
        print("Motors are accelerating...")
        for duty_cycle in range(0, 101, 5):
            ENA.value = duty_cycle / 100.0
            ENB.value = duty_cycle / 100.0
            print(f"Speed: {duty_cycle}%")
            for _ in range(5):  # 1 saniye boyunca RPM ölç ve yazdır
                print_rpm() # RPM Değerlerini yazdır
                sleep(0.1)

        print("Motors at maximum speed, waiting...")
        for _ in range(20):  # 2 saniye boyunca RPM ölç ve yazdır
            print_rpm()
            sleep(0.1)

        print("Motors are decelerating...")
        for duty_cycle in range(100, 59, -5):
            ENA.value = duty_cycle / 100.0
            ENB.value = duty_cycle / 100.0
            print(f"Speed: {duty_cycle}%")
            for _ in range(5):  # 1 saniye boyunca RPM ölç ve yazdır
                print_rpm() # RPM Değerlerini yazdır
                sleep(0.1)

            if duty_cycle == 60:
                sleep(15)

        print("Motors stopped, waiting...")
        for _ in range(20):  # 2 saniye boyunca RPM ölç ve yazdır
            print_rpm()
            sleep(0.1)

finally:
    ENA.off()
    ENB.off()
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    print("Motor control script stopped.")