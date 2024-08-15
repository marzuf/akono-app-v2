import dash_daq as daq
from settings import *
from utils_fcts import *
import plotly.express as px
from datetime import timedelta
import pandas as pd
import openpyxl
import numpy as np
from dash import dash_table
import pandas as pd
from datetime import datetime, timedelta
from app_settings import *
from plotly.subplots import make_subplots
from dash.dependencies import ALL


from callbacks.common_callbacks import register_callbacks as register_dashboard_common
from callbacks.tab_analyseGraphes_callbacks import register_callbacks as register_dashboard_analyseGraphes
from callbacks.render_content_callback import register_callbacks as register_render_content
from callbacks.tab_appareils_callbacks import register_callbacks as register_appareils
from callbacks.tab_timeevolution_callbacks import register_callbacks as register_timeevo
from callbacks.tab_fonctions_callbacks import register_callbacks as register_fonctions
from callbacks.tab_stat_callbacks import register_callbacks as register_stat
from callbacks.tab_dashboard_callbacks import register_callbacks as register_dashboard
from callbacks.tab_data_callbacks import register_callbacks as register_data

##################################### TODO IN PROCESS : dashboard
# https://dash.gallery/dash-manufacture-spc-dashboard/
# https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-manufacture-spc-dashboard/app.py


## prend les dates seulement dayP -> assume partt les mm !!


# Initialiser l'application Dash avec suppression des exceptions de callback
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
                suppress_callback_exceptions=True)

register_dashboard_common(app)
register_dashboard_analyseGraphes(app)
register_render_content(app)
register_appareils(app)
register_timeevo(app)
register_stat(app)
register_fonctions(app)
register_data(app)
register_dashboard(app)

# Définir la mise en page de l'application

all_confirm_dialogs = [dcc.ConfirmDialog(id=x,message='')
                       for x in all_confirm_dialogs]

all_maxvar_dialogs = [dcc.ConfirmDialog(id=x,message=popupmsg_maxvar)
                       for x in ['confirm-dialog',
                                 'confirm-dialog-daydataP',
                                 'confirm-dialog-daydataI',
                                 ]]
all_range_pickers = [get_range_picker(x) for x in all_range_pickers]

app.layout = html.Div([
    dcc.Tabs(id="tabs-example", value='tab-dashboard', children=[  # value ici définit l'onglet par défaut
        dcc.Tab(label='Dashboard', value='tab-dashboard',
                className='mytab', selected_className='mytab-slctd',
                children=[
                    dcc.Tabs(id="subtabs-dashboard", value='subtab-dayIdata', children=[
                        dcc.Tab(label='Données minutes', value='subtab-minutesdata',
                                className='mysubtab', selected_className='mysubtab-slctd'),
                        dcc.Tab(label='Données journalières', value='subtab-dayIdata',
                                className='mysubtab', selected_className='mysubtab-slctd'),

                    ]),                        dcc.Store(id='store-summary-minutes'),
                        dcc.Store(id='store-dbTime_df'),
                        dcc.Store(id='store-summary-dayI'),
                        dcc.Store(id='store-dbDayI_df')]),

        dcc.Tab(label='Evolution temporelle', value='tab-evotime',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Statistiques', value='tab-stat',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Analyse (graphes)', value='tab-analyseGraph',
                className='mytab', selected_className='mytab-slctd'),
        dcc.Tab(label='Par appareil', value='tab-appareils',
                className='mytab', selected_className='mytab-slctd',
             children=[
            dcc.Tabs(id="subtabs-appareils", value='subtab-bsp', children=[
                dcc.Tab(label='BSP', value='subtab-bsp',
                        className='mysubtab', selected_className='mysubtab-slctd'),
                dcc.Tab(label='VarioTrack', value='subtab-variotrack',
                            className='mysubtab', selected_className='mysubtab-slctd'),
                dcc.Tab(label='Xtender', value='subtab-xtender',
                                className='mysubtab', selected_className='mysubtab-slctd')
            ])]),
        dcc.Tab(label='Par fonction', value='tab-fonctions',
                className='mytab', selected_className='mytab-slctd',
                children=[
                    dcc.Tabs(id="subtabs-fonctions", value='subtab-batterie', children=[
                        dcc.Tab(label='Batterie', value='subtab-batterie',
                                className='mysubtab', selected_className='mysubtab-slctd')
                    ])]),

        dcc.Tab(label='Données', value='tab-data',
                className='mytab', selected_className='mytab-slctd',
                children=[
                    dcc.Tabs(id="subtabs-data", value='subtab-updateDB', children=[
                        dcc.Tab(label='Gérer les données', value='subtab-updateDB',
                                className='mysubtab', selected_className='mysubtab-slctd'),
                        dcc.Tab(label='Exporter des données', value='subtab-exportDB',
                                    className='mysubtab', selected_className='mysubtab-slctd'),
                        dcc.Tab(label='Aperçu de la base de données', value='subtab-showDB',
                                className='mysubtab', selected_className='mysubtab-slctd')
                    ])])
             ]),
    dcc.DatePickerSingle(
        id='date-picker-dbdata',
        date=None,
        display_format='DD.MM.YYYY',
        min_date_allowed=min(fetch_timedata_dates()),
        max_date_allowed=max(fetch_timedata_dates()),
        disabled_days=[pd.to_datetime(date).date() for date in
                       pd.date_range(start=min(fetch_timedata_dates()),
                                     end=max(fetch_timedata_dates())).
                       difference(pd.to_datetime(fetch_timedata_dates()))],
        style={'display': 'none'}  # Initialement caché
        # attention : pd.date_range(...).retourne un DatetimeIndex
        # pd.to_datetime pour convertir all_dates aussi en DatetimeIndex pr comparer
    )] +
                      all_range_pickers +
                      all_maxvar_dialogs +
                      all_confirm_dialogs+
    [html.Div(id='tabs-content')]

)






