import pyautogui
import cv2
import numpy as np
import concurrent.futures
import time

# Function to get the window coordinates
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

# Templates.
star_templates = [
    ('template_1', cv2.imread('template_1.png', cv2.IMREAD_COLOR)),
    ('template_2', cv2.imread('template_2.png', cv2.IMREAD_COLOR)),
    ('template_3', cv2.imread('template_3.png', cv2.IMREAD_COLOR)),
    ('template_4', cv2.imread('template_4.png', cv2.IMREAD_COLOR)),
    ('template_5', cv2.imread('template_5.png', cv2.IMREAD_COLOR)),
    ('template_6', cv2.imread('template_6.png', cv2.IMREAD_COLOR)),
    ('template_7', cv2.imread('template_7.png', cv2.IMREAD_COLOR)),
    ('template_8', cv2.imread('template_8.png', cv2.IMREAD_COLOR)),
    ('template_9', cv2.imread('template_9.png', cv2.IMREAD_COLOR)),
    ('template_10', cv2.imread('template_10.png', cv2.IMREAD_COLOR)),
    ('template_11', cv2.imread('template_11.png', cv2.IMREAD_COLOR)),
    ('template_12', cv2.imread('template_12.png', cv2.IMREAD_COLOR)),
    ('template_13', cv2.imread('template_13.png', cv2.IMREAD_COLOR)),
    ('template_14', cv2.imread('template_14.png', cv2.IMREAD_COLOR)),
]

# Initialize region variables
region_left, region_top, region_width, region_height = get_window("TelegramDesktop")

# Make a screenshot of a specified region.
def grab_screen(scale_factor=0.6):
    screenshot = pyautogui.screenshot(region=(region_left, region_top, region_width, region_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    new_width = int(screenshot.shape[1] * scale_factor)
    new_height = int(screenshot.shape[0] * scale_factor)
    resized_screenshot = cv2.resize(screenshot, (new_width, new_height))
    return resized_screenshot

# Find a template on the screen.
def find_template_on_screen(template, screenshot, step=0.6, scale_factor=0.6):
    new_width = int(template.shape[1] * scale_factor)
    new_height = int(template.shape[0] * scale_factor)
    resized_template = cv2.resize(template, (new_width, new_height))
    result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= step:
        return (int(max_loc[0] / scale_factor), int(max_loc[1] / scale_factor))
    return None

# Click on the coordinates, that matches with templates.
def click_on_screen(position, template_width, template_height):
    center_x = position[0] + template_width // 2
    center_y = position[1] + template_height // 2
    pyautogui.click(center_x + region_left, center_y + region_top)

# Process a template in a separate thread
def process_template(template_data, screenshot, scale_factor):
    template_name, template = template_data
    position = find_template_on_screen(template, screenshot, scale_factor=scale_factor)
    if position:
        template_height, template_width, _ = template.shape
        click_on_screen(position, template_width, template_height)
        return template_name, position
    return template_name, None

def main():
    star_count = 0
    scale_factor = 0.6
    try:
        while True:
            start_time = time.time()
            screenshot = grab_screen(scale_factor)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_template, template_data, screenshot, scale_factor) for template_data in star_templates]
                for future in concurrent.futures.as_completed(futures):
                    template_name, position = future.result()
                    if position:
                        star_count += 1
                        print(f"Clicked at position: {position} for {template_name}")
                    else:
                        print(f"No matching template found for {template_name}")
            time_spend = time.time() - start_time
            print(f"Loop took {time_spend:.2f} seconds")
    except KeyboardInterrupt:
        print(f'Total stars caught: {star_count}')

if __name__ == "__main__":
    main()
