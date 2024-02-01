import threading
import pyautogui
import keyboard
from PIL import ImageGrab, Image
import pyperclip
import time

# 这是一个示例的复制按钮的图像。您需要将其替换为实际的复制按钮的图像。
# COPY_BUTTON_IMAGE_PATH = r"D:\pic\img.jpeg"
COPY_BUTTON_IMAGE_PATH = r"F:\pic\img.jpeg"

def remove_text_after_marker(text, marker="摘自："):
    index = text.find(marker)
    if index != -1:
        return text[:index]
    return text

def on_ctrl_c():
    # 获取当前鼠标位置
    x, y = pyautogui.position()
    # 定义搜索范围
    RADIUS = 100
    region = (x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
    # 截取鼠标附近的屏幕内容
    screenshot = ImageGrab.grab(bbox=region)
    # 查找复制按钮
    try:
        location = pyautogui.locate(COPY_BUTTON_IMAGE_PATH, screenshot, confidence=0.8)  # confidence 是匹配度
    except:
        location = None # 如果找不到复制按钮，则 location 为 None
    # 如果找到复制按钮，则点击它
    if location:
        center_x =location.left + location.width/ 2
        center_y = location.top + location.height / 2
        # center = pyautogui.center(location)
        pyautogui.click(center_x + region[0], center_y + region[1])
        # pyautogui.click(center.x + region[0], center.y + region[1])

def process():
    # 获取剪贴板内容
    prev_content = ""
    while True:

        clipboard_content = pyperclip.paste()
        # 只有当内容有变化时才处理，避免不必要的操作
        if clipboard_content != prev_content:
            modified_content = remove_text_after_marker(clipboard_content)
            # 如果内容被修改，则更新剪贴板
            if modified_content != clipboard_content:
                pyperclip.copy(modified_content)
            prev_content = modified_content
        if keyboard.is_pressed('esc'):
            keyboard.wait('esc')
        # 休眠一秒，避免过度占用 CPU
        time.sleep(1)
def main():
    # 设置 Ctrl+C 的监听
    keyboard.add_hotkey('ctrl+c', on_ctrl_c)
    # 保持程序运行
    t_on_ctrl_c = threading.Thread(target=on_ctrl_c,daemon=False)
    t_process = threading.Thread(target=process, daemon=False)
    t_process.start()
    t_on_ctrl_c.start()
    keyboard.wait('esc')  # 可以按 Esc 键退出程序
# keyboard.wait('esc') 是使用 keyboard 库的一个方法，它会暂停程序的执行直到指定的按键（在这种情况下是 'esc'）被按下。
if __name__=='__main__':
    main()