import dash
import numpy as np
from apps.src.secrets import CONN_STR
from apps.src.data import data
df = data(CONN_STR, latest=True)
app = dash.Dash(__name__)
app.title = str(np.round(df.at[0, 'mmol'],1))
server = app.server
app.config.suppress_callback_exceptions = True
