# Bananaphone

# 0. What you will need

- Bananapi raspberry M2 or Normal raspberry pi
- 4 Microswitch Buttons
- 4 CD Cases
- Some female cables
- USB Cable + Charger 
- Gluegun


# 1. Install Stuff

- Image Raspbian
    - http://wiki.banana-pi.org/Banana_Pi_BPI-M2%2B#Image_Release
    - lgoin/password: pi/bananapi 

- Mopidy Music Deamon
    - https://www.mopidy.com 
    - Install
        -  https://docs.mopidy.com/en/latest/installation/raspberrypi/
        -  https://docs.mopidy.com/en/latest/installation/debian/#debian-install
- Mopidy Python Bindings https://pypi.org/project/python-mpd2/ 
    - pip install python-mpd2
    - https://python-mpd2.readthedocs.io/en/latest/topics/commands.html

# 2. Setup Autostart

- via .desktop Mode
    - https://developer-blog.net/raspberry-pi-autostart-von-programmen/
    - cp mopidy.desktop /home/pi/.config/autostart
    - cp music.desktop /home/pi/.config/autostart

- or via .bashrc, by adding two lines at the end:
    - screen -d -m ./run_mopidy.sh
    - sudo python test.py &
    
# 3. Copy test.py to Home

- cp test.py /home/pi/test.py

# 4. Configure raspberry

- sudo raspi-config
- set force 3.5mm jack (audio will always be played via jack)
- enable ssh (so you can login and tweak things without a screen)

# 5. Copy music over to pi

- e.g. make subfolders in /home/pi/Music/player

# 6. Setup Playists

- Make playlists with vlc 
- cp to /home/pi/.local/share/mopidy/m3u 
- see sample.m3u

# 7. Adjust test.py 

- Adjust which playlists should be played when you press a button. 
- if gpio_is_pressed(23): load_playlist_and_play("klassik",True)  

# Known bugs

- test.py will crash if it cannot connect to mopidy

