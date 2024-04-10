import streamlit as st
from modules.similarity import SimilarityScorer
import decimal

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