# AdafruitGFX-ChineseFont-Addon
A modified version of Adafruit GFX for 正體中文字型檔案 

## How it works
由於中文字體對於嵌入式硬體(MCU)來說，算是有點大。對於點陣字型來說通常都要個~1Mb，除非用外掛Flash的方式儲存。所以要使用這個軟體必須先定義需要的字，再算出來hash function(UTF-8 to array index)，同時從字型檔案當中取出點陣圖。  
另外因為目前Arduino常見的一個Graphic library是Adafruit GFX，所以再將Hash function與點陣圖檔都輸出成Adafruit GFX font的格式方便使用，不過還是需要修改Adafruit GFX才能支援直接對UTF-8的輸出  
字型檔案格式是倚天中文系統的字型檔，但是是由國喬中文系統點陣字型檔轉檔過來的，連結如下: http://ftp.isu.edu.tw/pub/Windows/Chinese/font/bmp_font/kc_to_eten/ 

目前預設的點陣大小是24x24，不過也可以選擇16x15的字形。  
而(Minimal) Perfect Hash Functions Generator的範例是來自於
http://iswsa.acm.org/mphf/mphf.py


## Usage
以weather.txt作為範例，這是從CWB Opendata下載下來的說明檔案的中文字  
首先是將weather.txt當中取出獨立的中文字  

```python .\discrete_utf8.py .\weather.txt ```

再來就是計算MPH與輸出字型檔案  

```python .\hash.py ```  
預設是全形24x24，半形12x24，如果需要16x15與8x15的話，後面加 -s就可以了  
```python .\hash.py -s```  
如果想看點陣字型的話，後面加上 -p  
```python .\hash.py -p```  

輸出的檔案是 userfont.h，搬移到Adafruit GFX library底下的\Fonts  
然後再Arduino code裡面使用方式如下:  

```c 
  #include <Fonts/userfont.h>
  display.begin();
  display.clearDisplay();
  display.setFont(&user_fontGFXfon);
  display.set_lookup(lookup);
  display.setTextColor(BLACK);

   for(int i=0x20; i<0x7F; i++){
       display.write(i);
   }
   display.println();
   display.println("多雲時陰陣雨或雷雨有霧陰時多雲短暫陣雨或雷雨");
   display.print("臺北ABCabc\nABCDEFG");
   display.println("臺中\n臺南");
   display.refresh();
```  
然後大概長這樣:   
![alt tag](picture.jpg)
## Change list

2017-02-05 增加了16x15 與 8x15的字形，修復println與print的bug  


