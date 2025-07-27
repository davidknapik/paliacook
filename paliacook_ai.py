import time
import sys
import logging
import pyautogui
import argparse
from dataclasses import dataclass

# --- Configuration ---
@dataclass
class TaskConfig:
    """Configuration for a single automation task station."""
    station_coords: tuple[int, int]
    station_color: tuple[int, int, int]
    action_coords: list[tuple[int, int]]
    action_colors: list[tuple[int, int, int]]
    action_name: str
    tolerance: int = 5

CONFIG = {
    "chop": TaskConfig(
        station_coords=(1277, 300),
        station_color=(210, 164, 85),
        action_coords=[(1165, 308)],  # Adjusted from 1175 + (-10)
        action_colors=[(83, 203, 255)],
        action_name="Chop"
    ),
    "mix": TaskConfig(
        station_coords=(1000, 430),
        station_color=(217, 189, 111),
        action_coords=[(1116, 332)], # The "in-progress" color pixel
        action_colors=[(250, 232, 89)],
        action_name="Mix"
    ),
    "roll": TaskConfig(
        station_coords=(598, 834),
        station_color=(208, 164, 85),
        action_coords=[(592, 308), (592, 783)],
        action_colors=[(152, 223, 251), (163, 227, 250)],
        action_name="Roll"
    )
}

# --- State-Based Functions  ---

def handle_chopping_station(detect_only: bool):
    """
    If the chopping station is detected, this function takes control
    and continuously checks for the action pixel until the station disappears.
    """
    cfg = CONFIG["chop"]
    # This loop ensures the function is "stuck" here as long as the chopping board is visible
    while pyautogui.pixelMatchesColor(*cfg.station_coords, cfg.station_color, tolerance=cfg.tolerance):
        logging.debug("Chopping station active...")
        # Check if the moving block is in the target zone
        if pyautogui.pixelMatchesColor(*cfg.action_coords[0], cfg.action_colors[0], tolerance=cfg.tolerance):
            logging.debug("Chop block in range.")
            if not detect_only:
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                logging.info("Chop!")
        # A small delay to prevent this blocking loop from maxing out the CPU
        time.sleep(0.01)

def handle_mixing_station(detect_only: bool):
    """
    If the mixing station is detected, this function performs the entire
    mixing process (mouse down, wait, mouse up) and then returns.
    """
    cfg = CONFIG["mix"]
    # This loop handles multiple batches if the player stays at the mixing station
    while pyautogui.pixelMatchesColor(*cfg.station_coords, cfg.station_color, tolerance=cfg.tolerance):
        logging.info("Mixing station active. Starting mix.")
        if not detect_only:
            pyautogui.mouseDown()
            time.sleep(0.5)  # Wait for the mixing to start

            # Inner loop: keep mixing as long as the "in-progress" color is visible
            while pyautogui.pixelMatchesColor(*cfg.action_coords[0], cfg.action_colors[0], tolerance=cfg.tolerance):
                logging.debug("Mixing...")
                time.sleep(2)  # Check every 2 seconds

            pyautogui.mouseUp()
            logging.info("Mixing complete!")
        else:
            # In detect_only mode, we just log that we would be mixing.
            logging.info("Mixing station detected.")
            time.sleep(2) # Add a delay to avoid spamming the log

def handle_rolling_station(detect_only: bool):
    """
    If the rolling station is detected, this function takes control
    and continuously checks for the action pixels until the station disappears.
    """
    cfg = CONFIG["roll"]
    while pyautogui.pixelMatchesColor(*cfg.station_coords, cfg.station_color, tolerance=cfg.tolerance):
        logging.debug("Rolling station active...")
        is_roll_ready = any(
            pyautogui.pixelMatchesColor(*coords, color, tolerance=cfg.tolerance)
            for coords, color in zip(cfg.action_coords, cfg.action_colors)
        )
        if is_roll_ready:
            logging.debug("Roll block in range.")
            if not detect_only:
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                logging.info("Roll!")
        time.sleep(0.01)

# --- Main Application ---

def setup_logging(args):
    """Configures the logging based on command-line arguments."""
    log_level = logging.DEBUG if args.detect else logging.INFO
    logging.basicConfig(stream=sys.stderr, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main polling loop.
    The script continuously checks for each station in sequence. When a station
    is found, the corresponding 'handle' function takes over until the task is complete.
    """
    parser = argparse.ArgumentParser(description="A Python automation script for Palia.")
    parser.add_argument("-d", "--detect", help="Detect only, do not perform actions", action="store_true")
    args = parser.parse_args()

    setup_logging(args)
    pyautogui.FAILSAFE = True
    
    logging.info("Starting automation script. Press Ctrl+C to exit.")
    logging.info(f"Detect only mode: {'ON' if args.detect else 'OFF'}")

    try:
        while True:
            # These functions are blocking, as intended. The script will
            # only proceed to check for the next station after the current
            # one is no longer visible.
            handle_chopping_station(args.detect)
            handle_mixing_station(args.detect)
            handle_rolling_station(args.detect)

            # Add a small delay in the main polling loop to prevent high CPU
            # usage when no stations are active.
            time.sleep(0.1)

    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()