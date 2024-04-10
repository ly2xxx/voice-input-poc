import streamlit as st
from streamlit_mic_recorder import speech_to_text
def callback():
    if st.session_state.my_stt_output:
        st.text_area("Enter second text:", st.session_state.my_stt_output)


speech_to_text(key='my_stt', callback=callback)