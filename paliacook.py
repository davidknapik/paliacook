import time
import sys
import logging
import pyautogui
import argparse

#
#
pyautogui.FAILSAFE = True
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


#
# Get arguments
parser=argparse.ArgumentParser()
parser.add_argument("-d","--detect", help="detect only", action="store_true")
args=parser.parse_args()


def main():
    """main loop"""
    exit_value = None


    while exit_value is None:
        # exit_value = detect_exit()

        # Chopping
        if  pyautogui.pixelMatchesColor( 1176, 308, (83, 203, 255), tolerance=2) :
            logging.info('(%s) found pixel: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1176,308)))
            if not args.detect:
                # Click the mouse
                # NOTE: pyautogui.click() was too fast and not detected, needed a way to slow it down.
                pyautogui.mouseDown()
                time.sleep(0.01)
                pyautogui.mouseUp()

        # # Mixing
        #     # RGB: 250, 232, 89
        #     # Hex: fae859
        #     # X: 1116 Y: 332
        # while pyautogui.pixelMatchesColor( 1116, 332, (250, 232, 89), tolerance=2) :
        #     logging.info('(%s) found pixel: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1176,308)))
        #     # pyautogui.mouseDown()




if __name__ == "__main__":
    main()