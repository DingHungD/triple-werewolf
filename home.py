import streamlit as st
from datetime import datetime
from util import plot, data, _plot, constant
import base64
from streamlit_echarts import st_echarts
# 改style要在改font之前
# plt.style.use('seaborn')

constant.init_session_state()


st.set_page_config(page_title='首頁',
                   page_icon="🐺")

side_bg = './img/S__75292772-removebg-preview.png'


## sidebar
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
   ('pyplot', 'echart'),
   index=st.session_state.CHARTMODEINDEX)
st.session_state.CHARTMODEINDEX = {'pyplot':0, 'echart':1}[st.session_state.CHARTMODE]



PLOTCOLOR_lst = ('Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2','Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b','tab20c')


st.session_state.PLOTCOLOR = st.sidebar.selectbox(
   "Select chart mode",
   PLOTCOLOR_lst,
   index=st.session_state.PLOTCOLORINDEX)
st.session_state.PLOTCOLORINDEX = {v:i for i, v in enumerate(PLOTCOLOR_lst)}[st.session_state.PLOTCOLOR]

sideb = st.sidebar
check1 = sideb.button("reload data")
if check1:
    data.reload()

# plot.update_colormap(name = constant.PLOTCOLOR)




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
    div[data-testid="stMarkdownContainer"] div{
    color: gray;
    }
    div[data-testid="stSlider"] div{
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
# body
session_number = st.slider('玩家場數過濾', 0,
                           data.get_final_df(st.session_state.STARTTIME,
                                             st.session_state.ENDTIME).session_number.max()-1,0)


plot.update_colormap(name = st.session_state.PLOTCOLOR)
if st.session_state.CHARTMODE=='pyplot':
    st.pyplot(plot.home_one(st.session_state.STARTTIME, st.session_state.ENDTIME, session_number))
    st.pyplot(plot.home_two(st.session_state.STARTTIME, st.session_state.ENDTIME))
    st.pyplot(plot.home_three(st.session_state.STARTTIME, st.session_state.ENDTIME))

elif st.session_state.CHARTMODE=='echart':

    st_echarts(options=_plot.home_1(st.session_state.STARTTIME, st.session_state.ENDTIME, session_number), height=800)
    st_echarts(options=_plot.home_2(st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)
    st_echarts(options=_plot.home_3(st.session_state.STARTTIME, st.session_state.ENDTIME))
    st_echarts(options=_plot.home_4(st.session_state.STARTTIME, st.session_state.ENDTIME))
    st_echarts(options=_plot.home_5(st.session_state.STARTTIME, st.session_state.ENDTIME), height=400)



