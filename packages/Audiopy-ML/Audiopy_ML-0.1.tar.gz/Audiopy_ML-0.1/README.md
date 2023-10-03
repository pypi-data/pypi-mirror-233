PyAudioFX

This is a python module for automated audio pre-processing and feature extraction. 

# Fetures
Automated auto-preprocessing effects like trim, time strech and remix

Automated calculation of statistical descriptors for audio data

Automated feature extraction for both single audio file and multiple audio files in a directory

Works on all formats of audio data



# basic_audio_processor(path,effect,hop_length=512,rate=1)

example- increase the speed of the audio by 1.5x times.

basic_audio_processor(r"C:\Users\sairam\Downloads\audio preprocessing\aah shit.mp3",'time-strech',512,1.5)

# statistical_analyser(path)

example- get statistical descriptors for audio data

statistical_analyser(r"C:\Users\sairam\Downloads\audio preprocessing\aah shit.mp3")

# AutomatedExtractor_single(path)

example- perform feature extraction on a single data

AutomatedExtractor_single(r"C:\Users\sairam\Downloads\audio preprocessing\aah shit.mp3")

# Automated Extractor_multiple(path)

example- perform feature extraction on multiple data given using glob function

path=glob.glob(r"\archive (2)\set_a\*.wav")
AutomatedExtractor_multiple(path)