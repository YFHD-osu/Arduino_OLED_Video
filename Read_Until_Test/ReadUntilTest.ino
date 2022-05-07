void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned char frame[8192];
  String input = "ff0x, aa02, cc05";

  char *inputchar;
  input.toCharArray(inputchar, 10);
  
  char *namea = NULL;
  
  namea = strtok(inputchar, ",");
  int i = 0;
  while(namea != NULL)
  {
      frame[i] = namea;
      namea = strtok(NULL, ","); 
      i += 1;
  }
  Serial.println(frame[2]);
  delay(1000);
}
