import pyautogui
import cv2
import numpy as np
import concurrent.futures
import time

# Templates.
star_templates = [
    ('template_1', cv2.imread('template_1.png', cv2.IMREAD_COLOR)),
    ('template_2', cv2.imread('template_2.png', cv2.IMREAD_COLOR)),
    ('template_3', cv2.imread('template_3.png', cv2.IMREAD_COLOR)),
    ('template_4', cv2.imread('template_4.png', cv2.IMREAD_COLOR)),
    ('template_5', cv2.imread('template_5.png', cv2.IMREAD_COLOR)),
]

# Search area settings.
screen_width, screen_height = pyautogui.size()
region_width = 402
region_height = 712
region_left = (screen_width - region_width) // 2
region_top = (screen_height - region_height) // 2
# Define the search area region.
region = (region_left, region_top, region_width, region_height)


# Make a screenshot of a specified region.
def grab_screen(region, scale_factor=0.5):
    screenshot = pyautogui.screenshot(
        region=(region[0], region[1], region[2], region[3]))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    # Resize the screenshot.
    new_width = int(screenshot.shape[1] * scale_factor)
    new_height = int(screenshot.shape[0] * scale_factor)
    resized_screenshot = cv2.resize(screenshot, (new_width, new_height))
    return resized_screenshot


# Find a template on the screen.
def find_template_on_screen(template, screenshot, step=0.7, scale_factor=0.5):
    # Resize the template.
    new_width = int(template.shape[1] * scale_factor)
    new_height = int(template.shape[0] * scale_factor)
    resized_template = cv2.resize(template, (new_width, new_height))
    # Template matching.
    result = cv2.matchTemplate(
        screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
    # Find the location with the maximum match.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= step:
        # Scale back the coordinates to the original size.
        return (int(max_loc[0] / scale_factor), int(max_loc[1] / scale_factor))
    return None


# Click on the coordinates, that matches with templates.
def click_on_screen(position, template_width, template_height):
    center_x = position[0] + template_width // 2
    center_y = position[1] + template_height // 2
    # Click on the center of the template.
    pyautogui.click(center_x + region_left, center_y + region_top)

# Process a template in a separate thread
def process_template(template_data, screenshot, scale_factor):
    template_name, template = template_data
    position = find_template_on_screen(
        template, screenshot, scale_factor=scale_factor)
    if position:
        template_height, template_width, _ = template.shape
        click_on_screen(position, template_width, template_height)
        return template_name, position
    return template_name, None


def main():
    star_count = 0
    scale_factor = 0.5
    try:
        # Infinite loop to monitor the screen for the termplates.
        while True:
            start_time = time.time()
            # Make a screenshot of the game window screen.
            screenshot = grab_screen(region, scale_factor)
            # Using ThreadPoolExecitor to procees templates together.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit tasks to process each template.
                futures = [executor.submit(
                    process_template, template_data, screenshot, scale_factor) for template_data in star_templates]
                for future in concurrent.futures.as_completed(futures):
                    # Get the result of each task.
                    template_name, position = future.result()
                    # Check if the template was dound
                    if position:
                        star_count += 1
                        # Print the position and template name for the found one.
                        print(f"Clicked at position: {
                              position} for {template_name}")
                    else:
                        # Print a message if can't found no mathcing tempalte at the screen.
                        print(f"No matching template found for {
                              template_name}")

            time_spend = time.time() - start_time
            print(f"Loop took {time_spend:.2f} seconds")

    except KeyboardInterrupt:
        print(f'Total stars caught: {star_count}')


if __name__ == "__main__":
    main()
