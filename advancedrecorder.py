import streamlit as st
import speech_recognition as sr
import datetime
import pyaudio
import wave
import os
import numpy as np

def record_system_audio(duration, filename):
    CHUNK = 4096  # Increased chunk size for better quality
    FORMAT = pyaudio.paInt16  # Changed to float32 for higher precision
    CHANNELS = 2
    RATE = 48000  # Increased sample rate for better quality
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
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert to numpy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

    # Apply gain (increase volume)
    gain = 95.0  # Adjust this value to increase or decrease volume
    audio_data = audio_data * gain

    # Clip to prevent distortion
    audio_data = np.clip(audio_data, -32768, 32767).astype(np.int16)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    print("* done recording")
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
            record_system_audio(10, "output.wav")  # 3 seconds of system audio

            # # Process microphone input
            # audio = r.listen(source, phrase_time_limit=3)
            # mic_text = r.recognize_google(audio)

            # Process system audio
            with sr.AudioFile("output.wav") as source:
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
