from util import data
from datetime import datetime, timedelta
import streamlit as st
def init_session_state():
    if 'CHARTMODE' not in st.session_state:
        st.session_state.CHARTMODE = 'pyplot'
    if 'CHARTMODEINDEX' not in st.session_state:
        st.session_state.CHARTMODEINDEX = 0
    if 'PLOTCOLOR' not in st.session_state:
        st.session_state.PLOTCOLOR = "Dark2"
    if 'PLOTCOLORINDEX' not in st.session_state:
        st.session_state.PLOTCOLORINDEX = 4
    if 'STARTTIME' not in st.session_state:
        st.session_state.STARTTIME = (datetime.strptime(data.df.date.min(), '%Y/%m/%d').date()-timedelta(days = 1)).strftime("%Y/%m/%d")
    if 'ENDTIME' not in st.session_state:
        st.session_state.ENDTIME = data.df.date.max()
    if 'THETIME' not in st.session_state:
        st.session_state.THETIME = data.df.date.max()
    if 'THESESSION' not in st.session_state:
        st.session_state.THESESSION = 1
    if 'THEROUND' not in st.session_state:
        st.session_state.THEROUND = 1
    if 'PUBLIC' not in st.session_state:
        st.session_state.PUBLIC = False

CHARTMODE = 'pyplot'
CHARTMODEINDEX = 0
PLOTCOLOR = "Dark2"
PLOTCOLORINDEX = 4

# STARTTIME = data.df.date.min()
STARTTIME = (datetime.strptime(data.df.date.min(), '%Y/%m/%d').date()-timedelta(days = 1)).strftime("%Y/%m/%d")
ENDTIME = data.df.date.max()



