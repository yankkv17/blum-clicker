import pyautogui


def get_window(window):
    windows = pyautogui.getWindowsWithTitle(window)
    if windows:
        window = windows[0]
        region_left = window.left
        region_top = window.top
        region_width = window.width
        region_height = window.height
        return region_left, region_top, region_width, region_height
    else:
        raise Exception(f"Window with title '{window}' not found.")


# Enter ur window title in the "".
window = ""
try:
    region_left, region_top, region_width, region_height = get_window(
        window)
    print(f"Region: left={region_left}, top={region_top}, width={
          region_width}, height={region_height}")
except Exception as e:
    print(e)
