import plotly.graph_objs as go


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
    return {'data': [go.Histogram(
                    y=df['mmol'])
         ]
    }
