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

if "secondText" not in st.session_state:
    st.session_state["secondText"] = ""

text1 = st.text_area("Enter first text:", "")
text2 = st.text_area("Enter second text:", value=st.session_state["secondText"])

# Initialize the recognizer
r = sr.Recognizer()
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
            st.session_state["secondText"] = text
        except sr.WaitTimeoutError:
            st.write("Timeout: No speech detected.")
        except sr.UnknownValueError:
            st.write("Error: Unable to recognize speech.")
        except sr.RequestError as e:
            st.write(f"Error: {e}")


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