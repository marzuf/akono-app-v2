
row1="v7.6;XT-Ubat- (MIN) [Vdc];;XT-Uin [Vac];;XT-Iin [Aac];;XT-Pout [kVA];;XT-Pout+ [kVA];;XT-Fout [Hz];;XT-Fin [Hz];;XT-Phase [];;XT-Mode [];;XT-Transfert [];;XT-E CMD [];;XT-Aux 1 [];;XT-Aux 2 [];;XT-Ubat [Vdc];;XT-Ibat [Adc];;XT-Pin a [kW];;XT-Pout a [kW];;XT-Tp1+ (MAX) [°C];;BSP-Ubat [Vdc];BSP-Ibat [Adc];BSP-SOC [%];BSP-Tbat [°C];Solar power (ALL) [kW];DEV XT-DBG1 [];DEV BSP-locE [];DEV SYS MSG;DEV SYS SCOM ERR;"
row2=";I3090;I3090;I3113;I3113;I3116;I3116;I3098;I3098;I3097;I3097;I3110;I3110;I3122;I3122;I3010;I3010;I3028;I3028;I3020;I3020;I3086;I3086;I3054;I3054;I3055;I3055;I3092;I3092;I3095;I3095;I3119;I3119;I3101;I3101;I3103;I3103;I7030;I7031;I7032;I7033;I17999;I3140;I7059;I17997;I17998;"
row3=";L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1;L2;L1-1;L2-2;L1-1;L2-2;L1-1;L2-2;L1-1;L2-2;L1-1;L2-2;1;1;1;1;ALL;1;1;1;1;"
row4="15.12.2023 00:00;50.19;50.12;0;0;0;0;0.29;0.12;0.29;0.12;50.00;50.00;0;0;4;4;1;1;0;0;0;1;0;0;1;1;50.12;50.00;-3.00;-2.00;-0.00;-0.00;0.14;0.05;42.00;40.00;50.31;-4.73;83.06;28.00;0;61440.00;0;;0;;"

row1.count(";")
row2.count(";")
row3.count(";")
row4.count(";")

dcc.DatePickerRange(
    id='range-picker-daydata',
    # date=None,
    display_format='DD.MM.YYYY',
    min_date_allowed=min(fetch_dayPdata_dates(dbDayP_name)),
    max_date_allowed=max(fetch_dayPdata_dates(dbDayP_name)),
    minimum_nights=0,
    disabled_days=[pd.to_datetime(date).date() for date in
                   pd.date_range(start=min(fetch_dayPdata_dates(dbDayP_name)),
                                 end=max(fetch_dayPdata_dates(dbDayP_name))).
                   difference(pd.to_datetime(fetch_dayPdata_dates(dbDayP_name)))],
    style={'display': 'none'}  # Initialement caché
    # attention : pd.date_range(...).retourne un DatetimeIndex
    # pd.to_datetime pour convertir all_dates aussi en DatetimeIndex pr comparer
),
dcc.DatePickerRange(
    id='range-picker-stat',
    # date=None,
    display_format='DD.MM.YYYY',  ## prend les dates seulement dayP -> assume partt les mm !!
    min_date_allowed=min(fetch_dayPdata_dates(dbDayP_name)),
    max_date_allowed=max(fetch_dayPdata_dates(dbDayP_name)),
    disabled_days=[pd.to_datetime(date).date() for date in
                   pd.date_range(start=min(fetch_dayPdata_dates(dbDayP_name)),
                                 end=max(fetch_dayPdata_dates(dbDayP_name))).
                   difference(pd.to_datetime(fetch_dayPdata_dates(dbDayP_name)))],
    minimum_nights=0,
    style={'display': 'none'}  # Initialement caché
),
get_range_picker('range-picker-evotime'),
# dcc.DatePickerRange(
#     id='range-picker-evotime',
#     # date=None,
#     display_format='DD.MM.YYYY',  ## prend les dates seulement dayP -> assume partt les mm !!
#     min_date_allowed=min(fetch_dayPdata_dates(dbDayP_name)),
#     max_date_allowed=max(fetch_dayPdata_dates(dbDayP_name)),
#     disabled_days=[pd.to_datetime(date).date() for date in
#                    pd.date_range(start=min(fetch_dayPdata_dates(dbDayP_name)),
#                                  end=max(fetch_dayPdata_dates(dbDayP_name))).
#                    difference(pd.to_datetime(fetch_dayPdata_dates(dbDayP_name)))],
#     minimum_nights=0,
#     style={'display': 'none'}  # Initialement caché
# ),
dcc.DatePickerRange(
    id='range-picker-analyseGraph',
    # date=None,
    display_format='DD.MM.YYYY',  ## prend les dates seulement dayP -> assume partt les mm !!
    min_date_allowed=min(fetch_dayPdata_dates(dbDayP_name)),
    max_date_allowed=max(fetch_dayPdata_dates(dbDayP_name)),
    disabled_days=[pd.to_datetime(date).date() for date in
                   pd.date_range(start=min(fetch_dayPdata_dates(dbDayP_name)),
                                 end=max(fetch_dayPdata_dates(dbDayP_name))).
                   difference(pd.to_datetime(fetch_dayPdata_dates(dbDayP_name)))],
    minimum_nights=0,
    style={'display': 'none'}  # Initialement caché
),

