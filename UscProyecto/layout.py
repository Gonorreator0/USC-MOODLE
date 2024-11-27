from dash import dcc, html

def create_layout():
    return html.Div(
        [
            # Barra superior
            html.Div(
                [
                    html.Img(src="/assets/logo.png", className="header-logo"),
                    html.Span("┃ Universidad Santiago de Cali", className="header-title"),
                ],
                className="header-bar",
            ),
            # Logo centrado
            html.Div(
                [
                    html.Img(src="/assets/logo-usc.webp", className="main-logo"),
                ],
                className="logo-container",
            ),
            # Área para subir archivo personalizada
            html.Div(
                [
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            [
                                html.Img(src="/assets/upload-icon.png", className="upload-icon"),
                                html.Span("Arrastra o haz clic para cargar un archivo CSV", className="upload-text"),
                            ]
                        ),
                        className="custom-upload-area",
                    ),
                    html.Div(id="file-info", className="file-info"),
                ],
                className="upload-section",
            ),
            # Botón para generar reportes
            html.Div(
                [
                    html.Button("Generar Reporte", id="generate-report", className="generate-button"),
                    dcc.Download(id="download-report"),
                ],
                style={"textAlign": "center", "marginBottom": "20px"},
            ),
            # Área de tabla
            html.Div(id="data-table", className="table-area"),
            # Área de gráficos con contexto
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Tiempo Promedio de Permanencia por Estudiante"),
                            html.P(
                                "Este análisis permite identificar qué estudiantes están dedicando menos tiempo a la plataforma. "
                                "Un tiempo reducido puede indicar falta de interés, problemas de acceso o dificultades con el contenido del curso."
                            ),
                            dcc.Graph(id="tiempo-graph"),
                        ],
                        className="graph-section",
                    ),
                    html.Div(
                        [
                            html.H3("Tasa de Completitud de Tareas"),
                            html.P(
                                "Esta gráfica muestra el porcentaje de tareas completadas por cada estudiante. "
                                "Una baja tasa de completitud puede sugerir problemas como falta de motivación o dificultades para comprender las instrucciones."
                            ),
                            dcc.Graph(id="completitud-graph"),
                        ],
                        className="graph-section",
                    ),
                    html.Div(
                        [
                            html.H3("Promedios de Notas"),
                            html.P(
                                "Esta gráfica muestra el promedio de calificaciones de los estudiantes. "
                                "Permite identificar tendencias de rendimiento académico y evaluar si los métodos de enseñanza están funcionando."
                            ),
                            dcc.Graph(id="notas-graph"),
                        ],
                        className="graph-section",
                    ),
                ],
                className="graph-area",
            ),
            # Área de alertas
            html.Div(id="alerts", className="alerts-section"),
        ]
    )
