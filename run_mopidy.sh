#!/bin/bash
sudo killall mopidy
amixer sset 'Master' 50%
mopidy