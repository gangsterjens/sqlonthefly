import streamlit as st
import pandas as pd
import pandasql as ps

# App Header
st.markdown('# SQL on the Fly')
st.markdown('An app to analyze your CSV files with SQL')

# Initialize session state for handling app state
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None
if 'tablename' not in st.session_state:
    st.session_state['tablename'] = 'my_table'

# Sidebar for File Upload
with st.sidebar:
    st.markdown('### Upload your CSV')
    delimiter = st.radio('Choose delimiter:', [";", ",", "\t"])
    file = st.file_uploader('Add file here')
    tablename = st.text_input('Name your table', st.session_state['tablename'])
    add = st.button('Add CSV')

# Handle CSV Upload and Table Naming
if add and file:
    try:
        df = pd.read_csv(file, delimiter=delimiter)
        st.session_state['dataframe'] = df
        st.session_state['tablename'] = tablename
        st.session_state['file_uploaded'] = True
        st.success(f"Uploaded and named table as: {tablename}")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Display DataFrame and Query Section
if st.session_state['file_uploaded']:
    df = st.session_state['dataframe']
    tablename = st.session_state['tablename']


    # Query Input
    query = st.text_area('Write your SQL Query here', 'SELECT * FROM my_table LIMIT 5')

    # Execute SQL Query
    if st.button('Run Query'):
        if query:
            try:
                # Execute SQL Query
                mapping = {tablename: df}
                result = ps.sqldf(query, mapping)
                st.markdown('### Query Results:')
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error in query execution: {e}")
        else:
            st.warning('Please enter a SQL query to execute.')
