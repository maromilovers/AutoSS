import cv2
import numpy as np
import os
import shutil
import time

# 指定した画像(path)の物体を検出し、外接矩形の画像を出力します
def detect_contour(path):

  #保存用フォルダが存在する場合は削除
  if os.path.exists('click') :
    shutil.rmtree('click')
    time.sleep(1)
  
  #保存用フォルダ作成
  os.makedirs("click")

  # 画像を読込
  src = cv2.imread(path, cv2.IMREAD_COLOR)

  # グレースケール画像へ変換
  gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
  #反転処理もする
  gray2 = cv2.bitwise_not(gray)
  #cv2.imwrite("nega.jpg", gray2)
  
  # 2値化
  # 閾値170位がちょうどよさげ
  retval, bw = cv2.threshold(gray2, 170, 255, cv2.THRESH_BINARY)
  #cv2.imwrite("gray.jpg", bw)

  # 輪郭を抽出
  #   contours : [領域][Point No][0][x=0, y=1]
  #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
  #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
  contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  # 矩形検出された数（デフォルトで0を指定）
  detect_count = 0

  # 各輪郭に対する処理
  for i in range(0, len(contours)):

    # 輪郭の領域を計算
    area = cv2.contourArea(contours[i])

    # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
    # 1e4～1e5位がちょうどよさげ
    if area < 1e4 or 1e5 < area:
      continue

    # 外接矩形
    if len(contours[i]) > 0:
      rect = contours[i]
      x, y, w, h = cv2.boundingRect(rect)
      cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)

      # 外接矩形毎に画像を保存
      cv2.imwrite('click/' + str(detect_count) + '.png', src[y:y + h, x:x + w])

      detect_count = detect_count + 1

  # 外接矩形された画像を表示
  #cv2.imshow('output', src)
  #cv2.waitKey(0)

  # 終了処理
  #cv2.destroyAllWindows()

if __name__ == '__main__':

  path = 'AllTerminals.png'
  detect_contour(path)
