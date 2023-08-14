# Open CV to display incoming frame
import cv2
# Redis to subscribe
import redis
# Numpy to convert message packet to 2D array of pixels.
import numpy as np
 
client = redis.Redis()
# Creating a Pub Sub client to subscribe to some channels.
client_channel = client.pubsub()


# Let's subscribe to other user's channel.
client_channel.subscribe("user_1")

frame_width = 640
frame_height = 360
writer = cv2.VideoWriter('captured_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                        25, (frame_width, frame_height))

try:         
    # Listening to messages in the channel
    for item in client_channel.listen():    
        if item["type"] != "message":
            continue

        # For every message received in the channel, converting the bytes to a 2D array.
        frame = np.frombuffer(item["data"], dtype="uint8").reshape(360, 640, 3)

        writer.write(frame)
        # Displaying this frame back to the User client.
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
finally:
    client_channel.unsubscribe()
    writer.release()
    cv2.destroyAllWindows()
    print("*********** Suscriber ENDED Gracefully ****************")


