#!/bin/bash

SERVER="127.0.0.1"
PORT="9353"
DOMAIN_SUFFIX=".dnsroleplay.club"
FRAMES_DIR="frames"

# Get the total number of frames
TOTAL_FRAMES=$(ls -1 $FRAMES_DIR | grep 'frame_.*\.png' | wc -l)

# Function to query a frame using dig and display the ASCII art
query_frame() {
    FRAME_NUMBER=$1
    DOMAIN="frame_$FRAME_NUMBER$DOMAIN_SUFFIX"

    # Process the dig output to extract the TXT records
    # Remove the leading and trailing quotes and backslashes

    # Replace semicolons with newlines (if necessary)
    # ASCII_ART=$(echo "$ASCII_ART" | tr ';' '\n')

    # Clear the screen
    clear
    dig @$SERVER -p $PORT $DOMAIN
    sleep 0.085

}

# Main loop to iterate through frames
FRAME_NUMBER=0
while true; do
    query_frame $FRAME_NUMBER
    FRAME_NUMBER=$(( (FRAME_NUMBER + 1) % TOTAL_FRAMES ))
done