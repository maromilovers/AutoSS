import os
import datetime
import subprocess
import pyautogui
import ctypes
import sys
import time
import shutil
import win32gui
from PIL import ImageGrab
import getTerminals
import searchNumber

def imagePath(filename):
  if hasattr(sys, "_MEIPASS"):
      return os.path.join(sys._MEIPASS, filename)
  return os.path.join(filename)


if __name__ == '__main__':

    #保存フォルダ名
    savedir = os.path.dirname(os.path.abspath("__file__"))  + '/' + datetime.datetime.today().strftime("%m%d %H%M")

    #保存用フォルダが存在する場合は削除
    if os.path.exists(savedir) :
        shutil.rmtree(savedir)
        time.sleep(1)
  
    #保存用フォルダ作成
    os.makedirs(savedir)

    #保存ファイル名
    savefile = savedir + r'\AllTerminals.png'

    #起動確認
    #オープンしているウィンドウから対象の名前のものを格納する
    handle = ctypes.windll.user32.FindWindowW(0, "対象の名前")

    #起動している場合、ウィンドウを最前面に設定
    if handle != 0:
    #    ctypes.windll.user32.SetForegroundWindow(handle)
    #    imagePos = pyautogui.locateCenterOnScreen(imagePath("images/all.png"))
    #    if imagePos is not None:
    #        pyautogui.click(imagePos[0], imagePos[1])
    #        time.sleep(5)
        ctypes.windll.user32.SendMessageA(handle,0x0010,0,0) 
        
    #起動ししばらく待つ
    result = subprocess.Popen(r'C:\bin\Target.exe', cwd=r'C:\bin')
    print(result)
    time.sleep(8)

    #対象ボタン押下
    imagePos = pyautogui.locateCenterOnScreen(imagePath("images/TargetButton.png"))
    if imagePos is None:
        print('対象ボタンが取得できませんでした')
        sys.exit(1)
    else:
        pyautogui.click(imagePos[0], imagePos[1])

    time.sleep(5)

    hd = win32gui.FindWindow(None, "対象の名前")
    rect = win32gui.GetWindowRect(hd)
    grabed_image = ImageGrab.grab()
    croped_image = grabed_image.crop(rect)

    croped_image.save(savefile)
    time.sleep(3)

    getTerminals.detect_contour(savefile)

    searchNumber.output_details(savedir)

    if os.path.exists('click') :
        shutil.rmtree('click')