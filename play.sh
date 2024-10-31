#!/bin/bash

SERVER="localhost"
PORT="9353"
DOMAIN_SUFFIX=".example.com"
FRAMES_DIR="frames"

# Get the total number of frames
TOTAL_FRAMES=$(ls -1 $FRAMES_DIR | grep 'frame_.*\.png' | wc -l)

# Function to query a frame using dig and display the ASCII art
query_frame() {
    FRAME_NUMBER=$1
    DOMAIN="frame_$FRAME_NUMBER$DOMAIN_SUFFIX"
    DIG_OUTPUT=$(dig @$SERVER -p $PORT $DOMAIN)

    # Process the dig output to extract the TXT records
    # Remove the leading and trailing quotes and backslashes
    ASCII_ART=$(echo "$DIG_OUTPUT" | sed -e 's/^.*TXT[[:space:]]*//' -e 's/"//g' -e 's/\\;$/;/g')

    # Replace semicolons with newlines (if necessary)
    # ASCII_ART=$(echo "$ASCII_ART" | tr ';' '\n')

    # Clear the screen
    clear

    # Display the ASCII art
    echo -e "$ASCII_ART"
}

# Main loop to iterate through frames
FRAME_NUMBER=0
while true; do
    query_frame $FRAME_NUMBER
    FRAME_NUMBER=$(( (FRAME_NUMBER + 1) % TOTAL_FRAMES ))
done