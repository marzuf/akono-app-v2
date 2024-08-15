################################################################################################
################################ CALLBACKS - TAB DASHBOARD		tab-dashbOLD
################################################################################################


@app.callback(
    Output('dashboard-graph-varinfo', 'children'),
    [Input('dashboard-device-choice', 'value')]
)
def update_dashboardvarinfo(selected_device, selected_db=dbTime_name):
    if selected_device :
        desc_txt = selected_device
    else:
        return None
    return html.Div([dcc.Markdown(desc_txt,
                                  dangerously_allow_html=True)])


dcc.Tab(label='DashboardOLD', value='tab-dashbOLD',
        className='mytab', selected_className='mytab-slctd'),


# Callback pour afficher le graphique en fonction de la sélection :
@app.callback(
    [Output('dashboard-graph', 'figure'),
     Output('confirm-dialog-dashboard', 'displayed'),
     Output('confirm-dialog-dashboard', 'message'),
     Output('dashboard-range-info', 'children')],

    [Input('show-dashboard-btn', 'n_clicks')],
    [

        State('dashboard-device-choice', 'value'),
        State('range-picker-dashboard', 'start_date'),
        State('range-picker-dashboard', 'end_date'),
        State('dashboardperiod-dropdown', 'value')]
)
def display_dashboard_graph(n_clicks, selected_device,
                            start_date, end_date, selected_period):
    if selected_device == "XTender":
        selected_col = 'XT_Transfert_I3020_L2'
    else:
        selected_col = 'Solar_power_ALL_kW_I17999_ALL'
    selected_viz = 'lineplot'

    selected_db = dbTime_name
    if n_clicks is None or n_clicks == 0:
        return [go.Figure(), False, "", ""]
    if (not selected_db or not selected_col or not selected_viz) and (not start_date or not end_date):
        return [go.Figure(), True, "Sélectionnez des données et une période", "Sélectionnez des données et une période"]

    if not selected_db or not selected_col or not selected_viz:
        return [go.Figure(), True, "Sélectionnez des données", "Sélectionnez des données"]

    if selected_period == "stat_all":
        date_info = f"Toutes les données disponibles"
        query = get_query_extractInterval(selected_db, None, None)
    else:
        if not start_date or not end_date:
            return [go.Figure(), True, "Sélectionnez une période", "Sélectionnez une période"]

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
            if start_date != end_date:
                return ["ERREUR", True, "Choisir une seule date dans une modal pop-up", ""]
            start_date = get_startrange_date(end_date, selected_period)

        if selected_period == 'stat_perso' and start_date == end_date:
            return [go.Figure(), True, "Choisir une date différente", "Choisir une date différente"]

        date_info = f"Données du {start_date} au {end_date}"
        query = get_query_extractInterval(selected_db, start_date, end_date)

    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if selected_db == dbTime_name:
        xcol = db_timecol
    else:
        xcol = db_daycol
        if selected_db == dbDayI_name:
            for col in dayI_cols:
                df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)

    if selected_db == dbTime_name and selected_viz == 'boxplot':
        df['date'] = pd.to_datetime(df[xcol]).dt.date
        fig = px.box(df, x='date', y=selected_col, title=f'{selected_col} Box Plot par jour')
    else:
        if selected_viz == 'lineplot':
            fig = px.line(df, x=xcol, y=selected_col, title=f'{selected_col} Line Plot')
        elif selected_viz == 'barplot':
            fig = px.bar(df, x=xcol, y=selected_col, title=f'{selected_col} Bar Plot')
        elif selected_viz == 'boxplot':
            fig = px.box(df, x=xcol, y=selected_col, title=f'{selected_col} Box Plot')

    if (selected_db == dbTime_name and selected_viz == 'boxplot') or (
            selected_db == dbDayP_name or selected_db == dbDayI_name):
        fig.update_layout(xaxis=dict(title='Date', tickformat='%Y-%m-%d', dtick="D1"))
    return [fig, False, "", date_info]



    if tab == 'tab-dashbOLD':
        # return days_success_card_body
        # md = medium devices
        # md=4 signifie que cette colonne occupera 4 des 12 colonnes disponibles sur les
        return html.Div([
            html.H3('Contenu de la base de données'),
            get_period_dropdown('dashboardperiod-dropdown'),

            dcc.Dropdown(
                id='dashboard-device-choice',
                placeholder="Choisissez l'appareil",
                options=['XTender', 'VarioTrack']
            ),
            html.Div(id='dashboard-graph-varinfo', style={'marginTop': '20px'}),

            html.Button('Afficher', id='show-dashboard-btn', n_clicks=0),
            html.Div(id='dashboard-range-info', style={'marginTop': '20px'}),

            dcc.Graph(id='dashboard-graph'),
            dbc.Container(dbc.Row(dbc.Col([timeDB_card,
                            dayPDB_card, dayIDB_card], md=10)))
        ])


