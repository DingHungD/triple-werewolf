import streamlit as st

from datetime import datetime
from util import _plot, data, plot, constant, plotly
import base64
from streamlit_echarts import st_echarts

side_bg = './img/S__75292772-removebg-preview.png'
st.set_page_config(page_title='動作',
                   page_icon="🐺")

constant.init_session_state()

st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background-image: url(data:image/png;base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        #   linear-gradient(rgba(81, 79, 89, 1), rgba(255, 255, 255, 1));
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
# st.markdown(
#   """
#     <style>
#     div[data-testid="stSelectbox"] div{
#     color: gray;
#     }

#     label[data-testid="stWidgetLabel"] label{
#     color: gray;
#     }
#     div[data-testid="stMarkdownContainer"] div{
#     color: gray;
#     }
#     div[data-testid="stSlider"] div{
#     color: gray;
#     }
# #     div[data-testid="stDateInput"] div {
# #     color: gray;
# #     }
# #     div[data-testid="stDateInput"] input{
# #     color: gray;
# #     }
# #     div[role="presentation"] div{
# #     color: gray;
# #     }
# #     div[data-baseweb="calendar"] button {
# #         color:gray
# #         };
#         </style>
# """,
#     unsafe_allow_html=True,
# )

# sidebar
st.session_state.STARTTIME = st.sidebar.date_input(
    'start time',
    datetime.strptime(st.session_state.STARTTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")

st.session_state.ENDTIME = st.sidebar.date_input(
    'end time',
    datetime.strptime(st.session_state.ENDTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")

st.session_state.CHARTMODE = st.sidebar.selectbox(
   "Select chart mode",
   ('pyplot', 'echart', 'matplotlib'),
   index=st.session_state.CHARTMODEINDEX)
st.session_state.CHARTMODEINDEX = {'pyplot':0, 'echart':1, 'matplotlib':2}[st.session_state.CHARTMODE]

# body
action = st.selectbox(
        'action',
        data.process_df.action.unique()
    )
if st.session_state.CHARTMODE!='pyplot':
    session_number = st.slider('玩家場數過濾', 0,
                            data.get_final_df(st.session_state.STARTTIME,
                                                st.session_state.ENDTIME).session_number.max(),0)


if st.session_state.CHARTMODE=='matplotlib':
    st.pyplot(plot.action_one(action, st.session_state.STARTTIME, st.session_state.ENDTIME, session_number))

elif st.session_state.CHARTMODE=='echart':
    st_echarts(options=_plot.action_1(action, st.session_state.STARTTIME, st.session_state.ENDTIME, session_number), height=800)


elif st.session_state.CHARTMODE=='pyplot':
    st.plotly_chart(plotly.action_1(action, st.session_state.STARTTIME, st.session_state.ENDTIME))

