import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar o dataset
df = pd.read_csv("student_exam_scores.csv")

# Inicializar o aplicativo Dash com um tema escuro do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Esta linha expõe o servidor Flask subjacente para que o Gunicorn possa encontrá-lo.
server = app.server

# Estilos CSS personalizados para um visual mais sofisticado
# e para garantir que o texto das conclusões seja legível no tema escuro
CUSTOM_CSS = {
    "body": {
        "font-family": "Arial, sans-serif",
        "background-color": "#222222",
        "color": "#DDDDDD"
    },
    ".card-header": {
        "background-color": "#34495E",
        "color": "white",
        "font-size": "1.2em",
        "font-weight": "bold"
    },
    ".card-body": {
        "background-color": "#2C3E50",
        "color": "#DDDDDD"
    },
    ".metric-value": {
        "font-size": "2em",
        "font-weight": "bold",
        "color": "#2ECC71"
    },
    ".metric-label": {
        "font-size": "1em",
        "color": "#BBBBBB"
    },
    ".graph-conclusion": {
        "font-size": "0.95em",
        "margin-top": "10px",
        "padding": "10px",
        "background-color": "#34495E",
        "border-left": "5px solid #2E86C1",
        "color": "#EEEEEE"
    }
}

# Função para aplicar o tema escuro aos gráficos Plotly
def update_layout_dark(fig, title_text):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#2C3E50",
        paper_bgcolor="#2C3E50",
        font_color="#DDDDDD",
        title_font_color="#DDDDDD",
        title_text=title_text,
        title_x=0.5 # Centralizar o título
    )
    return fig

# --- Layout do Dashboard --- #
app.layout = dbc.Container(
    style=CUSTOM_CSS["body"],
    children=[
        html.H1("Dashboard de Análise de Desempenho de Estudantes",
                className="text-center my-4",
                style={
                    "color": "#2E86C1",
                    "font-size": "3em",
                    "font-weight": "bold"
                }),

        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Média da Nota do Exame", className="card-title", style=CUSTOM_CSS[".metric-label"]),
                    html.P(f"{df['exam_score'].mean():.2f}", className="card-text", style=CUSTOM_CSS[".metric-value"])
                ]),
                className="text-center m-2", style=CUSTOM_CSS[".card-body"]
            ), md=4),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Média de Horas de Estudo", className="card-title", style=CUSTOM_CSS[".metric-label"]),
                    html.P(f"{df['hours_studied'].mean():.2f}", className="card-text", style=CUSTOM_CSS[".metric-value"])
                ]),
                className="text-center m-2", style=CUSTOM_CSS[".card-body"]
            ), md=4),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Média de Horas de Sono", className="card-title", style=CUSTOM_CSS[".metric-label"]),
                    html.P(f"{df['sleep_hours'].mean():.2f}", className="card-text", style=CUSTOM_CSS[".metric-value"])
                ]),
                className="text-center m-2", style=CUSTOM_CSS[".card-body"]
            ), md=4),
        ], className="mb-4"),

        html.H2("Visualizações Interativas", className="text-center my-4", style={"color": "#DDDDDD"}),

        # 1. Distribuição das Notas do Exame (Histograma)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.histogram(df, x="exam_score", nbins=20,
                                                            labels={"exam_score": "Nota do Exame"}),
                                                "Distribuição das Notas do Exame")),
            html.Div("Conclusão: O histograma da nota do exame mostra uma distribuição aproximadamente normal, com a maioria dos estudantes concentrada em torno da média, e caudas mais finas em notas muito baixas ou muito altas.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

        # 2. Horas de Estudo vs Nota do Exame (Scatter Plot)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.scatter(df, x="hours_studied", y="exam_score",
                                                            labels={"hours_studied": "Horas de Estudo", "exam_score": "Nota do Exame"},
                                                            hover_data=["student_id", "sleep_hours", "attendance_percent", "previous_scores"]),
                                                "Horas de Estudo vs Nota do Exame")),
            html.Div("Conclusão: Este scatter plot revela uma **forte correlação positiva** entre as horas de estudo e a nota do exame. Estudantes que dedicam mais tempo aos estudos tendem a obter notas mais altas.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

        # 3. Matriz de Correlação (Heatmap)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.imshow(df[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr(),
                                                            text_auto=True, aspect="auto",
                                                            color_continuous_scale="Viridis"),
                                                "Matriz de Correlação entre Variáveis")),
            html.Div("Conclusão: A matriz de correlação quantifica a força e a direção das relações lineares entre as variáveis. `hours_studied` tem a correlação mais forte com `exam_score` (0.777), seguido por `previous_scores` (0.431). `attendance_percent` e `sleep_hours` têm correlações positivas mais fracas.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

        # 4. Horas de Sono vs Nota do Exame (Scatter Plot)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.scatter(df, x="sleep_hours", y="exam_score",
                                                            labels={"sleep_hours": "Horas de Sono", "exam_score": "Nota do Exame"},
                                                            hover_data=["student_id", "hours_studied", "attendance_percent", "previous_scores"]),
                                                "Horas de Sono vs Nota do Exame")),
            html.Div("Conclusão: Observa-se uma correlação positiva, embora mais fraca, entre as horas de sono e a nota do exame. Mais horas de sono parecem estar associadas a notas ligeiramente melhores, mas a relação não é tão linear ou pronunciada quanto a das horas de estudo.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

        # 5. Porcentagem de Presença vs Nota do Exame (Scatter Plot)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.scatter(df, x="attendance_percent", y="exam_score",
                                                            labels={"attendance_percent": "Porcentagem de Presença", "exam_score": "Nota do Exame"},
                                                            hover_data=["student_id", "hours_studied", "sleep_hours", "previous_scores"]),
                                                "Porcentagem de Presença vs Nota do Exame")),
            html.Div("Conclusão: Existe uma correlação positiva entre o percentual de presença e a nota do exame. Estudantes com maior frequência nas aulas tendem a ter notas mais elevadas, sugerindo a importância da participação em sala de aula.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

        # 6. Notas Anteriores vs Nota do Exame (Scatter Plot)
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=update_layout_dark(px.scatter(df, x="previous_scores", y="exam_score",
                                                            labels={"previous_scores": "Notas Anteriores", "exam_score": "Nota do Exame"},
                                                            hover_data=["student_id", "hours_studied", "sleep_hours", "attendance_percent"]),
                                                "Notas Anteriores vs Nota do Exame")),
            html.Div("Conclusão: As notas anteriores dos estudantes mostram uma correlação positiva com a nota do exame atual. Isso indica que o desempenho passado é um bom preditor do desempenho futuro, refletindo a consistência acadêmica.",
                     className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
        ]), className="mb-4", style=CUSTOM_CSS[".card-body"]),

    ],
    fluid=True
)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8050)
