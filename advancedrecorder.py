import streamlit as st
import speech_recognition as sr
import datetime
import pyaudio
import wave
import os

def record_system_audio(duration, filename):
    sound  = True
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = duration
    WAVE_OUTPUT_FILENAME = filename
    p = pyaudio.PyAudio()
    # for i in range(p.get_device_count()):
    #     print(p.get_device_info_by_index(i))
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def main():
    st.title("Continuous Speech-to-Text")

    r = sr.Recognizer()

    if 'listening' not in st.session_state:
        st.session_state.listening = False

    if st.button("Start/Stop Listening"):
        st.session_state.listening = not st.session_state.listening

    container = st.container()

    while st.session_state.listening:
        try:
            # Record system audio
            record_system_audio(30, "output.wav")  # 3 seconds of system audio

            # # Process microphone input
            # audio = r.listen(source, phrase_time_limit=3)
            # mic_text = r.recognize_google(audio)

            # Process system audio
            with sr.AudioFile("OSR_us_000_0010_8k.wav") as source:
                system_audio = r.record(source)
            system_text = r.recognize_google(system_audio, language="en-US")

            with container:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # st.text_area(f"Recognized text (Microphone) ({current_time}):", value=mic_text, height=100, key=f"mic_{st.session_state.get('counter', 0)}")
                st.text_area(f"System text ({current_time}):", value=system_text, height=100, key=f"sys_{st.session_state.get('counter', 0)}")
                st.session_state['counter'] = st.session_state.get('counter', 0) + 1

            # Clean up the temporary file
            # os.remove("output.wav")

        except sr.UnknownValueError:
            with container:
                st.write("Could not understand audio")
        except sr.RequestError as e:
            with container:
                st.write(f"Error: {e}")

if __name__ == "__main__":
    main()
