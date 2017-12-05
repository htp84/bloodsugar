import plotly.graph_objs as go
import plotly.plotly as py
#import matplotlib.pyplot as plt
#import seaborn as sns

def scatter_(df):
    return {'data': [go.Scatter(
            x=df['date1'],
            y=df['mmol'],
            text=df['date1'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                #'color': 'red'
                'color': df['label']
            }
        )],
        'layout': go.Layout(
            margin={'l': 10, 'b': 30, 't': 10, 'r': 0},
            height=600,
            hovermode='closest'
        )
    }


def histogram_(df):
    #fig = sns.distplot(df['mmol'], kde=False, bins=15)
    return {'data': [go.Histogram(
                    x=df['mmol'],
                    )
         ]
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