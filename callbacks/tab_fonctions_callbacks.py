from dash.dependencies import Input, Output
from settings import *
from utils_fcts import *

def register_callbacks(app):

    ################################################################################################
    ################################ CALLBACKS SUBTAB PAR FONCTION
    ################################################################################################
    # Définir les callbacks pour mettre à jour le contenu des sous-onglets
    @app.callback(Output('subtabs-fonctions-content', 'children'),
                  [Input('subtabs-fonctions', 'value')])
    def render_subtab_fonctions_content(subtab):
        if subtab == 'subtab-batterie':
            return html.Div([
                html.H4("Données sur la batterie"),
                get_period_dropdown('subbat-period-dropdown'),
                html.Button('Afficher', id='show-batterie-btn', n_clicks=0),
                html.Div(id='subbat-range-info', style={'marginTop': '20px'}),
                html.Div(id='subtab-batterie-content', style={'marginTop': '20px'}),
            ])


    ######################################################################
    # graphes batterie
    ######################################################################
    @app.callback(
        [Output('subtab-batterie-content', 'children'),
         Output('confirm-dialog-subbat', 'displayed'),
         Output('confirm-dialog-subbat', 'message'),
         Output('subbat-range-info', 'children')],
        [Input('show-batterie-btn', 'n_clicks')],
        [
            State('range-picker-subbat', 'start_date'),
            State('range-picker-subbat', 'end_date'),
            State('subbat-period-dropdown', 'value')]
    )
    def display_batterie_graph(n_clicks ,start_date, end_date, selected_period):
        selected_db = dbTime_name
        selected_col = "FOO"

        if n_clicks is None or n_clicks == 0:
            return ["", False, "", ""]

        if selected_period == "stat_all":
            query = get_query_extractInterval(selected_db, None, None)
        else :
            if (not selected_db or not selected_col) and (not start_date or not end_date):
                return ["", True, "Sélectionnez des données et une période", ""]

            if not selected_db or not selected_col :
                return [ "", True, "Sélectionnez des données", ""]

            if not start_date or not end_date:
                return ["", True, "Sélectionnez une période", ""]

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if selected_period in ['stat_day', 'stat_week', 'stat_month', 'stat_year']:
                if start_date != end_date:
                    return ["ERREUR", True, "Choisir une seule date de début et fin", ""]
                start_date = get_startrange_date(end_date, selected_period)

            if selected_period == 'stat_perso' and start_date == end_date:
                return ["ERREUR", True, "Choisir une date différente", ""]

            query = get_query_extractInterval(selected_db, start_date, end_date)

        date_info = f"Données du {start_date} au {end_date}"


        conn = sqlite3.connect(db_file)

        # query = f"SELECT {db_daycol}, {selected_col} FROM {selected_db} WHERE {db_daycol} >= '{start_date}' AND {db_daycol} <= '{end_date}'"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if selected_db == dbTime_name:
            xcol = db_timecol
        else:
            xcol = db_daycol
            if selected_db == dbDayI_name:
                for col in dayI_cols:
                    df[col] = df[col + "_1"].fillna(0) + df[col + "_2"].fillna(0)


        div_container = []
        ##** GRAPHE 1 - minute

        plot1 = get_dbTime_2vargraph(df=df, xcol=db_timecol ,col1="XT_Ubat_Vdc_I3092_L1_1",
                                     col2="XT_Ubat_Vdc_I3092_L2_2",
                                     dbName = dbTime_name,
                                     settingsdict=showcols_settings)
        div_container.append(dcc.Graph(id='graph-battrie-XTubat', figure=plot1[0],config= {
                                        'scrollZoom': True  # Activer le zoom avec la molette
                                    }))
        div_container.append(dcc.Markdown(plot1[1],
                                          dangerously_allow_html=True))

        ##** GRAPHE 2 - jours
        selected_db = dbDayI_name
        queryI = get_query_extractInterval(selected_db, start_date, end_date)
        conn = sqlite3.connect(db_file)
        print(queryI)
        dayI_df = pd.read_sql_query(queryI, conn)
        conn.close()
        print(" nrow " + str(dayI_df.shape[0]))
        print('show first days dayI: ' + ','.join(dayI_df['day']))
        IvarsVT_toplot = ["I7007_1" ,"I7008_1"]
        dayI_df = dayI_df[[db_daycol ] +IvarsVT_toplot]

        plot3= get_dbTime_2vargraph(dayI_df, db_daycol ,col1=IvarsVT_toplot[0],
                                    col2 = IvarsVT_toplot[1],
                                    dbName = dbDayI_name)
        div_container.append(dcc.Graph(id='graph-batterie_dayI', figure=plot3[0],config= {
                                        'scrollZoom': True  # Activer le zoom avec la molette
                                    }))
        div_container.append(dcc.Markdown(plot3[1],
                                          dangerously_allow_html=True))

        return [div_container, False, "", date_info]

