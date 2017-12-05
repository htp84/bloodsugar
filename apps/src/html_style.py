
def style_(blood_sugar=None):
    if blood_sugar is not None:
        if blood_sugar >= 10:
            style = {'padding': '10px', 'fontSize': '32px', 'background-color': 'red'}
        elif 4 <= blood_sugar < 10:
            style = {'padding': '10px', 'fontSize': '32px', 'background-color': 'green'}
        else:
            style = {'padding': '10px', 'fontSize': '32px', 'background-color': 'pink'}
        return style
    else:
        return {'padding': '10px', 'fontSize': '20px', 'background-color': 'grey',
                "display": "inline-block", "margin-top": "12px", "border-radius": "10%"}