import argparse
import os
from datetime import datetime

import pvporcupine
from pvrecorder import PvRecorder
from utills import root_path


accessKey = '2LbjKeL8zIt6SprzJfIbTgfZhsEJxjxUl0/29HZ0poNYhbDzb/u39Q=='
# keyWordPath = ['../Data/macOS-wakeWord/يا-عياش_ar_mac_v3_0_0.ppn']
keyWordPath = [root_path +'Data/rasbparryPi-wakeWord/يا-عياش .ppn']

# keyWordPath = ['/Users/ahmaddarabee/ayyash/Data/rasbparryPi-wakeWord/يا-عياش .ppn']
modelPath = root_path +'Data/macOS-wakeWord/porcupine_params_ar.pv'
# modelPath = 'Data/macOS-wakeWord/porcupine_params_ar.pv'

device_index = 0


class WakeWord:
    def __init__(self):
        for i, device in enumerate(PvRecorder.get_available_devices()):
            if device == "USB Camera-B4.09.24.1, USB Audio" or device == "Sony Playstation Eye Analog Surround 4.0" or device == "MacBook Pro Microphone":
                global device_index
                device_index = i
                print('Device %d: %s' % (i, device) + "been selected")
        parser = argparse.ArgumentParser()

        parser.add_argument(

            '--access_key',
            default=accessKey,
            help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')

        parser.add_argument(
            '--keywords',
            nargs='+',
            help='List of default keywords for detection. Available keywords: %s' % ', '.join(
                '%s' % w for w in sorted(pvporcupine.KEYWORDS)),
            choices=sorted(pvporcupine.KEYWORDS),
            metavar='')

        parser.add_argument(
            '--keyword_paths',
            default=keyWordPath,
            nargs='+',
            help="Absolute paths to keyword model files. If not set it will be populated from `--keywords` argument")

        parser.add_argument(
            '--library_path',
            help='Absolute path to dynamic library. Default: using the library provided by `pvporcupine`')

        parser.add_argument(
            '--model_path',
            default=modelPath,
            help='Absolute path to the file containing model parameters. '
                 'Default: using the library provided by `pvporcupine`')

        parser.add_argument(
            '--sensitivities',
            nargs='+',
            help="Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A higher "
                 "sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 "
                 "will be used.",
            type=float,
            default=None)

        parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=device_index)

        parser.add_argument('--output_path', help='Absolute path to recorded audio for debugging.', default=None)

        parser.add_argument('--show_audio_devices', action='store_true')

        args = parser.parse_args()
        for i, device in enumerate(PvRecorder.get_available_devices()):
            print('Device %d: %s' % (i, device))
        if args.show_audio_devices:
            for i, device in enumerate(PvRecorder.get_available_devices()):
                print('Device %d: %s' % (i, device))
            return

        if args.keyword_paths is None:
            if args.keywords is None:
                raise ValueError("Either `--keywords` or `--keyword_paths` must be set.")

            keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in args.keywords]
        else:
            keyword_paths = args.keyword_paths

        if args.sensitivities is None:
            args.sensitivities = [0.5] * len(keyword_paths)

        if len(keyword_paths) != len(args.sensitivities):
            raise ValueError('Number of keywords does not match the number of sensitivities.')

        try:
            self.porcupine = pvporcupine.create(
                access_key=args.access_key,
                library_path=args.library_path,
                model_path=args.model_path,
                keyword_paths=keyword_paths,
                sensitivities=args.sensitivities)
        except pvporcupine.PorcupineInvalidArgumentError as e:
            print("One or more arguments provided to Porcupine is invalid: ", args)
            print(e)
            raise e
        except pvporcupine.PorcupineActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvporcupine.PorcupineActivationLimitError as e:
            print("AccessKey '%s' has reached it's temporary device limit" % args.access_key)
            raise e
        except pvporcupine.PorcupineActivationRefusedError as e:
            print("AccessKey '%s' refused" % args.access_key)
            raise e
        except pvporcupine.PorcupineActivationThrottledError as e:
            print("AccessKey '%s' has been throttled" % args.access_key)
            raise e
        except pvporcupine.PorcupineError as e:
            print("Failed to initialize Porcupine")
            raise e

        self.keywords = list()
        for x in keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
            if len(keyword_phrase_part) > 6:
                self.keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                self.keywords.append(keyword_phrase_part[0])

        print('Porcupine version: %s' % self.porcupine.version)

        # self.wav_file = None
        # if args.output_path is not None:
        #     self.wav_file = wave.open(args.output_path, "w")
        #     self.wav_file.setnchannels(1)
        #     self.wav_file.setsampwidth(2)
        #     self.wav_file.setframerate(16000)

        print('Listening ... (press Ctrl+C to exit)')
        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=device_index)

        self.recorder.start()

    def listing(self):
        try:

            # print(recorder.PvRecorderStatuses.value)
            while True:
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)

                # if self.wav_file is not None:
                #     self.wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                if result >= 0:
                    print('[%s] Detected %s' % (str(datetime.now()), self.keywords[result]))
                    # recorder.stop()
                    return True

        except Exception as error:
            print("An exception occurred:", error)
        finally:
            self.recorder.delete()
            self.porcupine.delete()
        return False


if __name__ == '__main__':
    detect = WakeWord()
    detect.listing()
