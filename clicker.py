import pyautogui
import cv2
import numpy as np

# Templates.
star_templates = [
    ('template_1', cv2.imread('template_1.png', cv2.IMREAD_COLOR)),
    ('template_2', cv2.imread('template_2.png', cv2.IMREAD_COLOR)),
    ('template_3', cv2.imread('template_3.png', cv2.IMREAD_COLOR)),
]

# Search area settings.
screen_width, screen_height = pyautogui.size()
region_width = 480
region_height = 553
region_left = (screen_width - region_width) // 2
region_top = (screen_height - region_height) // 2
# Define the search area region.
region = (region_left, region_top, region_width, region_height)

# Make a screenshot of a specified region.
def grab_screen(region):
    screenshot = pyautogui.screenshot(
        region=(region[0], region[1], region[2], region[3]))
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)


# Find a template on the screen.
def find_template_on_screen(template, step=0.6):
    screenshot = grab_screen(region)
    # Template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    # Find the location with the maximum match.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= step:
        return max_loc
    return None


# Click on the coordinates, that matches with templates
def click_on_screen(position, template_width, template_height):
    center_x = position[0] + template_width // 2
    center_y = position[1] + template_height // 2
    # Click on the center of the template.
    pyautogui.click(center_x + region_left, center_y + region_top)


def main():
    star_count = 0
    try:
        while True:
            # For loop to iterate each tempalte.
            for template_name, template in star_templates:
                # Find the template on the screen.
                position = find_template_on_screen(template, step=0.6)
                if position:
                    # Get the dimensions of the template.
                    template_height, template_width, _ = template.shape
                    # Click at the star.
                    click_on_screen(position, template_width, template_height)
                    star_count += 1
                    print(f"Сlicked at position: {position}")
                else:
                    print(f"No matching template found on the screen")
    except KeyboardInterrupt:
        print(f'Total stars caught: {star_count}')


if __name__ == "__main__":
    main()
