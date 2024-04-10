import streamlit as st
from modules.similarity import SimilarityScorer
import decimal
from streamlit_mic_recorder import speech_to_text

st.title("Text Similarity Calculator")

text1 = st.text_area("Enter first text:", "")
text2 = st.text_area("Enter second text:", "")

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

def callback():
    if st.session_state.my_stt_output:
        st.text_area("Copy recorded text to above area 👆", st.session_state.my_stt_output)


speech_to_text(key='my_stt', callback=callback)    