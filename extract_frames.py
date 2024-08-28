import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--video", required = True)
parser.add_argument("--out", required = True)
parser.add_argument("--fps", default = 30)
args = parser.parse_args()

os.makedirs(args.out, exist_ok = True)

vidcap = cv2.VideoCapture(args.video)

frame_id = 0

def getFrame(sec):
    global frame_id
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec * 1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(args.out, f"{str(frame_id).zfill(7)}.png"), image)     # save frame as PNG file
        frame_id += 1
    return hasFrames
sec = 0
fps = args.fps
caprate = 1 / fps
success = getFrame(sec)
while success:
    sec = sec + caprate
    sec = round(sec, 3)
    success = getFrame(sec)
