import pandas as pd
import streamlit as st

def reload():
    global user_df, role_df, session_df, process_df, df
    url_lst = {
        'user':st.secrets.db_links.user,
        'role':st.secrets.db_links.role,
        'session':st.secrets.db_links.session,
        'process':st.secrets.db_links.process
    }

    # df = { key:pd.read_csv(url) for key, url in url_lst.items()}
    user_df = pd.read_csv(url_lst['user'])
    role_df = pd.read_csv(url_lst['role'])
    session_df = pd.read_csv(url_lst['session'])
    process_df = pd.read_csv(url_lst['process'])



    god = ['通靈師', '預言家', '女巫', '獵人', '獵魔人', '守衛', '魔術師', '黑商', '騎士', '守墓人', '攝夢人', '覺醒預言家']
    villager = ['平民']
    wolf = ['夢魘', '小狼', '黑狼王', '狼美人', '機械狼', '狼兄','血月', '石像鬼', '狼弟', '尋香魅影', '惡靈騎士', '虎姑婆', '靈狼']

    df = pd.merge(role_df, user_df, on='uid')
    df = pd.merge(df, session_df, on='sid')

    # 神民狼 獲勝次數
    df['god'] = df.apply(lambda df:(df.role in god), axis=1)
    df['villager'] = df.apply(lambda df:(df.role in villager), axis=1)
    df['wolf'] = df.apply(lambda df:(df.role in wolf), axis=1)

    df['win'] = df.apply(lambda df:(df.wolf)==(df.result == '狼'), axis=1)
    role_df = pd.merge(role_df, user_df, on='uid')
reload()
from datetime import datetime, timedelta


def get_final_df(start_time, end_time, public):
    if public:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)&(
                session_df.public == 'public')].sid.values
    else:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)].sid.values

    tmp_df = df[df.apply(lambda df:df.sid in include_sid, axis = 1)]

    tmp_final_df = {
        'uid':[],
        'name':[],
        'god':[],
        'villager':[],
        'wolf':[],
        'win':[],
        'session_number':[],
    }

    for uid, items in tmp_df.groupby('uid'):

        tmp_final_df['uid'].append(items.uid.values[0])
        tmp_final_df['name'].append(items.name.values[0])
        tmp_final_df['win'].append(items.win.sum())
        tmp_final_df['god'].append(items.god.sum())
        tmp_final_df['villager'].append(items.villager.sum())
        tmp_final_df['wolf'].append(items.wolf.sum())
        tmp_final_df['session_number'].append(items.shape[0])

    final_df = pd.DataFrame(tmp_final_df)

    final_df.loc[:, ['god','villager','wolf','win']] = final_df.loc[:, ['god','villager','wolf','win']].div(final_df.session_number, axis=0)

    action = 'MVP'
    tmp_df = process_df[process_df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()
    tmp_df = tmp_df.drop_duplicates(['sid', 'round', 'action'])

    tmp_df = tmp_df[tmp_df.action == action].groupby('object')['sid'].count()

    final_df = pd.merge(final_df, tmp_df,
            left_on='uid', right_on='object', how='left').copy()
    final_df = final_df.rename(columns = {'sid':'mvp'})
    final_df['mvp'] = final_df.mvp/final_df.session_number
    final_df = final_df.fillna(0)


    return final_df


def get_board_proportion_df(start_time, end_time, public):
    if public:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)&(
                    session_df.public == 'public')].copy()
    else:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)].copy()

    column = 'board'
    tmp_df = _tmp_df.groupby(column).count()[['sid']]
    tmp_df = tmp_df.sort_values('sid',ascending=True)

    return tmp_df

def get_win_proportion_df(start_time, end_time, public):
    if public:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)&(
                    session_df.public == 'public')].copy()
    else:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)].copy()

    column = 'result'
    tmp_df = _tmp_df.groupby(column).count()[['sid']]

    return tmp_df

def get_win_sum_df(start_time, end_time, public):
    if public:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)&(
                    session_df.public == 'public')].copy()
    else:
        _tmp_df = session_df[(session_df.date>=start_time)&(
                    session_df.date<=end_time)].copy()

    tmp_df = {}

    for date, gb_df in _tmp_df.groupby('date'):
        tmp_df[date] = {key:value for key, value in gb_df.value_counts('result').items()}

    tmp_df = pd.DataFrame(tmp_df).fillna(0).T

    return tmp_df

