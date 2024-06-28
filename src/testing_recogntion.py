 

import signal
import sys
import time
from threading import Thread
from pvleopard import create, LeopardActivationLimitError
from pvrecorder import PvRecorder
from tabulate import tabulate
import utills
ACCESS_KEY = "2LbjKeL8zIt6SprzJfIbTgfZhsEJxjxUl0/29HZ0poNYhbDzb/u39Q=="
path_to_model=utills.root_path+"Data/rasbparry_speech_to_text_model/eng_speech_to_text.pv"
AUDIO_DEVICE_INDEX = -1
VERBOSE = False

class Recorder(Thread):
    def __init__(self, audio_device_index):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = False
        self._audio_device_index = audio_device_index

    def is_recording(self):
        return self._is_recording

    def run(self):
        self._is_recording = True

        recorder = PvRecorder(frame_length=160, device_index=self._audio_device_index)
        recorder.start()

        while not self._stop:
            self._pcm.extend(recorder.read())
        recorder.stop()

        self._is_recording = False

    def stop(self):
        self._stop = True
        while self._is_recording:
            pass

        return self._pcm

class AudioProcessor:
    def __init__(self):
        self.access_key = ACCESS_KEY
        self.model_path = path_to_model
        self.audio_device_index = AUDIO_DEVICE_INDEX
        self.verbose = VERBOSE
        self.leopard = create(
            access_key=self.access_key,
            model_path=self.model_path,
            enable_automatic_punctuation=True,
            enable_diarization=True
        )
        self.recorder = None
        signal.signal(signal.SIGINT, self.on_exit)

    def on_exit(self, signum, frame):
        self.leopard.delete()

        if self.recorder is not None:
            self.recorder.stop()

        print()
        sys.exit(0)

    def show_audio_devices(self):
        for index, name in enumerate(PvRecorder.get_available_devices()):
            print(f'Device #{index}: {name}')

    # def start(self):
    #     self.show_audio_devices()
    #     print('>>> Press `CTRL+C` to exit: ')

    #     while True:
    #         if self.recorder is not None:
    #             input('>>> Recording ... Press `ENTER` to stop: ')
    #             try:
    #                 transcript, words = self.leopard.process(self.recorder.stop())
    #                 print(transcript)
    #                 if self.verbose:
    #                     print(tabulate(
    #                         words,
    #                         headers=['word', 'start_sec', 'end_sec', 'confidence', 'speaker_tag'],
    #                         floatfmt='.2f'))
    #             except LeopardActivationLimitError:
    #                 print('AccessKey has reached its processing limit.')
    #             print()
    #             self.recorder = None
    #         else:
    #             input('>>> Press `ENTER` to start: ')
    #             self.recorder = Recorder(self.audio_device_index)
    #             self.recorder.start()
    #             time.sleep(.25)

    def record(self,period=5):
        print ("recording...")
        self.recorder = Recorder(self.audio_device_index)
        self.recorder.start()
        time.sleep(period)

        print ("processing...")

        if self.recorder is not None:
                try:
                    transcript, words = self.leopard.process(self.recorder.stop())
                    print(transcript)
                    # if self.verbose:
                    #     print(tabulate(
                    #         words,
                    #         headers=['word', 'start_sec', 'end_sec', 'confidence', 'speaker_tag'],
                    #         floatfmt='.2f'))
                except LeopardActivationLimitError:
                    print('AccessKey has reached its processing limit.')
                self.recorder = None







if __name__ == '__main__':
    processor = AudioProcessor()
    # processor.start()
    processor.record()


# import signal
# import sys
# import time
# from argparse import ArgumentParser
# from threading import Thread
# from pvleopard import create, LeopardActivationLimitError
# from pvrecorder import PvRecorder
# from tabulate import tabulate
# import utills

# ACCESS_KEY = "2LbjKeL8zIt6SprzJfIbTgfZhsEJxjxUl0/29HZ0poNYhbDzb/u39Q=="
# path_to_model=utills.root_path+"Data/rasbparry_speech_to_text_model/eng_speech_to_text.pv"

# class Recorder(Thread):
#     def __init__(self, audio_device_index=-1):
#         super().__init__()
#         self._pcm = list()
#         self._is_recording = False
#         self._stop = False
#         self._audio_device_index = audio_device_index

#     def is_recording(self):
#         return self._is_recording

#     def run(self):
#         self._is_recording = True

#         recorder = PvRecorder(frame_length=160, device_index=self._audio_device_index)
#         recorder.start()

#         while not self._stop:
#             self._pcm.extend(recorder.read())
#         recorder.stop()

#         self._is_recording = False

#     def stop(self):
#         self._stop = True
#         while self._is_recording:
#             pass

#         return self._pcm

# class Record():
#     def __init__(self):
#         self.leopard =   create(
#         access_key=ACCESS_KEY,
#         model_path=path_to_model,
#         library_path=None,
#         enable_automatic_punctuation=not True,
#         enable_diarization=not True)

#         self.recorder = Recorder(-1)
#         signal.signal(signal.SIGINT, self.on_exit)


#     def on_exit(self,_, __):
#         self.leopard.delete()

#         if  self.recorder is not None:
#              self.recorder.stop()

#         print()
#         sys.exit(0)
    
