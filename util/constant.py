from util import data
from datetime import datetime, timedelta
CHARTMODE = None
CHARTMODEINDEX = 0
PLOTCOLOR = "Dark2"
PLOTCOLORINDEX = 4

# STARTTIME = data.df.date.min()
STARTTIME = (datetime.strptime(data.df.date.min(), '%Y/%m/%d').date()-timedelta(days = 1)).strftime("%Y/%m/%d")
ENDTIME = data.df.date.max()

def update(_STARTTIME, _ENDTIME):
    global STARTTIME, ENDTIME
    STARTTIME, ENDTIME = _STARTTIME, _ENDTIME

