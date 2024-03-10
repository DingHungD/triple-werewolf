import pandas as pd
from datetime import datetime, timedelta
from util import data


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from matplotlib.gridspec import GridSpec



fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
mpl.rc('font', family='Taipei Sans TC Beta')

def update_colormap(name = 'Dark2'):
    global COLORMAP
    COLORMAP = mpl.colormaps[name].colors
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=COLORMAP)

update_colormap(name = 'Dark2')

def home_one(start_time, end_time, session_number = 0):

    tmp_df = data.get_final_df(start_time, end_time)
    tmp_df = tmp_df[tmp_df.session_number=>session_number]
    tmp_df = tmp_df.sort_values('win', ascending=True)
    include_sid = data.session_df[(data.session_df.date>=start_time)&(data.session_df.date<=end_time)].sid.values
    fig, ax = plt.subplots(1, 4)
    fig.patch.set_alpha(0.3)

    ax_i = 0
    tmp_df.plot(x='name', y='win', kind='barh', stacked=True, ax=ax[ax_i])
    ax[ax_i].title.set_text('勝率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(1,1.2)).remove()
    ax[ax_i].patch.set_alpha(0)

    ax_i = 1
    tmp_df.plot(x='name', y='mvp', kind='barh', stacked=True, ax=ax[ax_i])
    ax[ax_i].title.set_text('mvp率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(1,1.2)).remove()
    ax[ax_i].axes.yaxis.set_visible(False)
    ax[ax_i].grid(color='gray', linestyle='--', linewidth=1)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 2
    tmp_df.plot(x='name', y='session_number', kind='barh', stacked=True, ax=ax[ax_i])
    ax[ax_i].title.set_text('參與場次')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(1,1.2)).remove()
    ax[ax_i].axes.yaxis.set_visible(False)
    ax[ax_i].grid(color='gray', linestyle='--', linewidth=1)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 3
    tmp_df.plot(x='name', y=['god','villager','wolf'], kind='barh', stacked=True, ax=ax[ax_i])
    ax[ax_i].text(1.1,0,'統計時間 \n開始：%s \n結束：%s\n\n共%s場'%(start_time, end_time, len(include_sid)))
    ax[ax_i].title.set_text('角色比')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].axes.yaxis.set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(1,1))
    ax[ax_i].patch.set_alpha(0)

    return fig

def home_two(start_time, end_time):
    fig = plt.figure(layout="constrained")
    fig.patch.set_alpha(0.3)
    gs = GridSpec(2, 3, figure=fig)
    ax = [
        fig.add_subplot(gs[0:2, 0:2]),
        fig.add_subplot(gs[0, -1]),
        fig.add_subplot(gs[1,-1])
        ]

    ax_i = 0
    tmp_df = data.get_board_proportion_df(start_time, end_time)
    explode = [0.05 for i in range(tmp_df.shape[0])]

    tmp_df.plot(y='sid', kind='pie', autopct='%1.1f%%', startangle=90, pctdistance=0.85,
                explode = explode, wedgeprops=dict(width=0.4, edgecolor='w'), ax=ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('統計時間 \n開始：%s \n結束：%s\n共%s場\n\n板子統計'%(start_time, end_time, tmp_df.sid.sum()))
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].patch.set_alpha(0)

    ax_i = 1
    tmp_df = data.get_win_sum_df(start_time, end_time)

    tmp_df.plot(y=list(tmp_df.columns), kind='bar', stacked=True, ax=ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('日期&勝負統計')
    plt.setp(ax[ax_i].xaxis.get_majorticklabels(), rotation=0)
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2))
    ax[ax_i].patch.set_alpha(0)

    ax_i = 2
    tmp_df = data.get_win_proportion_df(start_time, end_time)
    explode = [0.05 for i in range(tmp_df.shape[0])]

    tmp_df.plot(y='sid', kind='pie', autopct='%1.1f%%', startangle=90, pctdistance=0.7,
                explode = explode, wedgeprops=dict(width=0.7, edgecolor='w'), ax=ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('總勝負比')
    plt.setp(ax[ax_i].xaxis.get_majorticklabels(), rotation=0)
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].patch.set_alpha(0)

    return fig

