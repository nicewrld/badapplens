import cv2
import os
from PIL import Image
from dnslib.server import DNSServer, BaseResolver, DNSLogger
from dnslib import RR, TXT, QTYPE

# Step 1: Extract Frames
def extract_frames(video_path, output_dir, frame_rate=10):
    os.makedirs(output_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    interval = int(fps // frame_rate) if frame_rate > 0 else 1
    frame_id = 0

    while success:
        if vidcap.get(cv2.CAP_PROP_POS_FRAMES) % interval == 0:
            frame_path = os.path.join(output_dir, f"frame_{frame_id}.png")
            cv2.imwrite(frame_path, image)
            frame_id += 1
        success, image = vidcap.read()
    vidcap.release()

# Updated Function: Convert Image to ASCII Art Lines
def image_to_ascii_lines(image_path, cols=80):
    chars = "@%#*+=-:. "
    num_chars = len(chars)
    
    # Open the image and convert to grayscale
    img = Image.open(image_path).convert('L')
    
    # Determine new dimensions to maintain aspect ratio
    W, H = img.size
    aspect_ratio = H / W
    rows = int(cols * aspect_ratio * 0.5)  # 0.5 accounts for character height-width ratio in terminals
    
    # Resize the image to the new dimensions
    img = img.resize((cols, rows))
    
    ascii_lines = []
    for y in range(rows):
        ascii_line = ""
        for x in range(cols):
            pixel = img.getpixel((x, y))
            ascii_char = chars[pixel * (num_chars - 1) // 255]
            ascii_line += ascii_char
        ascii_lines.append(ascii_line)
    return ascii_lines

# Load Frames Data
def load_frames_data(frames_dir):
    frames_data = {}
    for filename in sorted(os.listdir(frames_dir)):
        if filename.endswith('.png'):
            frame_path = os.path.join(frames_dir, filename)
            frame_id = int(filename.replace('frame_', '').replace('.png', ''))
            ascii_lines = image_to_ascii_lines(frame_path)
            # Ensure each line is within the TXT record limit
            txt_records = []
            for line in ascii_lines:
                if len(line) <= 255:
                    txt_records.append(line)
                else:
                    # Split long lines if necessary
                    for i in range(0, len(line), 255):
                        txt_records.append(line[i:i+255])
            frames_data[frame_id] = txt_records
    return frames_data

# DNS Resolver Class
class FrameResolver(BaseResolver):
    def __init__(self, frames_data):
        self.frames_data = frames_data

    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        frame_id = str(qname).split('.')[0]
        frame_number = frame_id.replace('frame_', '')
        if frame_number.isdigit():
            frame_number = int(frame_number)
            if frame_number in self.frames_data:
                txt_records = self.frames_data[frame_number]
                for txt in txt_records:
                    reply.add_answer(RR(rname=qname, rtype=QTYPE.TXT, rclass=1, ttl=0, rdata=TXT(txt)))
            else:
                reply.add_answer(RR(rname=qname, rtype=QTYPE.TXT, rclass=1, ttl=0, rdata=TXT("Frame not found.")))
        else:
            reply.add_answer(RR(rname=qname, rtype=QTYPE.TXT, rclass=1, ttl=0, rdata=TXT("Invalid frame ID.")))
        return reply

if __name__ == "__main__":
    video_path = 'media/bad_apple.mp4'
    output_dir = 'frames'

    # Step 1: Extract frames (uncomment if frames are not extracted yet)
    # extract_frames(video_path, output_dir)

    # Load frames data
    frames_data = load_frames_data(output_dir)

    # Start DNS server
    resolver = FrameResolver(frames_data)
    logger = DNSLogger(prefix=False)
    server = DNSServer(resolver, port=9353, address="0.0.0.0", logger=logger)
    print("Starting DNS server on port 9353...")
    server.start_thread()

    # Keep the main thread alive
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass