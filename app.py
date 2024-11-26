import dash
from dash import html
from layout import create_layout
from callbacks import register_callbacks

# Inicializa la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"])
app.title = "Universidad Santiago de Cali"

# Configura el layout
app.layout = create_layout()

# Registra los callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
