import plotly.graph_objs as go
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

def scatter_(df, datepart=None):
    if datepart:
        df[datepart] = getattr(df.date1.dt, datepart)
        df[datepart] = df[datepart].apply(lambda n: n+(np.random.uniform(-0.5, 0.4)))
        x = datepart
    else:
        x = 'date1'
    return {'data': [go.Scatter(
            x=df[x],
            y=df['mmol'],
            text='scatter',
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                #'color': 'red'
                'color': df['label']
            }
        )],
        'layout': go.Layout(
            margin={'l': 20, 'b': 30, 't': 10, 'r': 0},
            height=600,
            hovermode='closest',
            yaxis={'range': [1.5, 16]}
        )
    }


def histogram_(df):
    #fig = sns.distplot(df['mmol'], kde=False, bins=15)
    return {'data': [go.Histogram(
                    x=df['mmol'],
                    nbinsx=12
                    )
         ]
    }

def boxplot_(df, datepart=None):
    layout = go.Layout(
    autosize=True,
    #width=500,
    height=800,
    margin=go.Margin(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ))
    if datepart:
        df[datepart] = getattr(df.date1.dt, datepart)
        #df[datepart] = df[datepart].apply(lambda n: n+(np.random.uniform(-0.5, 0.4)))
        x = datepart
    else:
        x = 'weekday'
    x_data = sorted(df[datepart].unique(), reverse=True)
    y_data = []
    for i in x_data:
        y_data.append(list(df[df[datepart]==i]['mmol'].tolist()))
    #print(x_data)
    #print(y_data)
    weekday = {0: 'Måndag',
               1: 'Tisdag',
               2: 'Onsdag',
               3: 'Torsdag',
               4: 'Fredag',
               5: 'Lördag',
               6: 'Söndag',}
    traces = []
    if datepart=='weekday':

        for xd, yd in zip(x_data, y_data):
            traces.append(go.Box(
                x=yd,
                name= weekday.get(xd),
                boxmean='sd'
                )
            )
    else:
        for xd, yd in zip(x_data, y_data):
            traces.append(go.Box(
                x=yd,
                name=xd,
                boxmean='sd'
                )
            )

    #print(traces)
    #källa boxplot= https://plot.ly/python/box-plots/#fully-styled-box-plots se längs ner på sidan
    return {'data': traces,
            'layout': layout
            }
#def histogram__(df):
#    fig = sns.distplot(df['mmol'], kde=False, bins=15)
#    plt.savefig('test.png')
#    #return fig


#html.Div(
#        #[html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))],
#    id='test-hist',    
#    ),
#@app.callback(
#    dash.dependencies.Output('test-hist', 'children'),
#    [dash.dependencies.Input('input-startdate', 'value')])
#def update_png(startdate):
#    df = data(CONN_STR, startdate=str(startdate))
#    histogram__(df)
#    image_filename = 'test.png' # replace with your own image
#    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#    return [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))]