def plotly_settings(px):
    px.defaults.template = "plotly_white"
    px.color_discrete_sequence= px.colors.qualitative.Set2
    px.defaults.width = 600
    px.defaults.height = 400

def center_title(fig):
    fig.update_layout(
        title={
        'x':0.5,
        'xanchor': 'center'
    })


def get_config(scrollZoom=True,displaylogo=False,responsive=True,editable=True,height=None,width=None,scale=3):
    return {
        'scrollZoom': scrollZoom,
        'displaylogo': displaylogo,
        'responsive': responsive,
        'editable': editable,
        'toImageButtonOptions': {
            'format': 'png',  # one of png, svg, jpeg, webp
            'filename': 'custom_image',
            'height': height,
            'width': width,
            'scale': scale  # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

def legend_position(fig,orientation="h",yanchor="bottom",xanchor="left"):
    fig.update_layout(legend=dict(
        orientation=orientation,
        yanchor=yanchor,
        y=-0.2,
        xanchor=xanchor,
        x=0
    ))

def text_position(fig,pos="outside"):
    fig.update_traces(textposition=pos)

def labels(fig,xlabel=None,ylabel=None):
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)