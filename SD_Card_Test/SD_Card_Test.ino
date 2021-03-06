#include <SD.h>

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <vector>

#define SCREEN_WIDTH 128 // OLED 寬度像素
#define SCREEN_HEIGHT 64 // OLED 高度像素

using namespace std;


// 設定OLED
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // 一般1306 OLED的位址都是0x3C
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0,0);
  display.setTextColor(BLACK, WHITE);
  display.println("Press G35!");
  display.display();

  pinMode(35, INPUT);
  while (digitalRead(35) == HIGH){
    delay(50);
  }

  if (!SD.begin(5)) {
    display.setTextColor(BLACK, WHITE);
    display.println("Can't find SD.");
    display.display();
    while (1);
  }


  File myFile = SD.open("/Arduino/frame_1.txt");
  if (myFile) {
    display.setTextColor(BLACK, WHITE);
    display.println("Found code");
    display.display();
    myFile.close();

    display.setTextColor(BLACK, WHITE);
    display.println("Press G35!");
    display.display();
    while (digitalRead(35) == HIGH){
    delay(50);
    }
    display.clearDisplay();
    display.display();
  } 
  else {
      display.setTextColor(BLACK, WHITE);
      display.println("Can't find code.txt");
      display.display();
      while(true){
        delay(1);
      }
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0 ; i <= 207 ; i++){
//    String Framecount = String(i);
    File myfile = SD.open("/Arduino/frame" + String(i) + ".c");
    
//    myFile.readBytesUntil(terminateChar, serialBuffer, bufferLength);
    unsigned char disp[1030];
    myfile.readBytes(disp, 1030);
    display.drawBitmap(0,0,disp, 128, 64,WHITE);
    
    display.display();  // 要有這行才會把文字顯示出來
    delay(33);
    display.clearDisplay();
    delay(1);
  }

}