dcc.ConfirmDialog(
    id='confirm-dialog-evotime',
    message=''
),
dcc.ConfirmDialog(
    id='confirm-dialog-evoTimeDBgraph',
    message=''
),
dcc.ConfirmDialog(
    id='confirm-dialog-evoDayIDBgraph',
    message=''
),
dcc.ConfirmDialog(
    id='confirm-dialog-evoDayPDBgraph',
    message=''
),
# dcc.ConfirmDialog(
#     id='confirm-dialog-stat',
#     message=''
# ), dcc.ConfirmDialog(
#     id='confirm-dialog-statgraph',
#     message=''
# ),
dcc.ConfirmDialog(
    id='confirm-dialog-analyseGraph',
    message=''
), dcc.ConfirmDialog(
    id='confirm-dialog-daydataP',
    message=popupmsg_maxvar
), dcc.ConfirmDialog(
    id='confirm-dialog-daydataI',
    message=popupmsg_maxvar
)] + all_confirm_dialogs

# df[col2] = df[col2] - 51
#
# ## remplacer les 0
# minval0 = min(np.min(df.loc[df['source'] != 'Absence de source', col]),
#     np.min(df.loc[df['source2'] != 'Absence de source', col2]))
#
# df.loc[df['source'] == 'Absence de source', col] =  minval0-2
# df.loc[df['source2'] == 'Absence de source', col2] =  minval0-2
#
# fig = go.Figure()
#
# colors = {'Réseau': 'blue', 'Génératrice': 'green', 'Absence de source': 'red', 'Autre': 'grey'}
#
# for source, color in colors.items():
#     source_df = df[df['source'] == source]
#     fig.add_trace(go.Bar(
#         x=source_df['time'],
#         y=source_df[col],
#         marker=dict(color=color),
#         name=f'{source} {col}',
#         offsetgroup=0
#     ))
#
# for source, color in colors.items():
#     source2_df = df[df['source2'] == source]
#     fig.add_trace(go.Bar(
#         x=source2_df['time'],
#         y=source2_df[col2],
#         marker=dict(color=color, pattern_shape="x"),
#         name=f'{source} {col2}',
#         offsetgroup=1
#     ))
# # Déterminer les limites de l'axe y
# y_min = min(df[col].min(), df[col2].min())
# y_max = max(df[col].max(), df[col2].max())
# # Créer un intervalle régulier
# tickvals = np.arange(y_min, y_max + 1, 10)
# ticktext = tickvals + 51
# # fig.update_yaxes(zeroline=True, zerolinecolor='black', zerolinewidth=2, range=[-52, 52])
# # fig.update_layout(yaxis=dict(tickvals=[-50, -25, 0, 25, 50], ticktext=[1, 26, 51, 76, 101]))
#
#
# fig.update_layout(
#     title='Sources de xtfin à travers le temps',
#     xaxis=dict(title='Temps'),
#     yaxis=dict(title='xtfin', zeroline=True, zerolinewidth=2, zerolinecolor='black', tickvals=tickvals, ticktext=ticktext),
#     barmode='group',
#     legend_title='Source',
#     hovermode='x unified'
# )
# for source in sources:
#     source_df = df[df['source'] == source]
#     fig.add_trace(go.Scatter(
#         x=source_df['time'], y=source_df[col],
#         mode='lines', line=dict(color=colors[source], width=4),
#         name=source
#     ))
#
# fig.update_layout(
#     title='Sources de xtfin à travers le temps',
#     xaxis_title='Temps',
#     yaxis_title='xtfin',
#     legend_title='Source',
#     hovermode='x unified'
# )
# div_container.append(dcc.Graph(id='graph-XT_Fin', figure=fig))

