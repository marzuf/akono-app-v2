fig = go.Figure()

# Ajout des barres pour I3081 (vers la gauche, en vert)
fig.add_trace(go.Bar(
    x=-sumI_df['I3081'],  # Valeurs négatives pour partir à gauche
    y=sumI_df['day'],
    # orientation='h',
    name='I3081',
    marker_color='green'
))

# Ajout des barres pour I3083 (vers la droite, en rouge)
fig.add_trace(go.Bar(
    x=sumI_df['I3083'],  # Valeurs positives pour partir à droite
    y=sumI_df['day'],
    # orientation='h',
    name='I3083',
    marker_color='red'
))

fig.update_layout(
    title='Comparaison des valeurs I3081 et I3083 par jour',
    xaxis=dict(title='Valeurs'),
    yaxis=dict(title='Jour'),
    barmode='relative',
    hovermode='y unified'
)
fig.show()