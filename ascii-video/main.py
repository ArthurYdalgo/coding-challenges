import cv2
import numpy as np

def openVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap

def getFrames(cap):
    frames = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frames.append(frame)
        else:
            break
    return frames


def frameToAscii(frame):
    squares = getSquares(frame)

    final_frame = []

    for col in squares:
        horizontal_images = []
        for square in col:
            new_image = np.zeros((5, 5, 3), np.uint8)

            average_color_row = np.average(square, axis=0)
            average_color = np.average(average_color_row, axis=0)
            
            texted_image = cv2.putText(new_image, "o", (0, 5), cv2.FONT_HERSHEY_PLAIN, 0.5, average_color ,1)
            horizontal_images.append(texted_image)
         
        row = cv2.hconcat(horizontal_images)
        final_frame.append(row)
        
    ascii_frame = cv2.vconcat(final_frame)

    return ascii_frame

def getSquares(frame):
    im = frame

    squares = []

    imgheight = im.shape[0]
    imgwidth = im.shape[1]

    M = 5
    N = 5
    for y in range(0, imgheight, M):
        row = []
        for x in range(0, imgwidth, N):
            
            square = im[y:y+M, x:x+N]
            
            row.append(square)
        squares.append(row)

    return squares

def framesToVideo(frames):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frames[0].shape[1], frames[0].shape[0]))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()

def main():
    cap = openVideo("video.mp4")
    frames = getFrames(cap)
    ascii_frames = []
    for i in range(len(frames)):
        ascii_frame = frameToAscii(frames[i])
        ascii_frames.append(ascii_frame)
    
    framesToVideo(ascii_frames)

main()

