import pytesseract
import glob
import ctypes
import cv2
import pyautogui
import time
import win32gui
from PIL import Image
from PIL import ImageGrab
import main

def output_details(dir):

    files = glob.glob('click/*')

    unknown_count = 1

    handle = ctypes.windll.user32.FindWindowW(0, "対象の名前")

    for file in files:
        src = cv2.imread(file, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        #gray2 = cv2.bitwise_not(gray)
        #cv2.imwrite('sample/nega.png', gray)
        retval, bw = cv2.threshold(gray, 117, 255, cv2.THRESH_BINARY)
        #cv2.imwrite("gray.png", bw)

        h, w = gray.shape[:2]

        n = 2
        hosei = 3
        x0 = int(w/n)
        y0 = int(h/n)
        #c = [gray[y0*y:y0*(y+1), 0:w] for y in range(n)]
        #c = [src[0:h, x0*x:x0*(x+1)] for x in range(n)]
        c = [gray[y0*y+hosei:y0*(y+1)-hosei, x0*x+hosei:x0*(x+1)-hosei] for x in range(n) for y in range(n)]

        #cv2.imwrite("sample/c.png", c[0])
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        number = pytesseract.image_to_string(c[0])
        if number[0:13] == '':
            print('なし')
            pass
        else:
            #次画面へ遷移
            img = src[5:src.shape[0]-5, 5:src.shape[1]-5]
            cv2.imwrite('sample/img.png', img)
            #a = input()
            ctypes.windll.user32.SetForegroundWindow(handle)
            imgTerminal = pyautogui.locateCenterOnScreen(img, grayscale = True)
            if imgTerminal is None:
                print('画面に該当なし')
                continue
            else:
                pyautogui.click(imgTerminal[0], imgTerminal[1])
            time.sleep(1)

            imgBack = pyautogui.locateCenterOnScreen(main.imagePath('images/back.png'))
            if imgBack is None:
                print('戻るボタンなし')
                continue
            
        
            #IDの形式チェック
            flg = True
        
            if number[0:4].isdigit() == False:
                flg = False
            if number[4:5] != '-':
                flg = False
            if number[5:9].isdigit() == False:
                flg = False
            if number[9:10] != '-':
                flg = False
            if number[10:13].isdigit() == False:
                flg = False
        
            if flg:
                #print(number[0:13])
                filename = number[0:13] + '.png'
            else:
                filename = 'ID不明' + str(unknown_count) + '.png'
                unknown_count =+ 1
        
            filename = dir + '/' + filename
        
            hd = win32gui.FindWindow(None, "対象詳細の名前)
            rect = win32gui.GetWindowRect(hd)
            grabed_image = ImageGrab.grab()
            croped_image = grabed_image.crop(rect)
            croped_image.save(filename)
        
            #前画面に遷移
            pyautogui.click(imgBack[0], imgBack[1])
            time.sleep(1)
            
    #画面を閉じる
    ctypes.windll.user32.SendMessageA(handle,0x0010,0,0) 
    
if __name__ == '__main__':

    dir = 'test'
    output_details(dir)
