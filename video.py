import cv2

def video():

    cap = cv2.VideoCapture(1)
    cap.set(3, 3840)
    cap.set(4, 2160)

    if (cap.isOpened() == False):
        print("Error reading video file")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    result = cv2.VideoWriter('video.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             30, size)

    while (True):
        ret, frame = cap.read()

        if ret == True:
            result.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    result.release()

    cv2.destroyAllWindows()

    print("The video was successfully saved")

def main():
    video()

if __name__ == '__main__':
    main()