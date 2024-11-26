import streamlit as st

st.markdown('# Welcome to SQL on the fly')
st.markdown('## An app to analyze your csv, as you go')

with st.sidbear:
  st.markdown(' ### Upload your csv')
  file = st.file_uploader('Add file here')
  add = st.button('Add csv')


if add:
  df = pd.read_csv(file)
  print(df.head())