def get_seat_df(start_time, end_time, public):
    if public:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)&(
                session_df.public == 'public')].sid.values
    else:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)].sid.values
    _tmp_df = df[df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()
    tmp_df = {}
    for n, item in _tmp_df.groupby('set number'):
        tmp_df[n] = item.loc[:, ['god',	'villager',	'wolf']].sum()

    tmp_df = pd.DataFrame(tmp_df)

    return tmp_df

def get_action_df(action, start_time, end_time, public):
    if public:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)&(
                session_df.public == 'public')].sid.values
    else:
        include_sid = session_df[(session_df.date>=start_time)&(
                session_df.date<=end_time)].sid.values
    include_sid = list(set(include_sid)&set(process_df[process_df.action == action].sid.unique()))

    tmp_df = process_df[process_df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()
    role_tmp_df = role_df[role_df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()
    tmp_df = tmp_df.drop_duplicates(['sid', 'round', 'action', 'object'])

    lst = []
    for object, gb_df in tmp_df.groupby('object'):
        lst.append({'uid':gb_df.object.values[0],
                    'number':gb_df[gb_df.action == action].sid.nunique(),
                    'session_number':role_tmp_df[role_tmp_df.uid == object].sid.nunique(),
                })
    tmp_df = pd.DataFrame(lst)
    tmp_df = pd.merge(user_df, tmp_df,
            on='uid').copy()
    tmp_df['ratio'] = tmp_df.number/tmp_df.session_number
    tmp_df = tmp_df[tmp_df.number>0]
    tmp_df = tmp_df.sort_values('ratio',ascending=True)

    return tmp_df

def get_role_sum_df(board, role, start_time, end_time, public):
    if board != '全部':
        if public:
            sid_lst = session_df[(session_df.date>=start_time)&
                                (session_df.date<=end_time)&
                                (session_df.board == board)&
                                (session_df.public == 'public')].sid.values
        else:
            sid_lst = session_df[(session_df.date>=start_time)&
                                (session_df.date<=end_time)&
                                (session_df.board == board)].sid.values
        tmp_role_df = role_df[role_df.apply(lambda df:df.sid in sid_lst, axis=1)].copy()
    else:
        if public:
            sid_lst = session_df[(session_df.date>=start_time)&
                                 (session_df.date<=end_time)&
                                 (session_df.public == 'public')].sid.values
        else:
            sid_lst = session_df[(session_df.date>=start_time)&
                                 (session_df.date<=end_time)].sid.values
        tmp_role_df = role_df.copy()
    sid_lst = list(set(sid_lst)&set(tmp_role_df[tmp_role_df.role == role].sid))

    lst = []
    for uid, gp_df in tmp_role_df.groupby('uid'):
        tmp_gp_df = gp_df[gp_df.apply(lambda df:df.sid in sid_lst, axis=1)].copy()
        lst.append({'uid':uid,
                    'number':tmp_gp_df[tmp_gp_df.role == role].sid.nunique(),
                    'session_number':tmp_gp_df.shape[0],
                    })
    tmp_df = pd.DataFrame(lst)
    tmp_df = pd.merge(user_df, tmp_df,
            on='uid').copy()
    tmp_df['ratio'] = tmp_df.number/tmp_df.session_number
    tmp_df = tmp_df[tmp_df.number>0]
    tmp_df = tmp_df.sort_values('ratio',ascending=True)

    return tmp_df

def get_personal_role_win_df(name, start_time, end_time):
    _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)].copy()
    tmp_df = {}
    for i, gp_df in _tmp_df.groupby('role'):
        tmp_df[i] = {'win':gp_df.win.sum()/gp_df.shape[0]}
    tmp_df = pd.DataFrame(tmp_df)

    return tmp_df

def get_final_process_df(start_time, end_time):
    include_sid = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].sid.values
    tmp_process_df = process_df[process_df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()

    final_process_df = pd.merge(df.loc[:, ['sid','uid','role','name','god','villager','wolf']], tmp_process_df, on=['sid','uid'], how='right')
    final_process_df = pd.merge(df.loc[:, ['sid','uid','role','god','villager','wolf']].rename(
        columns={'uid':'object', 'role':'object_role', 'god':'object_god', 'villager':'object_villager', 'wolf':'object_wolf'}),
                final_process_df, on=['sid','object'], how='right')
    return final_process_df

def get_camp_sum_df(name, start_time, end_time):
    _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)].copy()
    tmp_df = _tmp_df.loc[:,['god',	'villager',	'wolf']].sum()
    return tmp_df

def get_camp_win_df(name, start_time, end_time):
    _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)].copy()
    tmp_df = _tmp_df.loc[:,['god',	'villager',	'wolf']].sum()
    tmp_df = pd.DataFrame({
            'god':{'win':_tmp_df[_tmp_df.god].win.sum()/_tmp_df[_tmp_df.god].shape[0]},
            'villager':{'win':_tmp_df[_tmp_df.villager].win.sum()/_tmp_df[_tmp_df.villager].shape[0]},
            'wolf':{'win':_tmp_df[_tmp_df.wolf].win.sum()/_tmp_df[_tmp_df.wolf].shape[0]},
        }).fillna(0)

    return tmp_df

