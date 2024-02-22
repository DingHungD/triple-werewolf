import streamlit as st

from datetime import datetime, timedelta
from util import data, plot, _plot
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

    div[data-testid="stDateInput"] div {
    color: gray;
    }
    div[data-testid="stDateInput"] input{
    color: gray;
    }
    div[role="presentation"] div{
    color: gray;
    }
    div[data-baseweb="calendar"] button {
        color:gray
        };
        </style>
""",
    unsafe_allow_html=True,
)

action = st.selectbox(
        'action',
        data.process_df.action.unique()
    )
start_time = st.date_input(
    'start time',
    datetime.strptime(data.df.date.min(), '%Y/%m/%d').date()-timedelta(days = 1)
).strftime("%Y/%m/%d/")
end_time = st.date_input(
    'end time',
    datetime.strptime(data.df.date.max(), '%Y/%m/%d').date()
).strftime("%Y/%m/%d/")

# st.pyplot(plot.action_one(action, start_time, end_time))


st_echarts(options=_plot.action_1(action, start_time, end_time), height=800)

