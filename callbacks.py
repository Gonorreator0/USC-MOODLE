from dash import Input, Output, State, dash_table, html
import pandas as pd
import io
import base64
import plotly.express as px

def register_callbacks(app):
    @app.callback(
        [
            Output("file-info", "children"),
            Output("data-table", "children"),
            Output("tiempo-graph", "figure"),
            Output("completitud-graph", "figure"),
            Output("notas-graph", "figure"),
            Output("alerts", "children"),
            Output("download-report", "data"),
        ],
        [
            Input("upload-data", "contents"),
            Input("generate-report", "n_clicks"),
        ],
        [State("upload-data", "filename")],
    )
    def update_output(contents, n_clicks, filename):
        # Si no hay contenido cargado, muestra un mensaje inicial
        if contents is None:
            return "No se ha cargado ningún archivo", None, {}, {}, {}, "", None

        try:
            # Leer archivo CSV solo si se sube un archivo
            content_type, content_string = contents.split(",")
            decoded = pd.read_csv(
                io.StringIO(base64.b64decode(content_string).decode("utf-8")),
                delimiter=";",
                encoding="utf-8",
            )

            # Mostrar información del archivo cargado
            info = f"Archivo cargado: {filename}"

            # Procesar calificaciones
            if "Calificación" in decoded.columns:
                decoded["Calificación"] = pd.to_numeric(
                    decoded["Calificación"]
                    .astype(str)
                    .str.replace(",", ".")
                    .str.strip(),
                    errors="coerce"
                ).fillna(0)

            # Crear tabla
            table = dash_table.DataTable(
                data=decoded.to_dict("records"),
                columns=[{"name": i, "id": i} for i in decoded.columns],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "5px"},
            )

            # Análisis y gráficos
            tiempo_promedio = decoded.groupby("Estudiante")["Tiempo de Permanencia (min)"].mean().reset_index()
            tasa_completitud = (
                decoded.groupby("Estudiante")["Tarea Completada"]
                .apply(lambda x: (x == "Sí").mean() * 100 if len(x) > 0 else 0)
                .reset_index()
            )
            tasa_completitud.columns = ["Estudiante", "Tasa de Completitud (%)"]

            promedios_notas = decoded.groupby("Estudiante").agg({"Calificación": "mean"}).reset_index()

            # Gráficas
            tiempo_fig = px.bar(
                tiempo_promedio,
                x="Estudiante",
                y="Tiempo de Permanencia (min)",
                title="Tiempo Promedio de Permanencia por Estudiante",
                color_discrete_sequence=["#003366"],
            )

            completitud_fig = px.bar(
                tasa_completitud,
                x="Estudiante",
                y="Tasa de Completitud (%)",
                title="Tasa de Completitud de Tareas",
                color_discrete_sequence=["#003366"],
            )

            notas_fig = px.bar(
                promedios_notas,
                x="Estudiante",
                y="Calificación",
                title="Promedio de Calificaciones por Estudiante",
                color_discrete_sequence=["#003366"],
            )

            # Estudiantes con calificaciones bajas
            estudiantes_bajos = promedios_notas[promedios_notas["Calificación"] < 3.0]
            report_data = estudiantes_bajos.to_csv(index=False, encoding="utf-8")

            # Alertas
            alertas = html.Ul(
    [
        html.Li(
            f"{row['Estudiante']} tiene un promedio bajo: {row['Calificación']:.2f}",
            className="alerta-promedio-bajo"
        )
        for _, row in estudiantes_bajos.iterrows()
    ]
)
            # Generar reporte solo si el botón es presionado
            if n_clicks and n_clicks > 0:
                report = {"content": report_data, "filename": "reporte_calificaciones_bajas.csv"}
            else:
                report = None

            return info, table, tiempo_fig, completitud_fig, notas_fig, alertas, report

        except Exception as e:
            return f"Error al procesar el archivo: {e}", None, {}, {}, {}, "", None
