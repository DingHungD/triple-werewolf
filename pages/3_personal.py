import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from util import _plot, data, plot, constant, plotly
import base64
from streamlit_echarts import st_echarts

st.set_page_config(page_title='首頁',
                   page_icon="🐺")
side_bg = './img/S__75292772-removebg-preview.png'

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
#     div[data-testid="stDataFrameResizable"] div{
#     solid: gray;
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

name = st.selectbox(
        'name',
        data.df.name.unique()
    )

st.session_state.STARTTIME = st.sidebar.date_input(
    'start time',
    datetime.strptime(st.session_state.STARTTIME, '%Y/%m/%d').date()

    ).strftime("%Y/%m/%d")

st.session_state.ENDTIME = st.sidebar.date_input(
    'end time',
    datetime.strptime(st.session_state.ENDTIME, '%Y/%m/%d').date()
).strftime("%Y/%m/%d")


# st.session_state.CHARTMODE = st.sidebar.selectbox(
#    "Select chart mode",
#    ('pyplot', 'echart', 'matplotlib'),
#    index=st.session_state.CHARTMODEINDEX)
st.session_state.CHARTMODEINDEX = {'pyplot':0, 'echart':1, 'matplotlib':2}[st.session_state.CHARTMODE]



if st.session_state.CHARTMODE=='matplotlib':
    st.pyplot(plot.personal_one(name, st.session_state.STARTTIME, st.session_state.ENDTIME))

    st.pyplot(plot.personal_two(name, st.session_state.STARTTIME, st.session_state.ENDTIME))
elif st.session_state.CHARTMODE=='echart':

    st_echarts(options=_plot.personal_1(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_2(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_3(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_4(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_5(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_6(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.personal_7(name, st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
elif st.session_state.CHARTMODE=='pyplot':
    st.plotly_chart(plotly.personal_1(name, st.session_state.STARTTIME, st.session_state.ENDTIME))

    # st.table(plotly.personal_2(name))
    st.title('角色操作動作')
    st.dataframe(data.get_player_df(name), hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.THETIME = st.selectbox(
            '選擇時間',
            data.session_df.date.unique()
        )
    with col2:
        st.session_state.THESESSION = int(st.selectbox(
            '選擇場次',
            data.session_df[data.session_df.date == st.session_state.THETIME].session.unique()
        ))
    session_info, tmp_df = data.get_allpalyer_df(
        st.session_state.THETIME,
        st.session_state.THESESSION)
    st.caption("板子：%s 獲勝方：%s"%(session_info['board'], session_info['result']), unsafe_allow_html=False)
    st.dataframe(tmp_df, hide_index=True)



