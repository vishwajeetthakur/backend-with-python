import cv2
import redis 

video = cv2.VideoCapture(0)

height = int(video.get(4) / 2 )
width = int(video.get(3) / 2 )

# print(height, width)
server = redis.Redis()
video_streaming = True

try:
    while video.isOpened():
        ret, frame = video.read()

        if ret and video_streaming:
            
            frame = cv2.resize(frame, (width, height))
            # Publish the frame (message packet) to a channel named user_1
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame', gray)
            server.publish("user_1", frame.tobytes())


        key = cv2.waitKey(1)

        if key == ord('s'):
            print("video is paused ...")
            video_streaming = False
        
        if key == ord('o'):
            print("video is opened ...")
            video_streaming = True

        if key == ord('q'):
            break
            

finally:
    video.release()
    cv2.destroyAllWindows()
    print("*********** Pubslisher ENDED Gracefully ****************")