# ################################ CALLBACKS - TAB TIMEDATA - GRAPHIQUES TEMPORELS DONNEES HORAIRES
# @app.callback(
#     Output('time-series-graph', 'figure'),
#     [Input('timedata-column-dropdown', 'value')]
# )
# def update_graph(selected_columns):
#     if not selected_columns:
#         return go.Figure()
#
#     # Lire toutes les données de la base de données
#     df = fetch_timedata()
#     fig = go.Figure()
#     for i, col in enumerate(selected_columns):
#         # Ajout de chaque variable sur un axe y différent
#         fig.add_trace(
#             go.Scatter(
#                 x=df[db_timecol],
#                 y=df[col],
#                 mode='lines',
#                 name=col,
#                 yaxis=f'y{i + 1}'
#             )
#         )
#     update_layout_cols(selected_columns)
#     fig.update_layout(
#         xaxis=dict(domain=[0.25, 0.75], showline=True, linewidth=2, linecolor='black'),
#         yaxis=yaxis_layout,
#         yaxis2=yaxis2_layout,
#         yaxis3=yaxis3_layout,
#         yaxis4=yaxis4_layout,
#         title_text="",  ## titre en-haut à gauche
#         margin=dict(l=40, r=40, t=40, b=30)
#     )
#     return fig
#
# # callback pour vérifier le nombre de variables sélectionnées et afficher la pop-up :
# @app.callback(
#     [Output('confirm-dialog', 'displayed'),
#      Output('timedata-column-dropdown', 'value')],
#     [Input('timedata-column-dropdown', 'value')]
# )
# def limit_selection_timedata(selected_columns):
#     if len(selected_columns) > maxTimePlotVar:
#         return True, selected_columns[:maxTimePlotVar]  # Afficher la pop-up et limiter la sélection à 2
#     return False, selected_columns  # Ne pas afficher la pop-up
# # Ajouter un callback pour mettre à jour la description
# @app.callback(
#     Output('timedata-column-description', 'children'),
#     [Input('timedata-column-dropdown', 'value')]
# )
# def update_description(selected_columns):
#     if selected_columns:
#         desc_txt = '<br>'.join(["<b>" + selcol + "</b> : " + showcols_settings[selcol]['description']
#                                 for selcol in selected_columns])
#         return html.Div([dcc.Markdown(desc_txt,
#                                       dangerously_allow_html=True)])
#     return html.P('No column selected')


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
    # for deploy
    #     app.run(debug=True, host='0.0.0.0', port=7860)
