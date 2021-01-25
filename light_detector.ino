int light0=0;
int light1=0;
int buzzer = 11;
int high_counter = 0;
int med_counter = 0;
int low_counter = 0;
float THRESHOLD0 = 0.25;
float THRESHOLD1 = 0.25;
int lowtone = 220;
int hightone = 880;
float prevlight0 = 0.0;
float prevlight1 = 0.0;
int first_time = 1;
float change0 = 0.0;
float change1 = 0.0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  light0 = analogRead(A0);
  light1 = analogRead(A1);
  if (first_time==1) {
    first_time=0;
    prevlight0 = light0;
    prevlight1 = light1;
  }
  Serial.print("Light0=");
  Serial.print(light0); 
  Serial.print("\tLight1=");
  Serial.println(light1); 
  change0 = (prevlight0-light0)/prevlight0;
  Serial.println(change0);
  if ((prevlight0-light0)/prevlight0 <-THRESHOLD0) {
/*    Serial.print("Low!!!\n"); */
    tone(buzzer, lowtone);
    delay(10);
    noTone(buzzer);
    prevlight0=light0;
/*    low_counter++;
    Serial.print("Light0 Counter: ");
    Serial.println(low_counter,DEC);*/
  }
  change1 = (prevlight1-light1)/prevlight1;
  Serial.println(change1);

  if (change1 <-THRESHOLD1) {
/*    Serial.print("Low!!!\n"); */
    tone(buzzer, hightone);
    delay(10);
    noTone(buzzer);
    prevlight1=light1;
/*    high_counter++;
    Serial.print("Light1 Counter: ");
    Serial.println(high_counter,DEC);*/
  }

  
/*  else if (light>50 && light<=100) {
    Serial.print("Med!!!\n");
    tone(buzzer, 440);
    delay(500);
    noTone(buzzer);   
    med_counter++;
    Serial.print("Med Counter: ");
    Serial.println(med_counter,DEC);
  }
  else if (light>100 && light<=120) {
    Serial.print("High!!!\n");
    tone(buzzer, 880);
    delay(100);
    noTone(buzzer);   
    high_counter++;
    Serial.print("High Counter: ");
    Serial.println(high_counter,DEC);
  }*/
  
  delay(100);
  noTone(buzzer);
}
