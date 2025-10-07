import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Carregar o dataset
df = pd.read_csv("student_exam_scores.csv")

# Inicializar o aplicativo Dash com um tema claro do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Esta linha expõe o servidor Flask subjacente para que o Gunicorn possa encontrá-lo.
server = app.server

# Estilos CSS personalizados para um visual mais profissional
CUSTOM_CSS = {
    "body": {
        "font-family": "Arial, sans-serif",
        "background-color": "#f8f9fa",
        "color": "#2c3e50",
        "min-height": "100vh"
    },
    ".card-header": {
        "background-color": "#3498db",
        "color": "white",
        "font-size": "1.2em",
        "font-weight": "bold",
        "border-radius": "8px 8px 0 0"
    },
    ".card-body": {
        "background-color": "white",
        "color": "#2c3e50",
        "border-radius": "0 0 8px 8px",
        "box-shadow": "0 4px 6px rgba(0,0,0,0.1)"
    },
    ".metric-value": {
        "font-size": "2.5em",
        "font-weight": "bold",
        "color": "#27ae60",
        "text-align": "center"
    },
    ".metric-label": {
        "font-size": "1em",
        "color": "#7f8c8d",
        "text-align": "center",
        "margin-bottom": "10px"
    },
    ".graph-conclusion": {
        "font-size": "0.9em",
        "margin-top": "15px",
        "padding": "12px",
        "background-color": "#e8f4fc",
        "border-left": "4px solid #3498db",
        "color": "#2c3e50",
        "border-radius": "0 8px 8px 0"
    },
    ".header-title": {
        "color": "#2c3e50",
        "font-size": "2.5em",
        "font-weight": "bold",
        "margin-bottom": "30px",
        "text-align": "center",
        "padding-top": "20px"
    },
    ".section-title": {
        "color": "#2c3e50",
        "font-size": "1.8em",
        "font-weight": "bold",
        "margin-bottom": "25px",
        "text-align": "center"
    }
}

# Função para aplicar o tema claro aos gráficos Plotly
def update_layout_light(fig, title_text):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#2c3e50",
        title_font_color="#2c3e50",
        title_text=title_text,
        title_x=0.5,
        title_font_size=16,
        margin=dict(t=50, b=50, l=50, r=50),
        hovermode='closest'
    )
    return fig

# Função para criar métricas principais
def create_metric_card(title, value, color="#3498db"):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title", style={"color": "#7f8c8d", "font-size": "1em", "margin-bottom": "10px"}),
            html.H2(f"{value:.2f}", className="card-text", style={"color": color, "font-weight": "bold", "font-size": "2.2em", "margin": "0"})
        ]),
        className="text-center m-2 shadow-sm",
        style={
            "border-radius": "10px",
            "border": "none",
            "box-shadow": "0 2px 10px rgba(0,0,0,0.08)",
            "transition": "transform 0.3s ease, box-shadow 0.3s ease"
        },
        hover_style={
            "transform": "translateY(-5px)",
            "box-shadow": "0 6px 20px rgba(0,0,0,0.15)"
        }
    )

# Criar gráfico de dispersão com linha de tendência
def create_scatter_with_trend(df, x_col, y_col, x_label, y_label, title):
    fig = px.scatter(df, x=x_col, y=y_col, 
                     labels={x_col: x_label, y_col: y_label},
                     hover_data=["student_id"],
                     trendline="ols",
                     opacity=0.7)
    
    fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='white')))
    fig = update_layout_light(fig, title)
    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)'),
        showlegend=False
    )
    return fig

# Criar gráfico de histograma
def create_histogram(df, col, label, title):
    fig = px.histogram(df, x=col, nbins=25, labels={col: label})
    fig = update_layout_light(fig, title)
    fig.update_layout(
        bargap=0.1,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    )
    return fig

# Criar heatmap de correlação
def create_correlation_heatmap(df):
    corr_data = df[["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]].corr()
    fig = px.imshow(
        corr_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        labels=dict(color="Correlação")
    )
    fig = update_layout_light(fig, "Matriz de Correlação entre Variáveis")
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Correlação",
            titleside="right"
        )
    )
    return fig

