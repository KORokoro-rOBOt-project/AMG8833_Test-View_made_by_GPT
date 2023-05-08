import time
import board
import busio
import adafruit_amg88xx
import numpy as np
import cv2

# サーマルカメラをI2Cバスに接続する
i2c_bus = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c_bus)

# カラーマップ
COLORS = [(i, i, i) for i in range(256)]

# OpenCVウィンドウを作成する
cv2.namedWindow("Thermal Camera", cv2.WINDOW_NORMAL)

# メインループ
while True:
    # 温度データを取得する
    temps = amg.pixels
    max_temp = np.max(temps)
    # 温度データを0から255に正規化する
    normalized_temps = np.interp(temps, (np.min(temps), max_temp), (0, 255)).astype(np.uint8)
    # 8x8のグレースケールデータを3次元のNumPy配列に変換する
    gray_array = cv2.cvtColor(normalized_temps, cv2.COLOR_GRAY2BGR)
    # ウィンドウにグレースケールデータを表示する
    cv2.imshow("Thermal Camera", gray_array)
    # 最高温度を表示する
    print(f"Max Temperature: {max_temp:.2f} °C")
    # 20ms間隔でキー入力を待機し、qが押されたらループを終了する
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break