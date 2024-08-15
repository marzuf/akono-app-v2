# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('date-picker-dbdata', 'style'),
    [Input('tabs-example', 'value')]
)
def show_hide_timedatepicker(tab):
    if tab == 'tab-showDB':
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-evotime', 'style'),
    [Input('tabs-example', 'value')]
)
def show_hide_evotimedatepicker(tab):
    if tab == 'tab-evotime':
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-stat', 'style'),
    [Input('tabs-example', 'value')]
)
def show_hide_statdatepicker(tab):
    if tab == 'tab-stat':
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-dashboard', 'style'),
    [Input('tabs-example', 'value')]
)
def show_hide_dashboarddatepicker(tab):
    if tab == 'tab-dashbOLD':
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle



# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subxtender', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-appareils', 'value')]
)
def show_hide_subxtenderdatepicker(tab, subtab):
    if tab == 'tab-appareils' and subtab == "subtab-xtender":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subvariotrack', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-appareils', 'value')]
)
def show_hide_subvariotrackdatepicker(tab, subtab):
    if tab == 'tab-appareils' and subtab == "subtab-variotrack":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subbsp', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-appareils', 'value')]
)
def show_hide_subbspdatepicker(tab, subtab):
    if tab == 'tab-appareils' and subtab == "subtab-bsp":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle


# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subbat', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-fonctions', 'value')]
)
def show_hide_subbatdatepicker(tab, subtab):
    if tab == 'tab-fonctions' and subtab == "subtab-batterie":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subminutes', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-dashboard', 'value')]
)
def show_hide_subminutesdatepicker(tab, subtab):
    if tab == 'tab-dashboard' and subtab == "subtab-minutesdata":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle

# Callback pour mettre à jour la visibilité du DatePickerSingle
@app.callback(
    Output('range-picker-subdayI', 'style'),
    [Input('tabs-example', 'value'),
     Input('subtabs-dashboard', 'value')]
)
def show_hide_subdayIdatepicker(tab, subtab):
    if tab == 'tab-dashboard' and subtab == "subtab-dayIdata":
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerSingle
    else:
        return {'display': 'none'}  # Cacher le DatePickerSingle


# Callback pour mettre à jour la visibilité du DatePickerSingle
# Modifier le callback pour afficher/cacher le DatePickerRange
@app.callback(
    Output('range-picker-analyseGraph', 'style'),
    [Input('tabs-example', 'value')]
)
def show_hide_analyseGraph_datepicker(tab):
    if tab == 'tab-analyseGraph':
        return {'display': 'block', 'margin': '20px 0'}  # Afficher le DatePickerRange
    else:
        return {'display': 'none'}  # Cacher le DatePickerRange
