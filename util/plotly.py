import pandas as pd
from util import data
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

colormap = ["rgba(26,19,52,0.3)", "rgba(38,41,74,0.3)", "rgba(1,84,90,0.3)", "rgba(1,115,81,0.3)",
            "rgba(3,195,131,0.3)", "rgba(170,217,98,0.3)", "rgba(251,191,69,0.3)", "rgba(239,106,50,0.3)",
            "rgba(237,3,69,0.3)", "rgba(161,42,94,0.3)", "rgba(113,1,98,0.3)", "rgba(17,1,65,0.3)"]
np.random.shuffle(colormap)
dark_color = '#555555'
light_color = '#E9E9E9'
font_family = './TaipeiSansTCBeta-Regular.ttf'

def home_1(start_time, end_time):
    tmp_df = data.get_final_df(start_time, end_time)
    tmp_df = tmp_df.sort_values('win', ascending=True)


    fig = make_subplots(
        rows=1, cols=4,
        column_widths=[0.5, 0, 0.25, 0.25],
        specs=[[{"type": "bar", "colspan": 2}, None, {"type": "bar", "colspan": 1}, {"type": "bar", "colspan": 1}]],
        subplot_titles=['<b>勝率</b>', '<b>MVP率</b>', '<b>場次</b>'],
    )

    for i in range(tmp_df.session_number.max()):
        _tmp_df = tmp_df[tmp_df.session_number>i]
        _tmp_df = _tmp_df.sort_values('win', ascending=True)
        fig.add_trace(
            go.Bar(x = _tmp_df.win, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                      color=colormap[0],
                      line=dict(color=dark_color, width=1 ))),
            row=1, col=1)

        fig.add_trace(
            go.Bar(x = _tmp_df.mvp, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                      color=colormap[1],
                      line=dict(color=dark_color, width=1 ))),
            row=1, col=3)

        fig.add_trace(
            go.Bar(x = _tmp_df.session_number, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                     color=colormap[2],
                      line=dict(color=dark_color, width=1 ))),
            row=1, col=4)

    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True

    steps = []
    for i in range(tmp_df.session_number.max()):
        step =  dict(
            method = 'update',
            args = [{'visible':[False] * len(fig.data)}],
            label=f'<b>{i}</b>',

        )
        step["args"][0]["visible"][i*3] = True
        step['args'][0]["visible"][i*3+1] = True
        step['args'][0]["visible"][i*3+2] = True

        steps.append(step)

    sliders = [dict(
        active=0,
        pad={"t": tmp_df.session_number.max()},
        steps=steps,
        currentvalue={"prefix": "<b>參與</b> ", "suffix": " <b>場次以上</b>"},
        minorticklen = 4
    )]

    fig.layout.sliders = sliders

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=30,color=dark_color)

    fig.update_layout(
        autosize=True,
        height=800,
        template=None,
        polar = dict(
            radialaxis = dict(range=[0, 5], showticklabels=False, ticks=''),
            angularaxis = dict(showticklabels=False, ticks='')
        ),
        showlegend=False,
        font=dict(
            family=font_family,
            color=dark_color,
        ),

    )
    fig.update_yaxes(showline=True, linewidth=2, linecolor=dark_color, gridcolor=light_color)
    return fig


def home_2(start_time, end_time):
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.5, 0.5],
        specs=[[{"type": "pie","rowspan": 2}, {"type": "bar"}],
              [         None, {"type": "pie"}]],
        subplot_titles=['<b>板子統計</b>', '<b>日期&勝負統計</b>', '<b>總勝負比</b>']
    )

    tmp_df = data.get_board_proportion_df(start_time, end_time)
    fig.add_trace(
            go.Pie(labels=tmp_df.index,
                                values=tmp_df.sid,
                                hole=.3, marker_colors=colormap, textinfo='label+value+percent',
                  marker_line_color=dark_color ,marker_line_width=1),
            row=1, col=1)


    tmp_df = data.get_win_sum_df(start_time, end_time)
    fig.add_trace(
            go.Bar(x = tmp_df.index, y = tmp_df['好'], marker_color = colormap[0],hoverinfo ='x+y',
                  marker_line_color=dark_color,marker_line_width=1),
            row=1, col=2)

    fig.add_trace(
        go.Bar(x = tmp_df.index, y = tmp_df['狼'], marker_color = colormap[1],hoverinfo ='x+y',
                  marker_line_color=dark_color,marker_line_width=1),
            row=1, col=2,
        )
    tmp_df = data.get_win_proportion_df(start_time, end_time)

    fig.add_trace(
            go.Pie(labels=tmp_df.index,
                                values=tmp_df.sid,
                                hole=.3, marker_colors=colormap, textinfo='label+value+percent',
                  marker_line_color=dark_color,marker_line_width=1),
            row=2, col=2,
        )

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=30,color=dark_color)

    fig.update_layout(margin = dict(t=50, l=0, r=0, b=30),
                      barmode = 'stack', showlegend=False,
                      autosize=True,
                      height=400,
                      font=dict(
                            family=font_family,
                            color=dark_color),
                    )

    return fig