# if selected_db == dbTime_name and selected_viz == 'boxplot':
#     df['date'] = pd.to_datetime(df[xcol]).dt.date
#     fig = px.box(df, x='date', y=selected_col, title=f'{selected_col} Box Plot par jour')
# else:
#     if selected_viz == 'lineplot':
#         fig = px.line(df, x=xcol, y=selected_col, title=f'{selected_col} Line Plot')
#     elif selected_viz == 'barplot':
#         fig = px.bar(df, x=xcol, y=selected_col, title=f'{selected_col} Bar Plot')
#     elif selected_viz == 'boxplot':
#         fig = px.box(df, x=xcol, y=selected_col, title=f'{selected_col} Box Plot')
#
# if (selected_db == dbTime_name and selected_viz == 'boxplot') or (
#         selected_db == dbDayP_name or selected_db == dbDayI_name):
#     fig.update_layout(xaxis=dict(title='Date', tickformat='%Y-%m-%d', dtick="D1"))

# legend_shown = {source: False for source in colors.keys()}
#
# for source, color in colors.items():
#     source_df = df[df['source'] == source]
#     for i, row in source_df.iterrows():
#         show_legend = not legend_shown[source] and i == 0
#         if source in ['Incertain', 'Absence de source']:
#             yvals = [-row[col1], row[col1]]
#         elif source =="Réseau" :
#             yvals = [0, row[col1]]
#         elif source == "Génératrice":
#             yvals = [0, -row[col1]]
#         else :
#             exit(1)
#         figBarMin.add_trace(go.Scatter(
#             x=[row['time'], row['time']],
#             y=yvals, #[0, row[col]],
#             mode='lines',
#             line=dict(color=color, width=2),
#             name=f'{source} {col1}' if show_legend else '',
#             showlegend=show_legend
#         ))
#     legend_shown[source] = True
#
# legend_shown = {source: False for source in colors.keys()}
# for source, color in colors.items():
#     source2_df = df[df['source2'] == source]
#     for i, row in source2_df.iterrows():
#         show_legend = not legend_shown[source] and i == 0
#         if source in ['Incertain', 'Absence de source']:
#             yvals2 = [-row[col2], row[col2]]
#         elif source =="Réseau" :
#             yvals2 = [0, row[col2]]
#         elif source == "Génératrice":
#             yvals2 = [0, -row[col2]]
#         else:
#             exit(1)
#
#         figBarMin.add_trace(go.Scatter(
#             x=[row['time'], row['time']],
#             y=yvals2,#[0, row[col2]],
#             mode='lines',
#             line=dict(color=color, width=2, dash='dot'),
#             name=f'{source} {col2}' if show_legend else '',
#             showlegend=show_legend
#         ))
#     legend_shown[source] = True
#
# figBarMin.update_layout(
#     title='Sources de xtfin à travers le temps',
#     xaxis=dict(title='Temps'),
#     yaxis=dict(title='xtfin', zeroline=True),
#     legend_title='Source',
#     hovermode='x unified'
# )

