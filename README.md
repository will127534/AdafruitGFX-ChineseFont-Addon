# AdafruitGFX-ChineseFont-Addon
A modified version of Adafruit GFX for 正體中文字型檔案 

## How it works
由於中文字體對於嵌入式硬體(MCU)來說，算是有點大。對於點陣字型來說通常都要個~1Mb，除非用外掛Flash的方式儲存。所以要使用這個軟體必須先定義需要的字，再算出來hash function(UTF-8 to array index)，同時從字型檔案當中取出點陣圖。  
另外因為目前Arduino常見的一個Graphic library是Adafruit GFX，所以再將Hash function與點陣圖檔都輸出成Adafruit GFX font的格式方便使用，不過還是需要修改Adafruit GFX才能支援直接對UTF-8的輸出  
字型檔案格式是倚天中文系統的字型檔，但是是由國喬中文系統點陣字型檔轉檔過來的，連結如下: http://ftp.isu.edu.tw/pub/Windows/Chinese/font/bmp_font/kc_to_eten/ 

目前設定的點陣大小是24x24，可能晚點再來寫成可以自訂的模式。  
而(Minimal) Perfect Hash Functions Generator的範例是來自於
http://iswsa.acm.org/mphf/mphf.py


## Usage
以weather.txt作為範例，這是從CWB Opendata下載下來的說明檔案的中文字  
首先是將weather.txt當中取出獨立的中文字  

```python .\discrete_utf8.py .\weather.txt ```

再來就是計算MPH與輸出字型檔案  

```python .\hash.py ```

輸出的檔案是 userfont.h，搬移到Adafruit GFX library底下的\Fonts  
然後再Arduino code裡面使用方式如下:  

```c 
  #include <Fonts/userfont.h>
  display.begin();
  display.setFont(&user_fontGFXfont);  //setup font
  display.set_lookup(lookup);          //setup font hash function
  
  display.write("晴天\n");
  display.refresh();
```
