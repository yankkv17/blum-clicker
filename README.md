# Automatic Clicker for Telegram Bot

# Info

Due to the game update, the code has been revised. This is a temporary solution. Currently, bombs are adding points instead of deducting them. The code will be improved. It is consistently possible to score 200+ points now.

## Description
This project is an automatic clicker for the Blum.

## Important Disclaimer
**This tool is created solely for educational purposes.**

### Disclaimer
Please consider the following before using this tool:
1. Using automation to interact with other bots may violate their rules and policies.
2. Bot owners may be against the use of automation, and this may lead to the blocking of your Telegram account or restrictions on access to the bot.
3. Before using the tool, make sure it does not violate any terms of use or user agreements associated with the bot.

The author of this tool is not responsible for any consequences related to its use.

## Download and Setup 
 * git clone [https://github.com/yankkv17/blum-clicker](https://github.com/yankkv17/blum-clicker)
 * Create virtual environment: python -m venv venv
 * venv/scripts/activate
 * pip install -r requirements.txt
 * python clicker.py

## Technologies Used
- Python
- PyAutoGUI
- OpenCV
- NumPy

##
This is the initial version of the clicker tool. Further updates and improvements may be made in the future.

## Updates
- Thanks to `template_6`, the script automatically continues the game. If you do not want this, comment out the line `('template_6', cv2.imread('template_6.png', cv2.IMREAD_COLOR)),`.
- The script consistently collects 200 stars.
- Automatic window size detection has also been implemented.

## Demonstration
<div align="center">

![YouCut_20240627_232949474(1)](https://github.com/yankkv17/blum-clicker/assets/166509664/1b0f19f4-1a1b-4d4f-9868-5181af693fee)
<div align="center">