# # row = data.iloc[0]
# for i, row in data.iterrows():
#     day = row['day']#.strftime('%d.%m.%Y')
#     i3081 = row['I3081']
#     i3083 = row['I3083']
#     min_val = min(i3081, i3083)
#
#     fig.add_trace(go.Bar(
#         x=[day],
#         y=[min_val],
#         marker_color='grey',
#         showlegend=False,
#         name='I3083 min'
#     ))
#
#     fig.add_trace(go.Bar(
#         x=[day],
#         y=[-i3083 + min_val],
#         base=[-i3083],
#         marker_color='red',
#         showlegend=False,
#         name='I3083'
#     ))
#
#     fig.add_trace(go.Bar(
#         x=[day],
#         y=[min_val],
#         marker_color='grey',
#         showlegend=False,
#         name='I3081 min'
#     ))
#
#     fig.add_trace(go.Bar(
#         x=[day],
#         y=[i3081 - min_val],
#         base=[min_val],
#         marker_color='green',
#         showlegend=False,
#         name='I3081'
#     ))
#
# fig.update_layout(
#     title='Comparaison des valeurs I3081 et I3083 par jour',
#     xaxis=dict(title='Jour'),
#     yaxis=dict(title='Valeurs (somme L1+L2)'),
#     barmode='relative',
#     showlegend=False,
#     hovermode='x unified'
# )
# # fig = go.Figure()
# #
# # print('show first days : ' + ','.join(sumI_df.day))
# #
# # fig = px.bar(sumI_df, x='day', y='I3081',
# #              title='I3081 Bar Plot')

# fig.show()
#
#
# fig = go.Figure()
# fig.add_trace(go.Bar(
#     y=-sumI_df['I3081'],
#     x=sumI_df['day'],
#     # orientation='h',
#     name='I3081',
#     marker_color='green'
# ))
# fig.add_trace(go.Bar(
#     y=sumI_df['I3083'],  # Valeurs positives pour partir à droite
#     x=sumI_df['day'],
#     # orientation='h',
#     name='I3083',
#     marker_color='red'
# ))
#
# fig.update_layout(
#     title='Comparaison des valeurs I3081 et I3083 par jour',
#     yaxis=dict(title='Valeurs (somme L1+L2)'),
#     xaxis=dict(title='Jour'),
#     # barmode='relative',
#     hovermode='x unified'
# )

# col1_txt = showcols_settings[col1]['description']
# col2_txt = showcols_settings[col2]['description']
# if htmlFormat:
#     if col1_txt == col2_txt :
#         fig_desc = "<u>" + col1 + "</u> et  <u>" + col2 + "</u> : " + col2_txt
#     else :
#         col1_desc = "<u>" + col1 + "</u> : " + col1_txt
#         col2_desc = "<u>" + col2 + "</u> : " + col2_txt
#         fig_desc = col1_desc + "<br>" + col2_desc
# else :
#     if col1_txt == col2_txt :
#         fig_desc = col1 + " et " + col2 +  " : " + col2_txt
#     else :
#         col1_desc = col1 + " : " + col1_txt
#         col2_desc = col2 + " : " + col2_txt
#         fig_desc = col1_desc + "\n" + col2_desc

# # Reshape le DataFrame en long format
# dayI_df_long = dayI_df.melt(id_vars=['day'],
#                             value_vars=IvarBSP_toplot,
#                             var_name='variable', value_name='value')
# colors = {'green': IvarBSP_toplot[0], 'red': IvarBSP_toplot[1]}
# ## grpahe 4
# plot4= get_dbTime_2vargraph(dayI_df, db_daycol,col1=IvarBSP_toplot[0],
#                             col2 = IvarBSP_toplot[1],
#                             dbName = dbDayI_name)
# #div_container.append(dcc.Graph(id='graph-BSP_dayIprod', figure=plot4[0]))
# div_container.append(dcc.Markdown(plot4[1],
#                                   dangerously_allow_html=True))

