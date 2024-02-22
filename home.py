import streamlit as st
from datetime import datetime, timedelta
from util import plot, data, _plot
import base64
from streamlit_echarts import st_echarts
# 改style要在改font之前
# plt.style.use('seaborn')

sideb = st.sidebar

st.set_page_config(page_title='首頁',
                   page_icon="🐺")

side_bg = './img/S__75292772-removebg-preview.png'
option = st.sidebar.selectbox(
   "Select color",
   ('Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2','Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b','tab20c'),
   index=4)
check1 = sideb.button("reload data")
if check1:
    data.reload()

plot.update_colormap(name = option)

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

start_time = st.date_input(
    'start time',
    datetime.strptime(data.df.date.min(), '%Y/%m/%d').date()-timedelta(days = 1)
).strftime("%Y/%m/%d/")

end_time = st.date_input(
    'end time',
    datetime.strptime(data.df.date.max(), '%Y/%m/%d').date()
).strftime("%Y/%m/%d/")


# st.pyplot(plot.home_one(start_time, end_time))

# st.pyplot(plot.home_two(start_time, end_time))

# st.pyplot(plot.home_three(start_time, end_time))



st_echarts(options=_plot.home_1(start_time, end_time), height=800)
st_echarts(options=_plot.home_2(start_time, end_time), height=400)
st_echarts(options=_plot.home_3(start_time, end_time))
st_echarts(options=_plot.home_4(start_time, end_time))
st_echarts(options=_plot.home_5(start_time, end_time), height=400)
