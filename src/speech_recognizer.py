 

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
                    return transcript
                    # if self.verbose:
                    #     print(tabulate(
                    #         words,
                    #         headers=['word', 'start_sec', 'end_sec', 'confidence', 'speaker_tag'],
                    #         floatfmt='.2f'))
                except LeopardActivationLimitError:
                    print('AccessKey has reached its processing limit.')
                self.recorder = None

recognize=AudioProcessor()

if __name__ == '__main__':
    processor = AudioProcessor()
    processor.record()

 