timeDB_card = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Contenu de la table des " + tabname2tablab[dbTime_name],
                            className="card-title"),
                    html.P(id='timeDB_content', className="card-text"),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-sun", style=card_icon),
            className="bg-warning",
            style={"maxWidth": 75},
        ),
    ],
    className="mt-4 shadow",
)

# Exemple de dayPDB_card ajoutée pour démonstration
dayPDB_card = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Contenu de la table des " + tabname2tablab[dbDayP_name],
                            className="card-title"),
                    html.P(id='dayPDB_content', className="card-text")
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-bolt", style=card_icon),
            className="bg-info",
            style={"maxWidth": 75},
        ),
    ],
    className="mt-4 shadow",
)

# Exemple de dayPDB_card ajoutée pour démonstration
dayIDB_card = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Contenu de la table des " + tabname2tablab[dbDayI_name],
                            className="card-title"),
                    html.P(id='dayIDB_content', className="card-text")
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-plug", style=card_icon),
            className="bg-success",
            style={"maxWidth": 75},
        ),
    ],
    className="mt-4 shadow",
)




# Callback to update the number of days in the database
@app.callback(
    Output('timeDB_content', 'children'),
    Output('dayIDB_content', 'children'),
    Output('dayPDB_content', 'children'),
    [Input('tabs-example', 'value')]
)
def update_days_count(tab):
    if tab == 'tab-dashbOLD':
        all_entries = fetch_timedata_dates()
        all_days = set([
            datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            for x in all_entries
        ])
        num_days = len(all_days)

        conn = sqlite3.connect(db_file)
        query = f"SELECT * FROM {dbDayI_name}"
        dayI_df = pd.read_sql_query(query, conn)
        conn.close()
        num_daysI = len(set(dayI_df[db_daycol]))
        all_entriesP = fetch_dayPdata_dates(dbDayP_name)

        num_daysP = len(all_entriesP)

        chargeTotal_dayI = round(dayI_df[ahCharge_dayIcol + "_1"].fillna(0).sum(), 2)
        dechargeTotal_dayI = round(dayI_df[ahDecharge_dayIcol + "_1"].fillna(0).sum(), 2)
        rendementTot_dayI = round(dechargeTotal_dayI / chargeTotal_dayI * 100, 2)
        nCycles = round(chargeTotal_dayI / 90)
        return (f'{num_days} jours',
                [f'{num_daysI} jours',
                 html.Br(),
                 html.B("Charge batterie total [Ah]"), " (" + ahCharge_dayIcol + ") :\t" + \
                 str(chargeTotal_dayI),
                 html.Br(),
                 html.B("Rendement batterie total [%]"), " (" + ahDecharge_dayIcol + "/" + \
                 ahCharge_dayIcol + ") :\t" + \
                 str(rendementTot_dayI) + " %",
                 html.Br(),
                 html.B("# Cycles"), " (" + ahCharge_dayIcol + "/90) :\t" + \
                 str(nCycles)],
                f'{num_daysP} jours')
    return [""] * 3