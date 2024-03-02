import cv2

def Start():
    cap = cv2.VideoCapture("video/video.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    i=0
    j=1
    while True:
        k,frame=cap.read()
        if not k:
            break
        if i==int(fps):
            i=0
            cv2.imwrite(f"images/{j}.png",frame)
            j+=1
        i+=1
    cap.release()
