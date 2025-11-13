import streamlit as st
import pandas as pd
import duckdb
from streamlit_ace import st_ace

# App Header
st.markdown('# SQL on the Fly')
st.markdown('An app to analyze your CSV files with SQL')

# Initialize session state
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = None
if 'tablename' not in st.session_state:
    st.session_state['tablename'] = 'my_table'
if 'duckdb_conn' not in st.session_state:
    st.session_state['duckdb_conn'] = duckdb.connect()

# Sidebar for File Upload
with st.sidebar:
    st.markdown('### Upload your CSV')
    delimiter = st.radio('Choose delimiter:', [";", ",", "\t"])
    file = st.file_uploader('Add file here')
    tablename = st.text_input('Name your table', st.session_state['tablename'])
    add = st.button('Add CSV')

# Handle CSV Upload
if add and file:
    try:
        df = pd.read_csv(file, delimiter=delimiter)
        st.session_state['dataframe'] = df
        st.session_state['tablename'] = tablename
        st.session_state['file_uploaded'] = True

        # Register the dataframe as a DuckDB table
        con = st.session_state['duckdb_conn']
        con.register(tablename, df)

        st.success(f"Uploaded and registered table: {tablename}")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# Display Dataframe + Query UI
if st.session_state['file_uploaded']:
    df = st.session_state['dataframe']
    tablename = st.session_state['tablename']
    con = st.session_state['duckdb_conn']

    THEMES = [
        "ambiance","chaos","chrome","clouds","clouds_midnight","cobalt",
        "crimson_editor","dawn","dracula","dreamweaver","eclipse","github",
        "gob","gruvbox","idle_fingers","iplastic","katzenmilch","kr_theme",
        "kuroir","merbivore","merbivore_soft","mono_industrial","monokai",
        "nord_dark","pastel_on_dark","solarized_dark","solarized_light",
        "sqlserver","terminal","textmate","tomorrow","tomorrow_night",
        "tomorrow_night_blue","tomorrow_night_bright","tomorrow_night_eighties",
        "twilight","vibrant_ink","xcode",
    ]

    KEYBINDINGS = ["emacs", "sublime", "vim", "vscode"]

    # ACE Editor for SQL Query
    query = st_ace(
        value=f"SELECT * FROM {tablename} LIMIT 5",
        language="SQL",
        theme=st.sidebar.selectbox("Theme", options=THEMES, index=26),
        keybinding=st.sidebar.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),
        font_size=st.sidebar.slider("Font size", 5, 24, 14),
        tab_size=st.sidebar.slider("Tab size", 1, 8, 4),
        wrap=st.sidebar.checkbox("Wrap lines", value=False),
        show_gutter=True,
        show_print_margin=True,
        auto_update=False,
        readonly=False,
        key="ace-editor",
    )

    # Run Query Button
    if st.button('Run Query'):
        if query:
            try:
                # Run SQL using DuckDB
                result = con.execute(query).df()

                st.markdown('### Query Results:')
                st.dataframe(result)

            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.warning('Please enter a SQL query to execute.')
