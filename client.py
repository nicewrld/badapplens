import dns.resolver
import os
import time

def query_frame(frame_number, server='127.0.0.1', port=9353):
    domain = f"frame_{frame_number}.example.com"
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [server]
    resolver.port = port
    answers = resolver.resolve(domain, 'TXT')
    ascii_art = '\n'.join([txt_string.decode('utf-8') for rdata in answers for txt_string in rdata.strings])
    return ascii_art

if __name__ == '__main__':
    import sys

    # Get total number of frames
    frames_dir = 'frames'
    frame_files = [f for f in os.listdir(frames_dir) if f.endswith('.png')]
    frame_files.sort()
    total_frames = len(frame_files)

    try:
        frame_number = 0
        while True:
            ascii_art = query_frame(frame_number)
            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            time.sleep(1/10)  # Adjust the delay to control frame rate
            frame_number = (frame_number + 1) % total_frames
    except KeyboardInterrupt:
        pass