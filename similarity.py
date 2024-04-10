import streamlit as st
from modules.similarity import SimilarityScorer
import decimal
import speech_recognition as sr

def listen_and_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""

st.title("Text Similarity Calculator")

text1 = st.text_area("Enter first text:", "")
text2 = st.text_area("Enter second text:", "")

def on_button_press():
    with sr.Microphone() as source: 
        r = sr.Recognizer()
        audio = r.listen(source)
        text = r.recognize_google(audio)
        st.session_state.text2 += text

listen_btn = st.button("Listen", on_click=on_button_press) 

scorer = SimilarityScorer() 
    
if st.button("Score"):
    score = scorer.score(text1, text2)
    # Convert to Decimal to avoid floating point precision issues
    score_formatted = decimal.Decimal(str(score))

    # Multiply by 100 to get a percentage 
    score_formatted *= 100

    # Format to two decimal places  
    percentage = '{0:.2f}%'.format(score_formatted)
    st.write("Similarity score:", percentage)