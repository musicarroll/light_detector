int light0=0;
int light1=0;
int light2=0;
int light3=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:
  light0 = analogRead(A0);
  light1 = analogRead(A1);
  light2 = analogRead(A2);
  light3 = analogRead(A3);
  Serial.print("Light0=");
  Serial.print(light0); 
  Serial.print("\tLight1=");
  Serial.print(light1); 
  Serial.print("\tLight2=");
  Serial.print(light2); 
  Serial.print("\tLight3=");
  Serial.println(light3); 
}
