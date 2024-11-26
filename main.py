import streamlit as st
import pandas as pd
import pandasql as ps

# App Header
st.markdown('# Welcome to SQL on the Fly')
st.markdown('## An app to analyze your CSV files with SQL')

# Sidebar for File Upload
with st.sidebar:
    st.markdown('### Upload your CSV')
    delimiter = st.radio('Choose delimiter:', [";", ",", "\t"])
    file = st.file_uploader('Add file here')
    tablename = st.text_input('Name your table', 'my_table')
    add = st.button('Add CSV')

# Placeholder for displaying query results
if add:
    if file is not None:
        try:
            # Read CSV
            df = pd.read_csv(file, delimiter=delimiter)
            st.write(f"Data from **{tablename}**:")
            st.dataframe(df)

            # Query Input
            query = st.text_area('Write your SQL Query here', 'SELECT * FROM my_table LIMIT 5')

            # Mapping DataFrame to SQL
            mapping = {tablename: df}

            if query:
                try:
                    # Execute SQL Query
                    result = ps.sqldf(query, mapping)
                    st.markdown('### Query Results:')
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Error in query execution: {e}")
            else:
                st.warning('Please enter a SQL query to execute.')
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    else:
        st.warning('Please upload a CSV file.')
