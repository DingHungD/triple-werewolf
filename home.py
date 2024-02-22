import streamlit as st
from datetime import datetime, timedelta
from util import plot, data, _plot, constant
import base64
from streamlit_echarts import st_echarts
# 改style要在改font之前
# plt.style.use('seaborn')

sideb = st.sidebar

st.set_page_config(page_title='首頁',
                   page_icon="🐺")

side_bg = './img/S__75292772-removebg-preview.png'

STARTTIME = st.date_input(
    'start time',
    datetime.strptime(constant.STARTTIME, '%Y/%m/%d').date()-timedelta(days = 1)
).strftime("%Y/%m/%d")

ENDTIME = st.date_input(
    'end time',
    datetime.strptime(constant.ENDTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")



constant.CHARTMODE = st.sidebar.selectbox(
   "Select chart mode",
   ('pyplot', 'echart'),
   index=constant.CHARTMODEINDEX)

constant.CHARTMODEINDEX = {'pyplot':0, 'echart':1}[constant.CHARTMODE]
constant.PLOTCOLOR = st.sidebar.selectbox(
   "Select color",
   ('Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2','Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b','tab20c'),
   index=4)

check1 = sideb.button("reload data")
if check1:
    data.reload()

plot.update_colormap(name = constant.PLOTCOLOR)

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
    div[data-testid="stMarkdownContainer"] div{
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




if constant.CHARTMODE=='pyplot':
    st.pyplot(plot.home_one(STARTTIME, ENDTIME))
    st.pyplot(plot.home_two(STARTTIME, ENDTIME))
    st.pyplot(plot.home_three(STARTTIME, ENDTIME))

elif constant.CHARTMODE=='echart':

    st_echarts(options=_plot.home_1(STARTTIME, ENDTIME), height=800)
    st_echarts(options=_plot.home_2(STARTTIME, ENDTIME), height=400)
    st_echarts(options=_plot.home_3(STARTTIME, ENDTIME))
    st_echarts(options=_plot.home_4(STARTTIME, ENDTIME))
    st_echarts(options=_plot.home_5(STARTTIME, ENDTIME), height=400)
