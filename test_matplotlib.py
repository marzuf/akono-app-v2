from io import BytesIO
import matplotlib.pyplot as plt

# Convert the 'day' column to datetime format
df['day'] = pd.to_datetime(df['day'])
df.set_index('day', inplace=True)

x = df.index
y1 = df['I7007_1']
y2 = df['I7008_1']

# Création de la figure
plotly_fig, ax = plt.subplots(figsize=(10, 6))

# Tracer les lignes
ax.plot(x, y1, label='I7007_1', color='blue')
ax.plot(x, y2, label='I7008_1', color='red')

# Remplir les zones entre les courbes
ax.fill_between(x, y1, y2, where=(y2 >= y1), facecolor='green', alpha=0.3, interpolate=True)
ax.fill_between(x, y1, y2, where=(y2 <= y1), facecolor='red', alpha=0.3, interpolate=True)

# Ajouter le titre et les légendes
ax.set_title('Fill Between with Interpolation')
ax.legend(loc='upper left')

buffer = BytesIO()
plotly_fig.savefig(buffer, format='png')
buffer.seek(0)

image_string = base64.b64encode(buffer.getvalue()).decode()
div_container.append(html.Div([
    html.Img(src='data:image/png;base64,' + image_string)
]))
