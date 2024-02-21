import pandas as pd
from util import data

def home_one(start_time, end_time):
    tmp_df = data.get_final_df(start_time, end_time)
    tmp_df = tmp_df.sort_values('win', ascending=True)
    return {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {"type": 'shadow'}},
          "graphic": {
        "elements": [
        {
          "type": 'text',
          "left": "12%",
          "top": "3%",
          "style": {
            "text": '勝率',
            "fontSize": 25,
            "fontWeight": 'bold',
            "lineDash": [0, 200],
            "lineDashOffset": 0,
            "stroke": '#4C5058',
            "lineWidth": 1}},
        {
          "type": 'text',
          "left": "55%",
          "top": "3%",
          "style": {
            "text": 'MVP率',
            "fontSize": 25,
            "fontWeight": 'bold',
            "lineDash": [0, 200],
            "lineDashOffset": 0,
            "stroke": '#4C5058',
            "lineWidth": 1}},
        {
          "type": 'text',
          "left": "77%",
          "top": "3%",
          "style": {
            "text": '參與場次',
            "fontSize": 25,
            "fontWeight": 'bold',
            "lineDash": [0, 200],
            "lineDashOffset": 0,
            "stroke": '#4C5058',
            "lineWidth": 1}}
            ]},
        "grid": [
            {"width": '50%',
             "bottom": '0%',
             "left": 10,
             "containLabel": True},
            {"width": '20%',
             "bottom": '0%',
             "left": '53%',
             "containLabel": True},
            {"width": '20%',
             "bottom": '0%',
             "left": '76%',
             "containLabel": True}],
        "xAxis": [{"type": "value"},
                  {"type": "value", "gridIndex": 1},
                  {"type": "value", "gridIndex": 2}],
        "yAxis": [{
            "type": "category",
            "data": list(tmp_df.name.values),
        },{
            "gridIndex": 1,
            "type": "category",
            "data": list(tmp_df.name.values),
            "axisLabel": {"show": False},
        },{
            "gridIndex": 2,
            "type": "category",
            "data": list(tmp_df.name.values),
            "axisLabel": {"show": False},
        }],
        "series": [
            {"data": list(tmp_df.win.values),
            #  "showBackground": True,
             "type": "bar",
            },
            {"data": list(tmp_df.mvp.values),
            #  "showBackground": True,
             "type": "bar",
             "xAxisIndex": 1,
             "yAxisIndex": 1,
             "itemStyle": {"color": '#abc'},
            },
            {"data": [int(i) for i in tmp_df.session_number.values],
            #  "showBackground": True,
             "type": "bar",
             "xAxisIndex": 2,
             "yAxisIndex": 2,
             "itemStyle": {"color": '#bce'},
            }
        ],
    }

def home_two(start_time, end_time):
    tmp_df = data.get_board_proportion_df(start_time, end_time)

    return {
        "title": {
            "text": '板子統計',
            "left": 'center'},
        "tooltip": {"trigger": 'item'},
        "series":[{
            "type": 'pie',
            "radius": [90, 140],
            "center": ['50%', '50%'],
            "roseType": 'area',
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2},
            "label": {
                "formatter": '{b|{b}}\n{hr|}\n{c} {per|{d}%}',
                "rich": {
                    "hr": {
                        "borderColor": '#8C8D8E',
                        "width": '100%',
                        "borderWidth": 1,
                        "height": 0
                    },
                    "b": {
                        "color": '#4C5058',
                        "fontSize": 14,
                        "fontWeight": 'bold',
                        "lineHeight": 33
                    },
                    "per": {
                        "color": '#fff',
                        "backgroundColor": '#4C5058',
                        "padding": [3, 4],
                        "bordeRadius": 4
                    }
                }
            },
            "data": [{"value": value, "name":name}
                for name, value in tmp_df.to_dict()['sid'].items()]
        }]
    }

