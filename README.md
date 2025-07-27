# Project Title

Palia cooking minigame

## Description

Simple script to help with the 'chopping/stiring/rolling' during the Palia cooking mini-game.

This script detects when the moving marker enters the chop zone and clicks the mouse button.

I leave the script running while playing and have had no issues.


## Getting Started

### Dependencies

Mainly pyautogui, however had some issues getting the venv environment set up with a working combination of PyAutoGUI/numpy/pillow

* see requirements.txt

### Installing

Running on 1920x1080 resolution. 
May need to change the location of the detect pixel if your screen resolution is different.

### Executing program

```
python paliacook.py
```
Start palia / cooking / chopping.

Currently only automated chopping is available.


## Help

```
paliacook.py -h
```

## Troubleshooting

I used sharex to grab the pixel color & location. If your screen resolution is different or the color pallet changes it should be simple enough to update with new values.

Occasionally the first 'chop' misses. I'm not sure why. Every chop after seems to be fine. Even starting a new recipe works ok. It's almost like that first mouse down action when the program first runs is delayed slightly.


## Authors

D.Knapik

## Version History

* See [commit change]() or See [release history]()

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