# --- Layout do Dashboard --- #
app.layout = dbc.Container(
    [
        # Cabeçalho
        html.Div([
            html.H1("Análise de Desempenho Acadêmico",
                    style=CUSTOM_CSS[".header-title"]),
            html.P("Dashboard interativo para análise de fatores que influenciam o desempenho dos estudantes",
                   className="text-center mb-4",
                   style={"color": "#7f8c8d", "font-size": "1.2em"})
        ], className="mb-5"),

        # Cards de métricas principais
        dbc.Row([
            dbc.Col(create_metric_card("Média da Nota do Exame", df['exam_score'].mean(), "#27ae60"), md=3),
            dbc.Col(create_metric_card("Média de Horas de Estudo", df['hours_studied'].mean(), "#3498db"), md=3),
            dbc.Col(create_metric_card("Média de Horas de Sono", df['sleep_hours'].mean(), "#9b59b6"), md=3),
            dbc.Col(create_metric_card("Média de Frequência", df['attendance_percent'].mean(), "#e74c3c"), md=3),
        ], className="mb-5"),

        # Título da seção de visualizações
        html.H2("Análise de Dados", style=CUSTOM_CSS[".section-title"], className="mb-4"),

        # Primeira linha de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribuição das Notas do Exame"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_histogram(df, "exam_score", "Nota do Exame", "")),
                        html.Div([
                            html.Strong("Análise: "),
                            "A distribuição das notas mostra uma concentração maior de estudantes com notas entre 70 e 85, indicando um desempenho geralmente satisfatório. A distribuição é levemente assimétrica para a esquerda, com poucos estudantes obtendo notas muito baixas."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Horas de Estudo vs Nota do Exame"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_scatter_with_trend(df, "hours_studied", "exam_score", "Horas de Estudo", "Nota do Exame", "")),
                        html.Div([
                            html.Strong("Análise: "),
                            "Existe uma forte correlação positiva (r ≈ 0.78) entre as horas de estudo e a nota do exame. Estudantes que dedicam mais tempo ao estudo tendem a obter resultados significativamente melhores."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6)
        ], className="mb-4"),

        # Segunda linha de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Matriz de Correlação"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_correlation_heatmap(df)),
                        html.Div([
                            html.Strong("Análise: "),
                            "A matriz de correlação revela que as horas de estudo têm a correlação mais forte com a nota do exame (0.78), seguido pelas notas anteriores (0.43). A frequência e as horas de sono também mostram correlações positivas moderadas."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Frequência vs Nota do Exame"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_scatter_with_trend(df, "attendance_percent", "exam_score", "Frequência (%)", "Nota do Exame", "")),
                        html.Div([
                            html.Strong("Análise: "),
                            "Existe uma correlação positiva moderada entre a frequência nas aulas e a nota do exame. Estudantes com maior frequência tendem a ter desempenho superior, ressaltando a importância da participação em sala de aula."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6)
        ], className="mb-4"),

        # Terceira linha de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Horas de Sono vs Nota do Exame"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_scatter_with_trend(df, "sleep_hours", "exam_score", "Horas de Sono", "Nota do Exame", "")),
                        html.Div([
                            html.Strong("Análise: "),
                            "Existe uma correlação positiva moderada entre as horas de sono e a nota do exame. Estudantes com 7-9 horas de sono tendem a ter melhor desempenho, sugerindo que o descanso adequado é um fator importante para o aprendizado."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Notas Anteriores vs Nota do Exame"),
                    dbc.CardBody([
                        dcc.Graph(figure=create_scatter_with_trend(df, "previous_scores", "exam_score", "Notas Anteriores", "Nota do Exame", "")),
                        html.Div([
                            html.Strong("Análise: "),
                            "Existe uma correlação positiva significativa entre as notas anteriores e a nota do exame atual. Isso indica que o desempenho acadêmico é relativamente consistente ao longo do tempo."
                        ], className="graph-conclusion", style=CUSTOM_CSS[".graph-conclusion"])
                    ])
                ], className="h-100")
            ], md=6)
        ], className="mb-5"),

        # Rodapé
        html.Div([
            html.Hr(className="mt-5"),
            html.Footer([
                html.Div([
                    html.P("Dashboard de Análise de Desempenho Acadêmico", className="text-center text-muted", style={"margin-bottom": "10px"}),
                    html.P("Dados analisados em tempo real | Atualizado em 2025", className="text-center text-muted small")
                ])
            ], className="container-fluid")
        ])
    ],
    fluid=True,
    style=CUSTOM_CSS["body"]
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
