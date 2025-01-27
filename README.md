# ![Hoplite Icon](assets/icon.png) Hoplite

An attempt at making a basic AI for the Hoplite Android game.

## Preamble

[Hoplite](http://www.magmafortress.com/p/hoplite.html) is a popular turn-based strategy Android game developed by [Magma Fortress](http://www.magmafortress.com/), originally created in [2013](http://www.roguetemple.com/7drl/2013/). Try it ([there is a free and a premium version](https://play.google.com/store/apps/details?id=com.magmafortress.hoplite&hl=fr)), you will love it!

This modules provides an interface for automatically playing the game on an Android simulator or even live on a device. Screen is captured and analyzed for the program to get a logical representation of the game. Then, like most chess engines, possible moves are explored and evaluated by pondering some relevant features. The best one is picked, and played.

[Here is a demonstration of it working on a emulator](https://www.youtube.com/watch?v=8ofj6W05LZg&list=PL2ecHtEW1_x9NVOkVryLtduEI3Y_NNnuB&index=4&t=0s).

This is a first draft, meaning many components are missing or poorly implemented. See the [roadmap](#roadmap) for details.

![Hoplite Android Icon](https://2.bp.blogspot.com/-QH3Ceormja0/UrKqFsfIMkI/AAAAAAAAAIM/XicUf6o0n4I/s200/helmetICON.png)

## Getting Started

### Prerequisites

You will need Python 3 and Android Studio for [`adb`](https://developer.android.com/studio/command-line/adb).

`adb` allows for remotely controlling the Android device (either a real phone plugged into the computer via USB with ['USB debugging' enabled](https://developer.android.com/studio/command-line/adb#Enabling), or an emulated phone created with [AVD](https://developer.android.com/studio/run/managing-avds)).

### Installation

1. Clone the repository

        git clone https://github.com/ychalier/hoplite.git

2. Install the dependencies

        cd hoplite/
        pip install -r requirements.txt

### Usage

1. Either start the emulated phone in AVD or plug in your phone, and open the Hoplite app.

2. Find out adb device serial using:

        adb devices

3. Start the script with:

        python main.py -serial <adb_device_serial> play 

Use `python main.py --help` for more details.

## Roadmap

There is a lot to do, so feel free to [contribute](#contributing)!

- [x] ~~Implement basic interaction with the game~~
- [x] ~~Implement a basic game engine~~
- [x] ~~Implement a basic decision making system~~
- [x] ~~Make the MonkeyRunner interface more reliable~~
- [x] ~~Replace the MonkeyRunner with python-pure-adb
- [ ] Enhance the game re-implementation:
    - [x] ~~Develop a game explorer to build a database of state sequences for further analysis~~
    - [ ] Complete and implement the [game rules](RULES.md)
        - [x] ~~Prayers~~
        - [x] ~~Energy restoration~~
        - [x] ~~Knockback, collisions~~
        - [x] ~~Killing spree (Surge and Regeneration prayers)~~
        - [ ] Demons movements
            - [ ] Footman movement
            - [ ] Archer and Wizard movement
            - [ ] Demolitionist movement and throw
        - [ ] Cooldowns
            - [ ] Bash cooldown
            - [ ] Wizard cooldown
            - [ ] Demolitionist cooldown
        - [ ] Demons status
            - [ ] Stunned
            - [ ] Sleeping
            - [ ] Shield
    - [x] ~~Allow for menus recognition (title screen and altars) and answering~~
    - [x] ~~Implement memory for `GameState` to allow prayers handling~~
- [x] ~~Fasten `Observer` by using fine-tuned template recognition model~~
- [ ] Enhance the AI part:
    - [ ] Fine-tune player's incentives between killing all enemies, go to the next level, and pray at the altar
    - [ ] Implement a proper training of the game state evaluation
    - [ ] Implement a proper exploration of variations starting from a position, like chess engines
- [ ] Explore support for device with resolution different from 1080*1920
- [ ] *Many more things that I am not thinking of right now...*

## Contributing

Open pull requests or issues if you have any proposition to make. Check the [roadmap](#roadmap) for ideas (there are many), and the [documentation](https://ychalier.github.io/hoplite/) for how to implement them. I put some screenshots [here](https://drive.google.com/file/d/1qxlnwcgf0HpPYMsUqjAjjSAjxX1xGKji/view?usp=sharing) (2MB) helping development, and the [templates](https://drive.google.com/file/d/12jOOsBgHntUWIagNk2fzicEvEETnyvvW/view?usp=sharing) (1MB) used for the classifiers.

If you implement some features, please make sure your code is clean enough (for this matter I use the [Pylint](https://www.pylint.org/) linter) and documented enough (add docstrings with short descriptions, types of arguments and returned values). I use [pdoc](https://pdoc3.github.io/pdoc/) to generate the documentation.
