import streamlit as st

from datetime import datetime, timedelta
from util import data, plot, _plot, constant
import base64
from streamlit_echarts import st_echarts

side_bg = './img/S__75292772-removebg-preview.png'
st.set_page_config(page_title='動作',
                   page_icon="🐺")

st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background-image: url(data:image/png;base64,{base64.b64encode(open(side_bg, "rb").read()).decode()}),linear-gradient(rgba(81, 79, 89, 1), rgba(255, 255, 255, 1));
          background-size: contain;
          #background-position: center;
          background-repeat: no-repeat;
          background-position-y: 100%;
          border:none;
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
st.markdown(
  """
    <style>
    div[data-testid="stSelectbox"] div{
    color: gray;
    }

    label[data-testid="stWidgetLabel"] label{
    color: gray;
    }

#     div[data-testid="stDateInput"] div {
#     color: gray;
#     }
#     div[data-testid="stDateInput"] input{
#     color: gray;
#     }
#     div[role="presentation"] div{
#     color: gray;
#     }
#     div[data-baseweb="calendar"] button {
#         color:gray
#         };
        </style>
""",
    unsafe_allow_html=True,
)

action = st.selectbox(
        'action',
        data.process_df.action.unique()
    )
constant.STARTTIME = st.sidebar.date_input(
    'start time',
    datetime.strptime(constant.STARTTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")

constant.ENDTIME = st.sidebar.date_input(
    'end time',
    datetime.strptime(constant.ENDTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")
constant.CHARTMODE = st.sidebar.selectbox(
   "Select chart mode",
   ('pyplot', 'echart'),
   index=constant.CHARTMODEINDEX)
constant.CHARTMODEINDEX = {'pyplot':0, 'echart':1}[constant.CHARTMODE]


if constant.CHARTMODE=='pyplot':
    st.pyplot(plot.action_one(action, constant.STARTTIME, constant.ENDTIME))

elif constant.CHARTMODE=='echart':
    st_echarts(options=_plot.action_1(action, constant.STARTTIME, constant.ENDTIME), height=800)

