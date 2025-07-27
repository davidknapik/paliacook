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

if args.detect:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def do_chop():
    # Chopping Board

    # The intention here was to have a way for the chop occur before the chop bar entered the zone
    delta_x = -10 

    #
    # Detect chopping board
    while pyautogui.pixelMatchesColor( 1277, 300, (210, 164, 85), tolerance=2):
        logging.debug('(%s) found chopping board: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1279,253)))

        #
        # Detect when moving block comes into range
        if  pyautogui.pixelMatchesColor( 1175+delta_x, 308, (83, 203, 255), tolerance=2) :
            logging.debug('(%s) found chop range pixel: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1176,308)))

            if not args.detect:
                # Click the mouse

                #
                # NOTE: pyautogui.click() was too fast and not detected by the game, needed a way to slow it down.
                pyautogui.mouseDown()
                # time.sleep(0.01)  # taken out
                pyautogui.mouseUp()
                logging.info('(%s) Chop!' , sys._getframe().f_code.co_name)
    return


def do_mixing():
    # Mixing Bowl

    #
    # Detect mixing bowl
    while pyautogui.pixelMatchesColor( 1000, 430, (217, 189, 111), tolerance=2) :
        logging.debug('(%s) found mixing bowl: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1000,430)))

        #
        # mousedown should change bowl rim color to yellow and start mixing
        pyautogui.mouseDown()
        time.sleep(0.5)

        #
        # keep mixing until the bowl color changes to white
        while pyautogui.pixelMatchesColor( 1116, 332, (250, 232, 89), tolerance=2) :
            logging.debug('(%s) Checking mixing bowl: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1116,332)))
            logging.info('(%s) Mixing!' , sys._getframe().f_code.co_name)
            time.sleep(5)

        pyautogui.mouseUp()
        logging.info('(%s) Stopped Mixing!' , sys._getframe().f_code.co_name)

    return

def do_roll():
    # Rolling Pin

    #
    # Detect rolling board
    while pyautogui.pixelMatchesColor( 598, 834, (208, 164, 85), tolerance=2):
        logging.debug('(%s) found rolling board: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1279,253)))

        #
        # Detect when moving block comes into range
        if  (pyautogui.pixelMatchesColor( 592, 308, (152, 223, 251), tolerance=3) | pyautogui.pixelMatchesColor( 592, 783, (163, 227, 250), tolerance=3)):
            logging.debug('(%s) found roll range pixel: %s' , sys._getframe().f_code.co_name, str(pyautogui.pixel(1176,308)))

            if not args.detect:
                # Click the mouse

                #
                # NOTE: pyautogui.click() was too fast and not detected, needed a way to slow it down.
                pyautogui.mouseDown()
                # time.sleep(0.01)
                pyautogui.mouseUp()
                logging.info('(%s) Roll!' , sys._getframe().f_code.co_name)
    return



def main():
    """main loop"""
    exit_value = None

    while exit_value is None:
        # exit_value = detect_exit()

        do_chop()
        do_mixing()
        do_roll()



if __name__ == "__main__":
    main()