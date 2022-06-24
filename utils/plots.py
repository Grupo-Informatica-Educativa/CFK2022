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

def legend_position(fig,orientation="h",yanchor="bottom",xanchor="left",y=-0.2, x=0):
    fig.update_layout(legend=dict(
        orientation=orientation,
        yanchor=yanchor,
        y=y,
        xanchor=xanchor,
        x=x
    ))

def text_position(fig,pos="outside"):
    fig.update_traces(textposition=pos)

def labels(fig,xlabel=None,ylabel=None):
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)

def percentage_labelsy(fig,xlabel=None,ylabel=None):
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig.update_traces(texttemplate='%{text:,.0%}')

def percentage_labelsx(fig,xlabel=None,ylabel=None):
    fig.for_each_xaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig.update_xaxes( range=(-0.1,1.1))