def home_three(start_time, end_time):
    tmp_df = data.get_win_sum_df(start_time, end_time)
    tmp_df2 = data.get_win_proportion_df(start_time, end_time)
    return {
    "grid": {
        "left": '0%',
        "right": '55%',
        "containLabel": True
    },
    "xAxis": [{"type": 'value'}],
    "yAxis": [{"type": 'category',
        "axisTick": {"show": False},
        "data": list(tmp_df.index)}
    ],
    "graphic": {
        "elements": [
      {
        "type": 'text',
        "left": "12%",
        "top": 0,
        "style": {
          "text": '日期&勝負統計',
          "fontSize": 25,
          "fontWeight": 'bold',
          "lineDash": [0, 200],
          "lineDashOffset": 0,
          "stroke": '#4C5058',
          "lineWidth": 1}},
      {
        "type": 'text',
        "left": "62%",
        "top": 0,
        "style": {
          "text": '好人獲勝率',
          "fontSize": 25,
          "fontWeight": 'bold',
          "lineDash": [0, 200],
          "lineDashOffset": 0,
          "stroke": '#4C5058',
          "lineWidth": 1}}
          ]},
    "series": [
        {
        "name": '好人陣營',
        "type": 'bar',
        "stack": 'Total',
        "label": {"show": True},
        "emphasis": {"focus": 'series'},
        "data": [int(i) for i in tmp_df['好'].values]
        },
        {
        "name": '狼人陣營',
        "type": 'bar',
        "stack": 'Total',
        "label": {"show": True},
        "emphasis": {"focus": 'series'},
        "data": [-int(i) for i in tmp_df['狼'].values]
        },
        {
        "center":["70%", "60%"],
      "type": 'gauge',
      "startAngle": 200,
      "endAngle": -20,
      "radius":"60%",
      "min": 0,
      "max": 100,
      "splitNumber": 10,
      "itemStyle": {
        "color": '#58D9F9',
        "shadowColor": 'rgba(0,138,255,0.45)',
        "shadowBlur": 10,
        "shadowOffsetX": 2,
        "shadowOffsetY": 2
      },
      "progress": {
        "show": True,
        # "roundCap": True,
        "width": 30
      },
      "pointer": {
          "show": False, 
        "icon": 'path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z',
        "length": '75%',
        "width": 16,
        "offsetCenter": [0, '5%']
      },
      "axisLine": {
        # "roundCap": True,
        "lineStyle": {
          "width": 30
        }
      },
      "axisTick": {
          "distance": -45,
        "splitNumber": 5,
        "lineStyle": {
          "width": 2,
          "color": '#999'
        }
      },
      "splitLine": {
          "distance": -52,
        "length": 14,
        "lineStyle": {
          "width": 3,
          "color": '#999'
        }
      },
      "axisLabel": {
        "distance": -20,
        "color": '#999',
        "fontSize": 20
      },
      "anchor": {
        "show": True
      },

      "detail": {
          "valueAnimation": True,
          "width": '60%',
          "lineHeight": 40,
          "borderRadius": 8,
        "backgroundColor": '#fff',
        "offsetCenter": [0, '-15%'],
        "fontSize": 25,
        "fontWeight": 'bolder',
        "formatter": '{value} %',
        "color": 'inherit'
        
      },
      "data": [
        {
          "value": round(tmp_df2.loc['好', :].values[0]/tmp_df2.sum().values[0], 4)*100
        }
      ]}],
    "legend": {
    "show": True,
    "data": ['狼人陣營', '好人陣營'],
     "bottom": 0,
     "left": 0,
  }
    }

def home_four(start_time, end_time):
  tmp_df = data.get_seat_df(start_time, end_time)
  tmp_df2 = (tmp_df/tmp_df.sum()).T
  return {
      "title": {
            "text": '座位風水圖',
            "left": 'center',
             "top": -5},
  "angleAxis": {
    "type": 'category',
    "data": [str(i) for i in tmp_df.columns]
  },
  "radiusAxis": {},
  "polar": {},
  "series": [
    {
      "type": 'bar',
      "data": list(tmp_df2.god.values),
      "label": {"show": True},
      "coordinateSystem": 'polar',
      "name": 'god',
      "stack": 'a',
      "emphasis": {
        "focus": 'series'
      }
    },
    {
      "type": 'bar',
      "data": list(tmp_df2.villager.values),
      "label": {"show": True},
      "coordinateSystem": 'polar',
      "name": 'villager',
      "stack": 'a',
      "emphasis": {
        "focus": 'series'
      }
    },
    {
      "type": 'bar',
      "data": list(tmp_df2.wolf.values),
      "label": {"show": True},
      "coordinateSystem": 'polar',
      "name": 'wolf',
      "stack": 'a',
      "emphasis": {
        "focus": 'series'
      }
    }
  ],
    "legend": {
    "show": True,
    "data": ['god', 'villager', 'wolf'],
     "bottom": -5,
  }
}

