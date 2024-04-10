import streamlit as st
import speech_recognition as sr

def main():
    st.title("Voice Input POC")

    # Initialize the recognizer
    r = sr.Recognizer()

    # Add a button to start listening
    if st.button("Listen"):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            st.write("Listening... Speak now!")
            try:
                # Listen for audio input
                audio = r.listen(source, timeout=5)
                st.write("Processing...")

                # Recognize the speech
                text = r.recognize_google(audio)
                st.write(f"Recognized text: {text}")

            except sr.WaitTimeoutError:
                st.write("Timeout: No speech detected.")
            except sr.UnknownValueError:
                st.write("Error: Unable to recognize speech.")
            except sr.RequestError as e:
                st.write(f"Error: {e}")

if __name__ == "__main__":
    main()