def get_sunburst_lst(name, start_time, end_time, public):
    if public:
        _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)&(df.public == 'public')].copy()
    else:
        _tmp_df = df[(df.name == name)&(df.date>=start_time)&(df.date<=end_time)].copy()
    _tmp_df['camp'] = df.apply(lambda df:'神' if df.god else '民' if  df.villager else '狼', axis = 1)
    _tmp_df['win'] = df.apply(lambda df:'贏' if df.win else '輸', axis = 1)
    _tmp_df['total_n'] = 1

    ids, labels, parents, values = [], [], [], []
    shapes, colors = [], []
    for camp, camp_v in _tmp_df.camp.value_counts().items():
        if camp == '民':color = "rgba(0,102,51,1)"
        elif camp == '神':color = "rgba(0,76,153,1)"
        elif camp == '狼':color = "rgba(153,0,0,1)"
        ids.append(camp)
        labels.append(camp)
        parents.append("")
        values.append(camp_v)
        shapes.append('')
        colors.append(color)
        role_color = 0.3
        for role, role_v in _tmp_df[_tmp_df.camp == camp].role.value_counts().items():
            ids.append(f"{camp} - {role}")
            labels.append(role)
            parents.append(camp)
            values.append(role_v)
            shapes.append('')
            colors.append(color.replace(',1)', f', {role_color}'))
            role_color+=0.075
            for win, win_v in _tmp_df[_tmp_df.role == role].win.value_counts().items():
                if win == '贏':win_color = "rgba(255,222,162,0.5)"
                else:win_color = win_color = "rgba(5,5,5,0.5)"
                ids.append(f"{role} - {win}")
                labels.append(win)
                parents.append(f"{camp} - {role}")
                values.append(win_v)
                shapes.append('/')
                colors.append(win_color)


    return ids, labels, parents, values, shapes, colors

def get_player_df(name):
    uid = user_df[user_df.name == name].uid.values[0]

    player_df = process_df[process_df.uid == uid]
    tmp_df = []
    for _, items in player_df.iterrows():
        _tmp_df = list()
        s_df = session_df.loc[session_df['sid'] == items['sid'],
                    ["date", "session", "board", "result"]].reset_index(drop=True)
        s_df.rename(columns={'date':'日期', "session":'場次', 'board':'板子', 'result':'獲勝方'}, inplace=True)
        _tmp_df.append(s_df)

        s_df = role_df.loc[(role_df['sid'] == items['sid'])&(role_df['uid'] == uid),
                    ['role','set number']].reset_index(drop=True)
        s_df.rename(columns={'role':'角色', "set number":'座位'}, inplace=True)
        _tmp_df.append(s_df)

        s_df = role_df.loc[(role_df['sid'] == items['sid'])&(role_df['uid'] == items['object']),
                    ['name', 'role','set number']].reset_index(drop=True)
        s_df.rename(columns={'name':'對象姓名', 'role':'對象角色', "set number":'對象座位'}, inplace=True)
        _tmp_df.append(s_df)


        _tmp_df = pd.concat(_tmp_df, axis = 1)
        _tmp_df['動作'] = items['action']
        _tmp_df['輪次'] = items['round']
        _tmp_df = _tmp_df.loc[:, ['日期', '場次', '板子', '輪次', '角色', '座位', '動作', '對象姓名', '對象角色', '對象座位', '獲勝方']]
        tmp_df.append(_tmp_df)
    tmp_df = pd.concat(tmp_df).reset_index(drop=True)

    return tmp_df

def get_allpalyer_df(date, session):

    tmp_session_df = session_df[(session_df.date == date)&(session_df.session==session)].reset_index()
    session_info = {i:v[0] for i, v in tmp_session_df.to_dict().items()}
    tmp_process_df = process_df[process_df.sid == session_info["sid"]]
    tmp_df = []
    for _, items in tmp_process_df.iterrows():
        _tmp_df = list()

        s_df = role_df.loc[(role_df['sid'] == items['sid'])&(role_df['uid'] == items['uid']),
                    ['name', 'role','set number']].reset_index(drop=True)
        s_df.rename(columns={'name':'姓名','role':'角色', "set number":'座位'}, inplace=True)
        _tmp_df.append(s_df)

        s_df = role_df.loc[(role_df['sid'] == items['sid'])&(role_df['uid'] == items['object']),
                    ['name', 'role','set number']].reset_index(drop=True)
        s_df.rename(columns={'name':'對象姓名', 'role':'對象角色', "set number":'對象座位'}, inplace=True)
        _tmp_df.append(s_df)


        _tmp_df = pd.concat(_tmp_df, axis = 1)
        _tmp_df['動作'] = items['action']
        _tmp_df['輪次'] = items['round']
        _tmp_df['動作'] = items['action']

        _tmp_df = _tmp_df.loc[:, ['輪次', '姓名', '角色', '座位', '動作', '對象姓名', '對象角色', '對象座位']]
        tmp_df.append(_tmp_df)

    tmp_df = pd.concat(tmp_df).reset_index(drop=True)
    return session_info, tmp_df


