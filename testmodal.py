import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

# Sample DataFrame
dbTime_df = pd.DataFrame({
    'time': pd.date_range(start='2023-01-01', periods=10, freq='T'),
    'XT_Ubat_MIN_Vdc_I3090_L1': range(10, 20),
    'XT_Ubat_MIN_Vdc_I3090_L2': range(20, 30),
    'XT_Uin_Vac_I3113_L1': range(30, 40)
})

summary = pd.DataFrame({
    'Column': ['XT_Ubat_MIN_Vdc_I3090_L1', 'XT_Ubat_MIN_Vdc_I3090_L2', 'XT_Uin_Vac_I3113_L1'],
    'Minutes with Data': [7, 8, 9],
    'Minutes with Missing Data': [3, 2, 1]
})

def generate_header_row():
    return html.Div(
        className="row metric-row header-row",
        children=[
            html.Div(
                className="one column metric-row-header",
                children=html.Div("Mesures"),
            ),
            html.Div(
                className="two columns metric-row-header",
                children=html.Div("# minutes avec valeurs"),
            ),
            html.Div(
                className="two columns metric-row-header",
                children=html.Div("# minutes manquantes"),
            ),
            html.Div(
                className="four columns metric-row-header",
                children=html.Div("Sparkline"),
            ),
            html.Div(
                className="four columns metric-row-header",
                children=html.Div("dispo."),
            ),
        ],
    )

def generate_summary_row(id_suffix, column_name, minutes_with_data, minutes_with_missing_data, sparkline_data, time_data):
    ooc_graph_id = f"ooc_graph_{id_suffix}"

    total_minutes = minutes_with_data + minutes_with_missing_data
    percentage_with_data = (minutes_with_data / total_minutes) * 100
    percentage_missing_data = (minutes_with_missing_data / total_minutes) * 100

    minutes_with_data_text = f"{minutes_with_data} ({percentage_with_data:.0f}%)"
    minutes_with_missing_data_text = f"{minutes_with_missing_data} ({percentage_missing_data:.0f}%)"

    sparkline_figure = go.Figure(
        {
            "data": [
                {
                    "x": time_data,
                    "y": sparkline_data,
                    "mode": "lines",
                    "line": {"color": "#f4d44d"},
                    "name": column_name,
                }
            ],
            "layout": {
                "margin": dict(l=0, r=0, t=0, b=0, pad=0),
                "xaxis": dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
                "yaxis": dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
            },
        }
    )

    return html.Div(
        className="row metric-row",
        children=[
            html.Div(
                className="one column metric-row-button-text",
                children=html.Button(
                    children=column_name,
                    id=f"button-{column_name}",
                    n_clicks=0,
                ),
            ),
            html.Div(
                className="two columns",
                children=html.Div(
                    children=minutes_with_data_text,
                ),
            ),
            html.Div(
                className="two columns",
                children=html.Div(
                    children=minutes_with_missing_data_text,
                ),
            ),
            html.Div(
                className="four columns",
                children=dcc.Graph(
                    id=f"sparkline_{id_suffix}",
                    figure=sparkline_figure,
                    style={"width": "100%", "height": "50px"},
                    config={"staticPlot": True, "displayModeBar": False},
                ),
            ),
            html.Div(
                className="four columns",
                children=daq.GraduatedBar(
                    id=ooc_graph_id,
                    color={
                        "ranges": {
                            "#f45060": [0, 3],
                            "#f4d44d": [3, 7],
                            "#13aa13": [7, 10],
                        }
                    },
                    showCurrentValue=False,
                    max=10,
                    value=percentage_with_data / 10,
                    size=250,
                ),
            ),
        ],
    )

# Conversion des données
dbTime_df['time'] = pd.to_datetime(dbTime_df['time'])
time_data = dbTime_df['time']

# Générer le contenu des lignes avec jauge et ajouter l'en-tête
div_container = [generate_header_row()]
for i, row in summary.iterrows():
    sparkline_data = dbTime_df[row['Column']]
    div_container.append(
        generate_summary_row(
            i,
            row['Column'],
            row['Minutes with Data'],
            row['Minutes with Missing Data'],
            sparkline_data,
            time_data
        )
    )

# Modal structure
div_container.append(
    html.Div(
        id="graph-modal",
        style={"display": "none"},
        children=[
            html.Div(
                id="modal-content",
                children=[
                    html.Button("Close", id="close-modal", n_clicks=0),
                    dcc.Graph(id="modal-graph")
                ],
                style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "background-color": "white",
                    "padding": "20px",
                    "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.5)",
                    "z-index": "1000",
                    "width": "80%",
                    "height": "80%",
                    "overflow": "auto"
                }
            ),
            html.Div(
                style={
                    "position": "fixed",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "background-color": "rgba(0, 0, 0, 0.5)",
                    "z-index": "999"
                }
            )
        ]
    )
)

app.layout = html.Div(
    children=[
        html.H3("Summary with Data Availability Gauge"),
        html.Div(
            id="summary-container",
            children=div_container,
        )
    ]
)

# Unique callback pour gérer l'ouverture et la fermeture du modal
@app.callback(
    [Output('graph-modal', 'style'),
     Output('modal-graph', 'figure')],
    [Input(f"button-{col}", "n_clicks") for col in summary['Column']] + [Input('close-modal', 'n_clicks')],
    [State('graph-modal', 'style')]
)
def toggle_modal(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        return {"display": "none"}, go.Figure()

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id.startswith('button-'):
        column_name = triggered_id.split('-')[1]
        fig = go.Figure(
            data=[
                go.Scatter(x=dbTime_df['time'], y=dbTime_df[column_name], mode='lines')
            ],
            layout=go.Layout(
                title=f"Courbe de {column_name} en fonction du temps",
                xaxis_title="Time",
                yaxis_title=column_name
            )
        )
        return {"display": "block"}, fig

    elif triggered_id == 'close-modal':
        return {"display": "none"}, go.Figure()

    return {"display": "none"}, go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)
