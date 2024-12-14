#! /bin/bash
grim -g "$(slurp)" ~/Pictures/$(date +"%Y-%m-%d_%H-%M-%S").png && notify-send 'screenshot saved'
