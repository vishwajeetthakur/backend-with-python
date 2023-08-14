import cv2
import redis
import numpy as np
import sounddevice as sd
import wave

video = cv2.VideoCapture(0)

height = int(video.get(4) / 2)
width = int(video.get(3) / 2)

server = redis.Redis()
video_streaming = True

audio_data = []
audio_sample_rate = 44100  # Example sample rate, adjust according to your needs

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_data.append(indata.copy())


frame_width = 640
frame_height = 360
writer = cv2.VideoWriter('received_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (frame_width, frame_height))
audio_writer = wave.open('received_audio.wav', 'wb')
audio_writer.setnchannels(1)
audio_writer.setsampwidth(2)
audio_writer.setframerate(44100)


try:
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=audio_sample_rate)

    stream.start()

    while video.isOpened():
        ret, frame = video.read()

        if ret and video_streaming:
            frame = cv2.resize(frame, (width, height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Convert audio_data to a list of bytes
            audio_bytes = [sample.tobytes() for sample in audio_data]

            # Create a dictionary with frame and audio data as bytes
            data_dict = {"frame": gray.tobytes(), "audio": audio_bytes}
            print("AUDIO : ", audio_bytes)
            writer.write(gray.tobytes())

            # Serialize the dictionary as a string and publish it
            server.publish("user_1", str(data_dict))

            cv2.imshow('frame', gray)

        key = cv2.waitKey(1)

        if key == ord('s'):
            print("Video is paused ...")
            video_streaming = False

        if key == ord('o'):
            print("Video is opened ...")
            video_streaming = True

        if key == ord('q'):
            break

finally:
    video.release()
    cv2.destroyAllWindows()
    print("*********** Publisher ENDED Gracefully ****************")