def home_3(start_time, end_time):

    tmp_df = data.get_seat_df(start_time, end_time).T
    tmp_df = pd.concat([tmp_df, tmp_df.iloc[[0], :]])
    theta = ['%s號'%i for i in tmp_df.index]
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'polar'}]*3],
                        subplot_titles=['<b>神</b>', '<b>民</b>', '<b>狼</b>'])

    fig.add_trace(go.Scatterpolar(
          name = "god",
          r = tmp_df.god.values,
          theta = theta,
          fillcolor=colormap[0],
        ), 1, 1)
    fig.add_trace(go.Scatterpolar(
          name = "villager",
          r = tmp_df.villager,
          theta = theta,
        fillcolor=colormap[1]
        ), 1, 2)
    fig.add_trace(go.Scatterpolar(
          name = "wolf",
          r = tmp_df.wolf,
          theta = theta,
        fillcolor=colormap[2]
        ), 1, 3)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=20,color=dark_color)
        i.update(y=0.5)
    fig.update_traces(fill='toself', line_color=dark_color)
    fig.update_layout(title=dict(text='<b>風水圖</b>', font=dict(size=30, color=dark_color),
                                  automargin=True, yref='paper'),
                      margin = dict(t=30, l=0, r=0, b=30),
                      autosize=True,
                      height=400,
                      font=dict(
                            family=font_family,
                            color=dark_color),)



    return fig


def action_1(action, start_time, end_time):
    tmp_df = data.get_action_df(action, start_time, end_time)

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.25, 0.25],
        specs=[[{"type": "bar", "colspan": 1}, {"type": "bar", "colspan": 1}]],
        subplot_titles=['<b>%s王</b>'%action if action == '自爆' else '<b>被%s王</b>'%action,
                        '<b>參與場次&%s次數</b>'%action if action == '自爆' else '<b>參與場次&被%s次數</b>'%action],
    )

    for i in range(tmp_df.session_number.max()):
        _tmp_df = tmp_df[tmp_df.session_number>i]
        _tmp_df = _tmp_df.sort_values('ratio', ascending=True)
        fig.add_trace(
            go.Bar(x = _tmp_df.ratio, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                    color=colormap[0],
                    line=dict(color=dark_color, width=1 ))),
            row=1, col=1)

        fig.add_trace(
            go.Bar(x = _tmp_df.number, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                    color=colormap[1],
                    line=dict(color=dark_color, width=1)
                  )),
            row=1, col=2)

        fig.add_trace(
            go.Bar(x = _tmp_df.session_number, y = [f'{i}' for i in _tmp_df.name],
                  orientation='h', visible=False,hoverinfo ='x+y',
                  marker=dict(
                    color=colormap[2],
                    line=dict(color=dark_color, width=1 )
                  )),
            row=1, col=2)

    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True

    steps = []
    for i in range(tmp_df.session_number.max()):
        step =  dict(
            method = 'update',
            args = [{'visible':[False] * len(fig.data)}],
            label=f'<b>{i}</b>',

        )
        step["args"][0]["visible"][i*3] = True
        step['args'][0]["visible"][i*3+1] = True
        step['args'][0]["visible"][i*3+2] = True

        steps.append(step)



    sliders = [dict(
        active=0,
        pad={"t": tmp_df.session_number.max()},
        steps=steps,
        currentvalue={"prefix": "<b>參與</b> ", "suffix": " <b>場次以上</b>"},
        minorticklen = 4,
    )]

    fig.layout.sliders = sliders


    # fig.update_layout(showlegend=False)
    # fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=30,color=dark_color)

    fig.update_layout(
        autosize=True,
        height=800,
        template=None,
        polar = dict(
            radialaxis = dict(range=[0, 5], showticklabels=False, ticks=''),
            angularaxis = dict(showticklabels=False, ticks='')
        ),
        showlegend=False,
        font=dict(
            family=font_family,
            color=dark_color,
        ),
    )
    fig.update_yaxes(showline=True, linewidth=2, linecolor=dark_color, gridcolor=light_color)

    return fig


def personal_1(name, start_time, end_time):
    ids, labels, parents, values, shapes, colors = data.get_sunburst_lst(name, start_time, end_time)
    fig =go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        textinfo='label+percent entry',
        marker=dict(colors=colors,
                    line=dict(color=light_color),
                    pattern=dict(shape=shapes, solidity=0.9),
                    ),
        hoverlabel=dict(font=dict(family=font_family)),

    ))
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/

    fig.update_layout(title=dict(text='<b>角色池</b>', font=dict(size=30, color=dark_color),
                                  automargin=True, yref='paper'),
                      margin = dict(t=30, l=0, r=0, b=30),
                      autosize=True,
                      height=400,
                      font=dict(
                            family=font_family,
                            color=dark_color),)

    return fig

def personal_2(name):
  # style
    th_props = [
    ('font-size', '16px'),
    ('text-align', 'center'),
    ('font-weight', 'bold'),
    ('color', '#6d6d6d'),
    ('background-color', '#fac88f')
    ]

    td_props = [
    ('font-size', '14px'),
    ('color', '#555555'),
    ]

    styles = [
    dict(selector="th", props=th_props),
    dict(selector="td", props=td_props)
    ]

    # table

    tmp_df = data.get_player_df(name).style.set_properties(**{'text-align': 'left',
                                                              "color": "#555555"}).set_table_styles(styles)
    tmp_df = tmp_df.hide_index()

    return tmp_df


