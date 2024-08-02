import speech_recognition as sr

class AudioToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def convert_wav_to_text(self, file_path="output.wav"):
        with sr.AudioFile(file_path) as source:
            audio = self.recognizer.record(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language="en-US")
            return text
        
        except sr.UnknownValueError:
            return "Speech could not be understood"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Usage example:
converter = AudioToText()
text = converter.convert_wav_to_text()
print(text)