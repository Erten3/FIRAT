#include<Servo.h>
Servo x, y;
int genislik = 640, yukseklik = 480, xp = 90, yp = 90;  
const int aci = 2;  
void setup() {
  Serial.begin(9600);
  x.attach(12);
  y.attach(13);
}
void loop() {
  if (Serial.available() > 0)
  {
    int x_merkez, y_merkez;
    if (Serial.read() == 'X')
    {
      x_merkez = Serial.parseInt(); 
      if (Serial.read() == 'Y')
        y_merkez = Serial.parseInt(); 
    }
    if (x_merkez > genislik / 2 + 60)
      xp += aci;
      x.write(xp);
    if (x_merkez < genislik / 2 - 60)
      xp -= aci;
      x.write(xp);
    if (y_merkez < yukseklik / 2 + 60)
      yp -= aci;
      y.write(yp);
    if (y_merkez > yukseklik / 2 - 60)
      yp += aci;
      y.write(yp);
  }
}
