from enum import Enum

# setting default settings
speak_engine = {
    "rate": 180,
    "voice": "Maged",
    "volume": 1.0,  # range [0.0 , 1.0]
}
speak_recognition = {
    "lang": "ar",
    "energy_threshold": 400,  # 300 is minimum
    "dynamic_energy_threshold": False,
    "timeout": 3,
    "phrase_time_limit": 10,
}


def set_config(config):
    try:
        speak_engine["rate"] = config["speak_engine"]["rate"]
        speak_engine["voice"] = config["speak_engine"]["voice"]
        speak_engine["volume"] = config["speak_engine"]["volume"]

        speak_recognition["lang"] = config["speak_recognition"]["lang"]
        speak_recognition["energy_threshold"] = config["speak_recognition"]["energy_threshold"]
        speak_recognition["dynamic_energy_threshold"] = config["speak_recognition"]["dynamic_energy_threshold"]
    except Exception as e:
        print("An error occurred:", e)
# preprocessing_queue = [
#     preprocessing.scale_and_center,
#     preprocessing.dot_reduction,
#     preprocessing.connect_lines,
# ]