# Modal structure
# div_container.append(
#     html.Div(
#         id="graph-modal",
#         style={"display": "none"},
#         children=[
#             html.Div(
#                 id="modal-content",
#                 children=[
#                     html.Button("Close", id="close-modal", n_clicks=0),
#                     dcc.Graph(id="modal-graph")
#                 ],
#                 style={
#                     "position": "fixed",
#                     "top": "50%",
#                     "left": "50%",
#                     "transform": "translate(-50%, -50%)",
#                     "background-color": "white",
#                     "padding": "20px",
#                     "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.5)",
#                     "z-index": "1000",
#                     "width": "80%",
#                     "height": "80%",
#                     "overflow": "auto"
#                 }
#             ),
#             html.Div(
#                 style={
#                     "position": "fixed",
#                     "top": "0",
#                     "left": "0",
#                     "width": "100%",
#                     "height": "100%",
#                     "background-color": "rgba(0, 0, 0, 0.5)",
#                     "z-index": "999"
#                 }
#             )
#         ]
#     )
# )




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


# @app.callback(
#     Output('tabs-example', 'value'),
#     [Input('btn-dashboard', 'n_clicks'),
#      Input('btn-evotime', 'n_clicks'),
#      Input('btn-stat', 'n_clicks'),
#      Input('btn-analyseGraph', 'n_clicks'),
#      Input('btn-appareils', 'n_clicks'),
#      Input('btn-variotrack', 'n_clicks'),
#      Input('btn-fonctions', 'n_clicks'),
#      Input('btn-data', 'n_clicks')]
# )
# def navigate_to_tabs(*_):
#     ctx = dash.callback_context
#     print("navigate to tabs")
#     if not ctx.triggered:
#         return 'tab-accueil'
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#         print(button_id)
#         if button_id == 'btn-dashboard':
#             return 'tab-dashboard'
#         elif button_id == 'btn-evotime':
#             return 'tab-evotime'
#         elif button_id == 'btn-stat':
#             return 'tab-stat'
#         elif button_id == 'btn-analyseGraph':
#             return 'tab-analyseGraph'
#         elif button_id == 'btn-appareils' or button_id == 'btn-variotrack':
#             return 'tab-appareils'
#         elif button_id == 'btn-fonctions':
#             return 'tab-fonctions'
#         elif button_id == 'btn-data':
#             return 'tab-data'
#     return 'tab-accueil'
#
#
# @app.callback(
#     Output('subtabs-appareils', 'value'),
#     [Input('btn-variotrack', 'n_clicks')]
# )
# def navigate_to_subtab_variotrack(btn_variotrack):
#     if btn_variotrack:
#         return 'subtab-variotrack'
#     return 'subtab-bsp'  # Valeur par défaut
#
#
# # Callback pour gérer la navigation vers le sous-onglet "Export" quand on clique sur "Export" dans le texte
# @app.callback(
#     [Output('tabs-example', 'value'),
#      Output('subtabs-data', 'value')],
#     [Input('markdown-data', 'n_clicks')],
#     [dash.dependencies.State('tabs-example', 'value')]
# )
# def navigate_to_export(n_clicks, current_tab):
#     if n_clicks:
#         return 'tab-data', 'subtab-exportDB'  # Naviguer vers l'onglet "Données" et le sous-onglet "Exporter des données"
#     return current_tab, 'subtab-updateDB'
#

        # Onglet Accueil
        # dcc.Tab(label='Accueil', value='tab-accueil',
        #         className='mytab', selected_className='mytab-slctd',
        #         children=[
        #             html.Div([
        #                 html.H3("Bienvenue sur le tableau de bord"),
        #                 html.Div([
        # dcc.Markdown("Le dashboard donne une vue d'ensemble du contenu de la base de données et des données disponibles. " +
        #              "On peut cliquer sur chacune des variables pour voir la tendance dans le temps.",
        #                                dangerously_allow_html=True),
        # dbc.Button("Dashboard", id="btn-dashboard", color="primary", className="mr-2"),
        # dbc.Button("Évolution temporelle", id="btn-evotime", color="primary", className="mr-2"),
        # dbc.Button("Statistiques", id="btn-stat", color="primary", className="mr-2"),
        # dbc.Button("Analyse (Graphes)", id="btn-analyseGraph", color="primary", className="mr-2"),
        # dcc.Markdown("L'onglet 'Par appareil' permet d'afficher les différentes variables pour chacun des appareils. ",
        #                                dangerously_allow_html=True),
        # dbc.Button("Par appareil", id="btn-appareils", color="primary", className="mr-2"),
        # dbc.Button("VarioTrack", id="btn-variotrack", color="primary", className="mr-2"),
        # dbc.Button("Par fonction", id="btn-fonctions", color="primary", className="mr-2"),
        # dcc.Markdown("L'onglet 'Données' contient plusieurs sous-onglets qui permettent de voir un aperçu des tables de la base de données, "+
        #              "d'ajouter ou supprimer des données de la base de données ou d'exporter des données en fichiers Excel.",
        #                                dangerously_allow_html=True),
        #
        # dbc.Button("Données", id="btn-data", color="primary", className="mr-2")
        #                 ], className="d-flex justify-content-center")
        #             ])
        #         ]),