def home_three(start_time, end_time):

    tmp_df = data.get_seat_df(start_time, end_time)

    fig = plt.figure(layout="constrained")
    fig.patch.set_alpha(0.3)
    gs = GridSpec(1, 1, figure=fig)
    ax = [fig.add_subplot(gs[0, 0])]

    ax_i = 0
    ax[ax_i] = (tmp_df/tmp_df.sum()).T.plot(y=['god', 'villager', 'wolf'], kind='barh', color = [COLORMAP[0], COLORMAP[1], COLORMAP[2]], stacked=True, ax=ax[ax_i])
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].patch.set_alpha(0)
    plt.title('座位風水圖')
    plt.xlabel('比例')
    plt.ylabel('座位')
    plt.legend(bbox_to_anchor=(1.2,1))
    ax[ax_i].text(1.05,0,'統計時間 \n開始：%s \n結束：%s\n\n共%s場'%(start_time, end_time, tmp_df.sum().max()))

    return fig

def action_one(action, start_time, end_time, session_number=0):

    tmp_df = data.get_action_df(action, start_time, end_time)
    tmp_df = tmp_df[tmp_df.session_number>session_number]
    include_sid = data.session_df[(data.session_df.date>=start_time)&(data.session_df.date<=end_time)].sid.values
    fig, ax = plt.subplots(1, 2)
    fig.patch.set_alpha(0.3)
    ax_i = 0
    tmp_df.plot(x='name', y=['ratio'], kind='barh', stacked=True, ax=ax[ax_i])

    ax[ax_i].title.set_text('被%s王'%action)
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].set_xlabel('被%s率'%action)
    ax[ax_i].grid(color='gray', linestyle='--',axis='x', linewidth=0.5)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 1
    tmp_df.plot(x='name', y=['session_number', 'number'], kind='barh', stacked=False, ax=ax[ax_i])
    ax[ax_i].title.set_text('參與場次&被%s次數'%action)
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(1,1))
    ax[ax_i].axes.yaxis.set_visible(False)
    ax[ax_i].grid(color='gray', linestyle='--', linewidth=0.5)
    ax[ax_i].set_xlabel('數量')
    ax[ax_i].text(tmp_df.session_number.max()+1,0,'統計時間 \n開始：%s \n結束：%s\n\n共%s場'%(start_time, end_time, len(include_sid)))
    ax[ax_i].patch.set_alpha(0)

    return fig

def personal_one(name, start_time, end_time):
    df = data.df
    _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)].copy()

    fig = plt.figure(layout="constrained")
    fig.patch.set_alpha(0.3)
    gs = GridSpec(1, 2, figure=fig)
    ax = [
        fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        ]

    ax_i = 0
    tmp_df = _tmp_df.value_counts('role')
    explode = [0.05 for i in range(tmp_df.shape[0])]
    tmp_df.plot(kind='pie', autopct='%1.1f%%', startangle=90, pctdistance=0.7,
        explode = explode,wedgeprops=dict(width=0.3, edgecolor='w'), ax=ax[ax_i])
    ax[ax_i].title.set_text('角色統計')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 1
    tmp_df = _tmp_df.loc[:,'win'].value_counts()
    if False in tmp_df.index:
        tmp_df = tmp_df.rename(index={False:'輸'})
    if True in tmp_df.index:
        tmp_df = tmp_df.rename(index={True:'贏'})
    explode = [0.05 for i in range(tmp_df.shape[0])]
    tmp_df.plot(kind='pie', autopct='%1.1f%%', startangle=90, pctdistance=0.7,
        explode = explode, wedgeprops=dict(width=0.7, edgecolor='w'), ax=ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('勝率')
    plt.setp(ax[ax_i].xaxis.get_majorticklabels(), rotation=0)
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].patch.set_alpha(0)

    return fig