#     def recording(self,time=5):
#         self.recorder = Recorder(-1)
#         self.recorder.start()
#         time.sleep(.25)


#         while True:
#             # Set an alarm to go off after 5 seconds
#             # signal.alarm(time)

#             if self.recorder is not None:
#                 time.sleep(4)
#                 # input('>>> Recording ... Press `ENTER` to stop: ')
#                 try:
#                     transcript, words = self.leopard.process(recorder.stop())
#                     print(transcript)
#                     if False:
#                         print(tabulate(
#                             words,
#                             headers=['word', 'start_sec', 'end_sec', 'confidence', 'speaker_tag'],
#                             floatfmt='.2f'))
#                 except LeopardActivationLimitError:
#                     print('AccessKey has reached its processing limit.')
#                 print()
#                 recorder = None
#             else:
#                 input('>>> Press `ENTER` to start: ')
#                 self.recorder = Recorder(-1)
#                 self.recorder.start()
#                 time.sleep(.25)

# if __name__ == "__main__":
#     r =Record()
#     r.recording()


# def main():
#     leopard = create(
#         access_key=ACCESS_KEY,
#         model_path=path_to_model,
#         library_path=None,
#         enable_automatic_punctuation=not True,
#         enable_diarization=not True)
    
#     recorder = None
    
#     def on_exit(self,_, __):
#         leopard.delete()

#         if recorder is not None:
#             recorder.stop()

#         print()
#         sys.exit(0)


#     signal.signal(signal.SIGINT, on_exit)

#     print('>>> Press `CTRL+C` to exit: ')

#     while True:
#         if recorder is not None:
#             input('>>> Recording ... Press `ENTER` to stop: ')
#             try:
#                 transcript, words = leopard.process(recorder.stop())
#                 print(transcript)
#                 if False:
#                     print(tabulate(
#                         words,
#                         headers=['word', 'start_sec', 'end_sec', 'confidence', 'speaker_tag'],
#                         floatfmt='.2f'))
#             except LeopardActivationLimitError:
#                 print('AccessKey has reached its processing limit.')
#             print()
#             recorder = None
#         else:
#             input('>>> Press `ENTER` to start: ')
#             recorder = Recorder(-1)
#             recorder.start()
#             time.sleep(.25)






# # import time
# # import numpy as np
# # import sounddevice as sd

# # import speech_recognition as sr
# # from scipy.io import wavfile

# # recognizer = sr.Recognizer()


# # def ndarray_to_audio_data(ndarray, sample_rate):
# #     # Convert the ndarray to bytes
# #     audio_bytes = ndarray.tobytes()

# #     # Create an AudioData object from the bytes and sample rate
# #     audio_data = sr.AudioData(audio_bytes, sample_rate, 2)  # Assuming 2 channels for stereo audio

# #     return audio_data


# # def record_audio(duration, fs, channels):
# #     print("Recording...")
# #     audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
# #     sd.wait()  # Wait until recording is finished
# #     print("Recording finished.")
# #     return ndarray_to_audio_data(audio_data, fs)


# # if __name__ == "__main__":
# #     duration = 3  # Duration of recording in seconds
# #     fs = 44100  # Sampling frequency
# #     channels = 4  # Number of audio channels (1 for mono, 2 for stereo)

# #     audio_data = record_audio(duration, fs, channels)

# #     text = recognizer.recognize_sphinx(audio_data).lower()  # Recognize the speech
# #     print("Recognized text:", text)

# #     print("Audio saved to output.wav")

# # # import time
# # #
# # # import sounddevice as sd
# # #
# # # import speech_recognition as sr
# # # from scipy.io import wavfile
# # #
# # # recognizer = sr.Recognizer()
# # #
# # #
# # # def ndarray_to_audio_data(ndarray, sample_rate):
# # #     # Convert the ndarray to bytes
# # #     audio_bytes = ndarray.tobytes()
# # #
# # #     # Create an AudioData object from the bytes and sample rate
# # #     audio_data = sr.AudioData(audio_bytes, sample_rate, 2)  # Assuming 2 channels for stereo audio
# # #
# # #     return audio_data
# # #
# # #
# # # def record_audio(duration, fs, channels):
# # #     print("Recording...")
# # #     audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='float64')
# # #     sd.wait()  # Wait until recording is finished
# # #     print("Recording finished.")
# # #     return ndarray_to_audio_data(audio_data, fs)
# # #
# # #
# # # if __name__ == "__main__":
# # #     duration = 3  # Duration of recording in seconds
# # #     fs = 44100  # Sampling frequency
# # #     channels = 1  # Number of audio channels (1 for mono, 2 for stereo)
# # #
# # #     audio_data = record_audio(duration, fs, channels)
# # #
# # #     time.sleep(1)
# # #
# # #     file_path = "output.wav"
# # #     # Save the recorded audio to a WAV file
# # #     with open(file_path, "w") as file:
# # #         # Write data to the file
# # #         file.write("This is a test.")
# # #
# # #     wavfile.write(file_path, fs, audio_data)
# # #
# # #     text = recognizer.recognize_sphinx(audio_data).lower()  # Recognize the speech
# # #     print("Recognized text:", text)
# # #
# # #     print("Audio saved to output.wav")
