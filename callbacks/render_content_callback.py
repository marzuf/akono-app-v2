from dash.dependencies import Input, Output
from settings import *
from utils_fcts import *

def register_callbacks(app):
    timedata_columns = get_timedata_columns()
    timecols2show = [x for x in timedata_columns if not showcols_settings[x] == "NA"]


    ############################################## MAIN CALLBACK RENDER_CONTENT

    # Callback pour mettre à jour le contenu des onglets
    # NB : component_property ne peut pas être choisi librement !!
    @app.callback(
        Output('tabs-content', 'children'),
        [Input('tabs-example', 'value'),
         Input('date-picker-dbdata', 'date')
         ]
    )
    def render_content(tab, picked_date):
        if tab == 'tab-dashboard':
            return html.Div([
                html.Div(id='subtabs-dashboard-content')
            ])
        elif tab == "tab-data":
            return html.Div([
                html.Div(id='subtabs-data-content')
            ])
        elif tab == 'tab-evotime':
            return html.Div([
                html.H3('Aperçu dans le temps'),
                html.H4(dbTime_name + ' database'),
                get_period_dropdown('evotimeperiod-dropdown'),
                html.Button('Afficher', id='show-evotime-btn', n_clicks=0),
                html.Div(id='evotime-range-info', style={'marginTop': '20px'}),

                dcc.Dropdown(
                    id='evotimeTimeDB-graph-col',
                    placeholder="Choisissez la colonne de données",
                    options=[{'label': col, 'value': col} for col in timecols2show]
                ),
                html.Div(id='evotimeTimeDB-graph-varinfo', style={'marginTop': '20px'}),
                dcc.Dropdown(
                    id='evotimeTimeDB-graph-viz',
                    options=[
                        {'label': 'Line Plot', 'value': 'lineplot'},
                        {'label': 'Bar Plot', 'value': 'barplot'},
                        {'label': 'Box Plot', 'value': 'boxplot'}
                    ],
                    placeholder="Choisissez le type de visualisation"
                ),
                html.Button('Visualiser', id='show-evotimeTimeDBgraph-btn',
                            n_clicks=0),
                dcc.Graph(id='evotimeTimeDB-graph',config= {
                                        'scrollZoom': True  # Activer le zoom avec la molette
                                    })
            ])
        elif tab == 'tab-stat':
            return html.Div([
                html.H3('Valeur moyenne de chacune des variables'),
                get_period_dropdown('statperiod-dropdown'),
                html.Button('Afficher', id='show-stat-btn', n_clicks=0),
                html.Div(id='stat-range-info', style={'marginTop': '20px'}),
                html.Div(id='stat-means-info', style={'marginTop': '20px'}),
                html.H3('Visualisation des données'),
                get_db_dropdown(id='tabstatgraph-db'),
                # dcc.Dropdown(
                #     id='tabstatgraph-db',
                #     options=[
                #         {'label': 'Données horaires', 'value': dbTime_name},
                #         {'label': 'Données journalières P', 'value': dbDayP_name},
                #         {'label': 'Données journalières I', 'value': dbDayI_name}
                #     ],
                #     placeholder="Choisissez la table de données"
                # ),
                dcc.Dropdown(
                    id='tabstatgraph-col',
                    placeholder="Choisissez la colonne de données"
                ),
                html.Div(id='tabstatgraph-varinfo', style={'marginTop': '20px'}),
                dcc.Dropdown(
                    id='tabstatgraph-viz',
                    options=[
                        {'label': 'Line Plot', 'value': 'lineplot'},
                        {'label': 'Bar Plot', 'value': 'barplot'},
                        {'label': 'Box Plot', 'value': 'boxplot'}
                    ],
                    placeholder="Choisissez le type de visualisation"
                ),
                html.Button('Visualiser', id='show-statgraph-btn', n_clicks=0),
                dcc.Graph(id='stat-graph', config= {
                                        'scrollZoom': True  # Activer le zoom avec la molette
                                    })
            ])
        elif tab == 'tab-analyseGraph':
            return html.Div([
                html.H3('Analyse (graphiques)'),
                get_period_dropdown('asGraphPeriod-dropdown'),
                html.Div(id='analyseGraph-period-subtit', children=""),
                html.H4('Répartition des fréquences '),
                dcc.Dropdown(
                    id='asL-dropdown',
                    options=[
                        {'label': 'L1', 'value': 'as_L1'},
                        {'label': 'L2', 'value': 'as_L2'},
                        {'label': 'L1+L2', 'value': 'as_both'}
                    ],
                    value='as_L1',
                    placeholder="Source"
                ),
                html.Button('Afficher', id='show-asGraph-btn', n_clicks=0),
                html.Div(id='analyseGraph-pie-chart-tit', children=""),
                html.Div([
                    html.Div(id='analyseGraph-pie-chart-global', children="", className="col"),
                    html.Div(id='analyseGraph-pie-chart-day', children="", className="col"),
                    html.Div(id='analyseGraph-pie-chart-night', children="", className="col")
                ], className='row'),
                html.H4('Température batterie'),
                html.Div([
                    html.Div(id='analyseGraph-tempbat-barplot', children="", className="col")
                ], className='row')
            ])
        elif tab == 'tab-appareils':
            return html.Div([
                html.Div(id='subtabs-appareils-content')
            ])
        elif tab == 'tab-fonctions':
            return html.Div([
                html.Div(id='subtabs-fonctions-content')
            ])
        # elif tab == 'subtab-updateDB':
        #     return html.Div([
        #         html.H3('Gérer les données'),
        #         html.H4('Ajout de données à partir de fichier(s)'),
        #         dcc.Upload(
        #             id='upload-data',
        #             children=html.Button('Upload Files'),
        #             style={
        #                 'width': '100%',
        #                 'height': '60px',
        #                 'lineHeight': '60px',
        #                 'borderWidth': '1px',
        #                 'borderStyle': 'dashed',
        #                 'borderRadius': '5px',
        #                 'textAlign': 'center',
        #                 'margin': '10px'
        #             },
        #             multiple=True  # Allow multiple files to be uploaded
        #         ),
        #         html.Div(id='output-upload'),
        #         html.H4('Suppression de données'),
        #         dcc.DatePickerSingle(
        #             id='date-picker-delete',
        #             date=None,
        #             display_format='DD.MM.YYYY',
        #             min_date_allowed=min(fetch_timedata_dates()),
        #             max_date_allowed=max(fetch_timedata_dates()),
        #             disabled_days=[pd.to_datetime(date).date() for date in
        #                            pd.date_range(start=min(fetch_timedata_dates()),
        #                                          end=max(fetch_timedata_dates())).
        #                            difference(pd.to_datetime(fetch_timedata_dates()))]
        #         ),
        #         html.Button('Supprimer les données', id='delete-button', n_clicks=0),
        #         html.Div(id='output-delete')
        #     ])
        # elif tab == 'subtab-showDB':
        #     df = fetch_timedata()
        #     if picked_date:
        #         picked_df = fetch_timedata(picked_date)
        #     else:
        #         picked_df = pd.DataFrame(columns=["Aucun jour sélectionné"])
        #     # Convertir les données en tableau interactif DataTable
        #     data_table_all = dash_table.DataTable(
        #         data=df.to_dict('records'),
        #         columns=[{'name': col, 'id': col} for col in df.columns],
        #         page_size=10,
        #         style_table={'overflowX': 'auto'},
        #         style_cell={'textAlign': 'left'},
        #         style_header={
        #             'backgroundColor': 'rgb(230, 230, 230)',
        #             'fontWeight': 'bold'
        #         }
        #     )
        #     data_table_selected = dash_table.DataTable(
        #         data=picked_df.to_dict('records'),
        #         columns=[{'name': col, 'id': col} for col in picked_df.columns],
        #         page_size=10,
        #         style_table={'overflowX': 'auto'},
        #         style_cell={'textAlign': 'left'},
        #         style_header={
        #             'backgroundColor': 'rgb(230, 230, 230)',
        #             'fontWeight': 'bold'
        #         }
        #     )
        #     # Nouvelle section pour afficher le nombre de jours disponibles
        #     all_entries = fetch_timedata_dates()
        #     num_entries = len(all_entries)
        #     print(all_entries[0])
        #     all_days = set([datetime.strptime(x,
        #                                       '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for
        #                     x in all_entries])
        #
        #     num_days = len(all_days)
        #     nb_entries = html.Div([
        #         html.H6(f'Nombre d\'entrées dans la base de données : {num_entries}')
        #     ])
        #     nb_days = html.Div([
        #         html.H6(f'Nombre de jours dans la base de données : {num_days}')
        #     ])
        #     return html.Div([
        #         html.Div(id='datepicker-container'),
        #         html.H3('Données pour le jour sélectionné'),
        #         data_table_selected,
        #         html.H3('Aperçu de la base de données'),
        #         data_table_all,
        #         nb_entries,
        #         nb_days
        #     ])