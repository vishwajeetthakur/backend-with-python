import cv2
import redis
import numpy as np
import sounddevice as sd
import wave

client = redis.Redis()
client_channel = client.pubsub()
client_channel.subscribe("user_1")

frame_width = 640
frame_height = 360
writer = cv2.VideoWriter('received_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (frame_width, frame_height))
audio_data = []

# def audio_callback(outdata, frames, time, status):
#     if len(audio_data) >= frames:
#         outdata[:] = np.vstack(audio_data[:frames])
#         del audio_data[:frames]
#     else:
#         outdata[:len(audio_data)] = np.vstack(audio_data)
#         outdata[len(audio_data):] = 0
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    
    if len(indata) > 0:
        audio_data.append(indata.copy())

try:
    stream = sd.OutputStream(callback=audio_callback, channels=1)
    stream.start()

    audio_writer = wave.open('received_audio.wav', 'wb')
    audio_writer.setnchannels(1)
    audio_writer.setsampwidth(2)
    audio_writer.setframerate(44100)

    for item in client_channel.listen():
        if item["type"] != "message":
            continue

        data_str = item["data"].decode('utf-8')
        data_dict = eval(data_str)

        frame_data = np.frombuffer(data_dict["frame"], dtype="uint8").reshape(frame_height, frame_width, 1)
        audio_sample_data_list = data_dict["audio"]

        for audio_sample_data in audio_sample_data_list:
            audio_data.append(np.frombuffer(audio_sample_data, dtype="int16"))
            audio_writer.writeframes(audio_sample_data)

        writer.write(frame_data)
        cv2.imshow("Frame", frame_data)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    client_channel.unsubscribe()
    writer.release()
    cv2.destroyAllWindows()
    audio_writer.close()
    stream.stop()
    print("*********** Subscriber ENDED Gracefully ****************")
