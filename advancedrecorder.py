import streamlit as st
import speech_recognition as sr
import datetime

def main():
    st.title("Continuous Speech-to-Text")

    r = sr.Recognizer()

    if 'listening' not in st.session_state:
        st.session_state.listening = False

    if st.button("Start/Stop Listening"):
        st.session_state.listening = not st.session_state.listening

    container = st.container()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        while st.session_state.listening:
            try:
                audio = r.listen(source, phrase_time_limit=3)  # Reduced listening interval
                text = r.recognize_google(audio)
                with container:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.text_area(f"Recognized text ({current_time}):", value=text, height=100, key=st.session_state.get('counter', 0))
                    st.session_state['counter'] = st.session_state.get('counter', 0) + 1
            except sr.UnknownValueError:
                with container:
                    st.write("Could not understand audio")
            except sr.RequestError as e:
                with container:
                    st.write(f"Error: {e}")

if __name__ == "__main__":
    main()
