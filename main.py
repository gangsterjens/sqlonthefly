import streamlit as st
import pandas as pd
import pandasql as ps

st.markdown('# Welcome to SQL on the fly')
st.markdown('## An app to analyze your csv, as you go')

with st.sidebar:
  st.markdown(' ### Upload your csv')
  delimiter = st.radio('Choose:', [";","'"])
  if not delimiter:
    delimiter = ';'
  file = st.file_uploader('Add file here')
  tablename = st.text_input('name of table')
  add = st.button('Add csv')


if add:
  df = pd.read_csv(file, delimiter=delimiter)
  query = st.text_area('Query')
  mapping = {tablename, df}
  result = ps.sqldf(query, mapping)
  if query:
    st.dataframe(result)