# dcc.Tab(label='Accueil', value='tab-accueil',
#         className='mytab', selected_className='mytab-slctd',
#         children=[
#             html.Div([
#                 html.H1("Bienvenue sur le tableau de bord", className='title'),
#                 html.Div([
#                     html.P("Le dashboard donne une vue d'ensemble du contenu de la base de données et des données disponibles. " +
#                            "On peut cliquer sur chacune des variables pour voir la tendance dans le temps.",
#                            className='description'),
#                     dbc.Button("Dashboard", id="btn-dashboard", color="primary", className="mr-2"),
#                     dbc.Button("Évolution temporelle", id="btn-evotime", color="primary", className="mr-2"),
#                     dbc.Button("Statistiques", id="btn-stat", color="primary", className="mr-2"),
#                     dbc.Button("Analyse (Graphes)", id="btn-analyseGraph", color="primary", className="mr-2"),
#                 ], className="section"),
#                 html.Div([
#                     html.P("L'onglet 'Par appareil' permet d'afficher les différentes variables pour chacun des appareils.",
#                            className='description'),
#                     dbc.Button("Par appareil", id="btn-appareils", color="primary", className="mr-2"),
#                     dbc.Button("VarioTrack", id="btn-variotrack", color="primary", className="mr-2"),
#                     dbc.Button("Par fonction", id="btn-fonctions", color="primary", className="mr-2"),
#                 ], className="section"),
#                 html.Div([
#                     html.P("L'onglet 'Données' contient plusieurs sous-onglets qui permettent de voir un aperçu des tables de la base de données, " +
#                            "d'ajouter ou supprimer des données de la base de données ou d'exporter des données en fichiers Excel.",
#                            className='description'),
#                     dbc.Button("Données", id="btn-data", color="primary", className="mr-2"),
#                 ], className="section"),
#             ], className="container")
#         ]),
#     dcc.Markdown("""
#         **Par fonction** : Visualisez les données en fonction de leur utilisation dans le système.
#     """),
#     dbc.Button("Par fonction", id="landpage-btn-fonctions",
#                style={'backgroundColor': '#2507cf', 'color': 'white'},
#                className="my-2"),
# ], width=4),
