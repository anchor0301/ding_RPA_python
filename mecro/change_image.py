from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
import pyautogui
import keyboard
import time

from line_notify import LineNotify
ERROR_TOKEN = "LoRFWtQxndakmcniVZIymNCNKcqKitRy5Aqd0dy5G0A"  # 에러 코드
error_notify = LineNotify(ERROR_TOKEN)


import time

def PixelCheck(x1, y1, x2, y2):
    time.sleep(1)
    im1 = ImageGrab.grab((x1, y1, x2, y2))
    # Take a snapshot of the screen. The pixels inside the bounding box are returned as an “RGB” image
    # on Windows or “RGBA” on macOS. If the bounding box is omitted, the entire screen is copied.
    while 1:
        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'r')  # ctrl 키를 누릅니다.

        time.sleep(10)
        im2 = ImageGrab.grab((x1, y1, x2, y2))
        im = ImageChops.difference(im1, im2)
        # Returns the absolute value of the pixel-by-pixel difference between the two images.
        # 마우스로 인한 변경은 반영 되지 않는다. 같은 이미지이면 difference()의 결과 이미지는 모든 픽셀이 0.
        stat = ImageStat.Stat(im)
        # Calculate statistics for the given image. If a mask is included, only the regions covered by
        # that mask are included in the statistics. You can also pass in a previously calculated histogram.
        if stat.sum != [0, 0, 0]:  # Sum of all pixels for each band in the image.
            print("Change detected: sum[%s]: %s" % (im.getbands().__str__(), stat.sum.__str__()))
            error_notify.send("!!변화 감지!!")
            # Returns a tuple containing the name of each band in this image. For example, getbands on
            # an RGB image returns (“R”, “G”, “B”).
            return


#x1, y1, x2, y2 = map(int, input("Enter x1, y1, x2, y2 values: ").split())  # 추적할 영역의 좌상단, 우하단 좌표
PixelCheck(863, 803, 1182, 986)
# x1, y1, x2, y2 = input("Enter x1, y1, x2, y2 values: ").split()
# x1 = int(x1)
# y1 = int(y1)
# x2 = int(x2)
# y2 = int(y2)

