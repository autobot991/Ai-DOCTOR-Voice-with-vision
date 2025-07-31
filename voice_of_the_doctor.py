# Optional: load environment variables if needed
# from dotenv import load_dotenv
# load_dotenv()

import os
import platform
import subprocess
import time
from gtts import gTTS
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def text_to_speech_with_gtts(input_text, output_filepath):
    os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
    language = "en"

    # Generate TTS audio
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Windows":
            wav_path = output_filepath.replace(".mp3", ".wav")
            convert_mp3_to_wav(output_filepath, wav_path)
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
            time.sleep(1)
            if os.path.exists(wav_path):
                os.remove(wav_path)
        elif os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # You can also use 'mpg123'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred during playback: {e}")

if __name__ == "__main__":
    input_text = "Hi, this is AI speaking with Ahmad!"
    output_path = "gtts_output.mp3"
    text_to_speech_with_gtts(input_text, output_path)