def personal_two(name, start_time, end_time):
    fig = plt.figure(layout="constrained")
    fig.patch.set_alpha(0.3)
    gs = GridSpec(2, 3, figure=fig)
    ax = [
        fig.add_subplot(gs[0:2, 0:1]),
        fig.add_subplot(gs[0:1, 1:2]),
        fig.add_subplot(gs[1:2, 1:2]),
        fig.add_subplot(gs[0:1, 2:3]),
        fig.add_subplot(gs[1:2, 2:3])
         ]

    ax_i = 0
    tmp_df = data.get_personal_role_win_df(name, start_time, end_time)
    tmp_df.T.plot(y='win', kind='barh', stacked=True, ax = ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('職業勝率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].axis(xmin=0,xmax=1.1)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 1
    final_process_df = data.get_final_process_df(start_time, end_time)
    tmp_df = final_process_df[(final_process_df.name == name)&(final_process_df.god)]
    tmp_df = tmp_df[tmp_df.action != '救']
    if tmp_df.shape[0]>0:

        tmp_lst = []
        for role, item in tmp_df.groupby('role'):
            tmp_lst.append({'role':role, 'numer':item[item.object_wolf].shape[0], 'total_round':item.shape[0]})
        tmp_df = pd.DataFrame(tmp_lst)
        tmp_df['ratio'] = tmp_df.numer/tmp_df.total_round
        tmp_df.plot(x='role',y='ratio', kind='barh', stacked=True, ax = ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('殺狼率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].axis(xmin=0,xmax=1.1)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 2
    tmp_df = final_process_df[(final_process_df.name == name)&(final_process_df.wolf)]
    if tmp_df.shape[0]>0:
        tmp_lst = []
        for role, item in tmp_df.groupby('role'):
            tmp_lst.append({'role':role, 'numer':item[item.object_god].shape[0], 'total_round':item.shape[0]})
        tmp_df = pd.DataFrame(tmp_lst)
        tmp_df['ratio'] = tmp_df.numer/tmp_df.total_round
        tmp_df.plot(x='role',y='ratio', kind='barh', stacked=True, ax = ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('殺神率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    ax[ax_i].axis(xmin=0,xmax=1.1)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 3
    tmp_df = data.get_camp_sum_df(name, start_time, end_time)
    tmp_df.plot(kind='bar', stacked=True, ax = ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('神狼民次數')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    plt.setp(ax[ax_i].xaxis.get_majorticklabels(), rotation=0)
    ax[ax_i].text(3,tmp_df.max(),'\n%s'%(name), fontsize=20)
    ax[ax_i].patch.set_alpha(0)

    ax_i = 4
    _tmp_df = data.df[(data.df.name == name)&(data.df.date>=start_time)&(data.df.date<=end_time)].copy()
    tmp_df = data.get_camp_win_df(name, start_time, end_time)
    tmp_df.T.plot(y='win', kind='bar', stacked=True, ax = ax[ax_i])
    ax[ax_i].set_ylabel("")
    ax[ax_i].title.set_text('陣營勝率')
    ax[ax_i].spines['top'].set_visible(False)
    ax[ax_i].spines['right'].set_visible(False)
    ax[ax_i].legend(bbox_to_anchor=(-0.1,1.2)).remove()
    plt.setp(ax[ax_i].xaxis.get_majorticklabels(), rotation=0)
    ax[ax_i].text(3.05,0,'統計時間 \n開始：%s \n結束：%s\n\n共%s場'%(start_time, end_time, _tmp_df.shape[0]))
    ax[ax_i].axis(ymin=0,ymax=1.1)
    ax[ax_i].patch.set_alpha(0)

    return fig
