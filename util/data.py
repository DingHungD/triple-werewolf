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

    god = ['通靈師', '預言家', '女巫', '獵人', '獵魔人', '守衛', '魔術師', '黑商', '騎士', '守墓人', '攝夢人']
    villager = ['平民']
    wolf = ['夢魘', '小狼', '黑狼王', '狼美人', '機械狼', '狼兄','血月', '石像鬼', '狼弟']

    df = pd.merge(role_df, user_df, on='uid')
    df = pd.merge(df, session_df, on='sid')

    # 神民狼 獲勝次數
    df['god'] = df.apply(lambda df:(df.role in god), axis=1)
    df['villager'] = df.apply(lambda df:(df.role in villager), axis=1)
    df['wolf'] = df.apply(lambda df:(df.role in wolf), axis=1)

    df['win'] = df.apply(lambda df:(df.wolf)==(df.result == '狼'), axis=1)

reload()
from datetime import datetime, timedelta


def get_final_df(start_time, end_time):

    include_sid = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].sid.values

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


def get_board_proportion_df(start_time, end_time):
    _tmp_df = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].copy()

    column = 'board'
    tmp_df = _tmp_df.groupby(column).count()[['sid']]
    tmp_df = tmp_df.sort_values('sid',ascending=True)

    return tmp_df

def get_win_proportion_df(start_time, end_time):
    _tmp_df = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].copy()

    column = 'result'
    tmp_df = _tmp_df.groupby(column).count()[['sid']]

    return tmp_df

def get_win_sum_df(start_time, end_time):
    _tmp_df = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].copy()

    tmp_df = {}

    for date, gb_df in _tmp_df.groupby('date'):
        tmp_df[date] = {key:value for key, value in gb_df.value_counts('result').items()}

    tmp_df = pd.DataFrame(tmp_df).fillna(0).T

    return tmp_df

def get_seat_df(start_time, end_time):
    include_sid = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].sid.values
    _tmp_df = df[df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()
    tmp_df = {}
    for n, item in _tmp_df.groupby('set number'):
        tmp_df[n] = item.loc[:, ['god',	'villager',	'wolf']].sum()

    tmp_df = pd.DataFrame(tmp_df)

    return tmp_df

def get_action_df(action, start_time, end_time):

    include_sid = session_df[(session_df.date>=start_time)&(session_df.date<=end_time)].sid.values
    final_df = get_final_df(start_time, end_time)

    tmp_df = process_df[process_df.apply(lambda df:df.sid in include_sid, axis = 1)].copy()

    tmp_df = tmp_df.drop_duplicates(['sid', 'round', 'action'])
    tmp_df = tmp_df[tmp_df.action == action].groupby('object')['sid'].count()

    tmp_df = pd.merge(user_df, tmp_df,
            left_on='uid', right_on='object').copy()
    tmp_df = tmp_df.rename(columns = {'sid':'number'})

    tmp_df = pd.merge(tmp_df, final_df.loc[:, ['name','session_number']], on = 'name', how = 'left')
    tmp_df['ratio'] = tmp_df.number/tmp_df.session_number

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

