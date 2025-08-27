import pandas as pd
import numpy as np
from pathlib import Path

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

# ------------------------------------------------------------
# Carregar dados
# ------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "dados_cafe.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Não encontrei '{DATA_PATH.name}' na pasta do app. Gere o CSV antes.")

df = pd.read_csv(DATA_PATH)

# Garantir colunas derivadas
if "fertilizante_kgN_ha" in df.columns and "N_kg_ha" not in df.columns:
    df["N_kg_ha"] = df["fertilizante_kgN_ha"]
if "lucro_Rsha" in df.columns and "rentabilidade_RSha" not in df.columns:
    df["rentabilidade_RSha"] = df["lucro_Rsha"]
if "custo_por_saca_R$" not in df.columns:
    df["custo_por_saca_R$"] = df["custo_total_RSha"] / \
        df["produtividade_sacas_ha"]
if "margem_liquida_%" not in df.columns:
    if "margem_liquida" in df.columns:
        df["margem_liquida_%"] = 100 * df["margem_liquida"].astype(float)
    else:
        df["margem_liquida_%"] = 100 * \
            (df["receita_total_RSha"] - df["custo_total_RSha"]) / \
            df["receita_total_RSha"]

# ------------------------------------------------------------
# Métricas e KPIs
# ------------------------------------------------------------
METRICS = {
    "Produtividade (sacas/ha)":              ("produtividade_sacas_ha", "up",   "num"),
    "C orgânico (g/kg)":                     ("C_organico_gkg",         "up",   "num"),
    "Irrigação (mm)":                        ("irrigacao_mm",           "down", "num"),
    "Água de pulverização (L/ha)":           ("agua_pulverizacao_Lha",  "down", "num"),
    "Água total (m³/ha)":                    ("agua_total_m3ha",        "down", "num"),
    "Produtividade hídrica (kg/m³)":         ("produtividade_hidrica_kg_m3", "up", "num"),
    "Diesel (L/ha)":                         ("diesel_Lha",             "down", "num"),
    "Intensidade de combustível (L/saca)":   ("diesel_por_saca_L",      "down", "num"),
    "N aplicado (kg/ha)":                    ("N_kg_ha",                "down", "num"),
    "Pegada de carbono (kg CO₂e/saca)":      ("GHG_kgCO2e_saca",        "down", "num"),
    "Pegada de carbono (t CO₂e/ha)":         ("CI_ha_tCO2e",            "down", "num"),
    "Custo total (R$/ha)":                   ("custo_total_RSha",       "down", "money"),
    "Custo por saca (R$/sc)":                ("custo_por_saca_R$",      "down", "money"),
    "Receita total (R$/ha)":                 ("receita_total_RSha",     "up",   "money"),
    "Rentabilidade (R$/ha)":                 ("rentabilidade_RSha",     "up",   "money"),
    "Margem líquida (%)":                    ("margem_liquida_%",       "up",   "perc"),
    "Biodiversidade (índice)":               ("biodiversidade_indice",  "up",   "num"),
    "Erosão (t/ha)":                         ("erosao_ton_ha",          "down", "num"),
    "Infiltração (mm/h)":                    ("infiltracao_mm_h",       "up",   "num"),
}

KPI_TOP = [
    "Produtividade (sacas/ha)",
    "Custo por saca (R$/sc)",
    "Margem líquida (%)",
    "Pegada de carbono (kg CO₂e/saca)",
    "Produtividade hídrica (kg/m³)",
    "Receita total (R$/ha)",
    "Rentabilidade (R$/ha)",
    "Diesel (L/ha)",
]

anos_options = [{"label": str(a), "value": int(a)}
                for a in sorted(df["ano"].unique())]
metric_options = [{"label": k, "value": k} for k in METRICS.keys()]

# Dicionário para labels bonitos nos gráficos
LABELS = {col: label for label, (col, _, _) in METRICS.items()}


# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------


def fmt_value(v, kind="num"):
    if pd.isna(v):
        return "–"

    if kind == "money":
        return "R$ {:,.2f}".format(v).replace(",", "X").replace(".", ",").replace("X", ".")
    if kind == "perc":
        return "{:,.2f}%".format(v).replace(",", "X").replace(".", ",").replace("X", ".")
    return "{:,.2f}".format(v).replace(",", "X").replace(".", ",").replace("X", ".")


def agg_series(s, agg): return s.median() if agg == "median" else s.mean()


def compute_benchmark(data, agg="mean"):
    rows = []
    for label, (col, _, _) in METRICS.items():
        if col not in data.columns:
            continue
        g = data.groupby("sistema")[col].apply(lambda x: agg_series(x, agg))
        conv, reg = g.get("convencional", np.nan), g.get(
            "regenerativo", np.nan)
        diff_pct = (reg - conv) / conv * \
            100 if pd.notna(conv) and conv != 0 else np.nan
        rows.append((label, conv, reg, diff_pct))
    return pd.DataFrame(rows, columns=["Indicador", "Convencional", "Regenerativo", "Diferença (%)"])


def compute_kpis_cards(data, agg="mean"):
    bench = compute_benchmark(data, agg).set_index("Indicador")
    cards = {}
    for k in KPI_TOP:
        if k in bench.index:
            conv, reg, diff = bench.loc[k, "Convencional"], bench.loc[k,
                                                                      "Regenerativo"], bench.loc[k, "Diferença (%)"]
            _, _, kind = METRICS[k]
            cards[k] = (fmt_value(conv, kind), fmt_value(
                reg, kind), fmt_value(diff, "perc"))
    return cards


def beneficial_signed_diff(row):
    label = row["Indicador"]
    val = row["Diferença (%)"]
    _, direction, _ = METRICS.get(label, (None, "up", "num"))
    return -val if direction == "down" else val


# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------
external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title="Café Regenerativo — Dashboard")
server = app.server

app.layout = dbc.Container(fluid=True, className="tight", children=[
    # Header + Subheader
    # Header
    dbc.Row([
        dbc.Col(html.H2([
            html.Span("Café ", className="cafe"),
            html.Span("| Manejo Convencional vs Regenerativo",
                      className="app-title")
        ], className="app-title"), md=8),
        dbc.Col(html.Div("Protótipo ESG • KPIs, Benchmarking e Análises Interativas",
                         className="app-subtitle"), md=4)
    ], className="mt-2 mb-1 align-items-center", id="header-row"),

    # Sub-header hero text
    dbc.Row(
        dbc.Col(
            html.H4([
                html.Span("Explorando impactos econômicos e ambientais ",
                          className="hero-strong"),
                html.Br(),  # << força a quebra de linha
                html.Span("da agricultura regenerativa e seus reflexos na competitividade do café brasileiro",
                          className="hero-muted")
            ], className="hero-text"),
            width=12
        ),
        className="hero-row mb-3"
    ), html.Hr(),



    # KPI Cards
    dbc.Row(id="row-kpis", className="gx-1 gy-1 section-separator"),

    # ===== LINHA 1: Benchmark + Dispersão =====
    dbc.Row([
        # --- Benchmark ---
        dbc.Col(dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Span("Benchmark | Diferenças (%)",
                              className="me-2"),
                    dcc.Checklist(
                        id="filtro-anos",
                        options=anos_options,
                        value=[opt["value"] for opt in anos_options],
                        inline=True,
                        inputStyle={"margin-right": "6px",
                                    "margin-left": "12px"}
                    )
                ], className="d-flex align-items-center justify-content-between")
            ]),
            dbc.CardBody(dcc.Graph(id="graf-benchmark",
                                   style={"height": "380px"}, config={"displayModeBar": False}))
        ]), md=6),

        # --- Dispersão(ScatteR) ---
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        html.Span("Correlação | Dispersão", className="me-2"),
                        # wrapper para os dois dropdowns
                        html.Div([
                            dcc.Dropdown(
                                id="scatter-x",
                                options=metric_options,
                                value="C orgânico (g/kg)",
                                clearable=False,
                                className="dd-compact",
                                style={"width": "220px", "marginRight": "8px"}
                            ),
                            dcc.Dropdown(
                                id="scatter-y",
                                options=metric_options,
                                value="Produtividade (sacas/ha)",
                                clearable=False,
                                className="dd-compact",
                                style={"width": "220px", "marginRight": "8px"}
                            ),
                        ], style={"display": "flex", "alignItems": "center"})
                    ], style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    })
                ),
                dbc.CardBody(
                    dcc.Graph(
                        id="graf-scatter",
                        style={"height": "380px"},
                        config={"displayModeBar": False}
                    )
                )
            ]),
            md=6
        )
    ], className="gx-1 gy-1 section-separator"),

    # ===== LINHA 2: Boxplot + Série temporal =====
    dbc.Row([
        # --- BOX ---
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                        # ...e o rótulo à esquerda
                        html.Span("Distribuição por manejo",
                                  className="header-label"),
                        # Dropdown à direita...
                        dcc.Dropdown(
                            id="filtro-metrica",
                            options=metric_options,
                            value="Produtividade (sacas/ha)",
                            clearable=False,
                            className="dd-compact",
                            style={"width": "220px", "marginRight": "8px"}
                        ),
                    ], style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "width": "100%"
                    })
                ),
                dbc.CardBody(
                    dcc.Graph(
                        id="graf-box",
                        style={"height": "380px"},
                        config={"displayModeBar": False}
                    )
                ),
            ]),
            md=6
        ),

        # --- SÉRIE ---
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Série temporal"),
                dbc.CardBody(
                    dcc.Graph(
                        id="graf-serie",
                        style={"height": "380px"},
                        config={"displayModeBar": False}
                    )
                ),
            ]),
            md=6
        )
    ], className="gx-1 gy-1 section-separator"),
    html.Hr(),

    # Footer
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Span("Carlos Augusto Freitas Silva  |  "),
                html.Span("carlosaugusto.fre@gmail.com",
                          className="footer-email")
            ], className="app-footer"),
            width=12
        ),
        className="mt-4 mb-2"
    ),

])

# ------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------


@app.callback(
    Output("row-kpis", "children"),
    Output("graf-benchmark", "figure"),
    Output("graf-box", "figure"),
    Output("graf-serie", "figure"),
    Output("graf-scatter", "figure"),
    Input("filtro-anos", "value"),
    Input("filtro-metrica", "value"),
    Input("scatter-x", "value"),
    Input("scatter-y", "value"),
)
def update_all(anos_sel, metrica, mx, my):
    # Seleção de anos (fallback)
    if not anos_sel:
        anos_sel = sorted(df["ano"].unique().tolist())
    dff = df[df["ano"].isin(anos_sel)].copy()

    # ---- KPI cards (média sempre) ----
    bench_cards = compute_benchmark(dff).set_index("Indicador")
    kpi_cards = []
    for label in KPI_TOP:
        if label in bench_cards.index:
            conv = fmt_value(
                bench_cards.loc[label, "Convencional"], METRICS[label][2])
            reg = fmt_value(
                bench_cards.loc[label, "Regenerativo"], METRICS[label][2])
            diff = fmt_value(bench_cards.loc[label, "Diferença (%)"], "perc")
        else:
            conv, reg, diff = "–", "–", "–"

        kpi_cards.append(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(label),
                    dbc.CardBody([
                        html.Div([html.Span("Convencional", className="kpi-legend me-2"),
                                 html.Span(conv, className="kpi-value")], className="kpi-line"),
                        html.Div([html.Span("Regenerativo", className="kpi-legend me-2"),
                                 html.Span(reg,  className="kpi-value")], className="kpi-line"),
                        html.Hr(),
                        html.Div("Reg vs Conv", className="kpi-legend"),
                        html.Div(diff, className="kpi-diff")
                    ])
                ], className="kpi-card mini"),
                md=3
            )
        )

    # ---- Benchmark ----
    bench = compute_benchmark(dff)
    bench["Benefício Ajustado (%)"] = bench.apply(
        beneficial_signed_diff, axis=1)
    bench_sorted = bench.sort_values(
        "Benefício Ajustado (%)", ascending=False)
    colors = ["#13CE66" if v >=
              0 else "#FF6B6B" for v in bench_sorted["Benefício Ajustado (%)"]]

    fig_bench = px.bar(
        bench_sorted,
        x="Benefício Ajustado (%)", y="Indicador", orientation="h",
        text=bench_sorted["Diferença (%)"].map(lambda v: fmt_value(v, "perc"))
    )

    fig_bench.update_traces(marker_color=colors,
                            textposition="outside",     # texto à direita
                            insidetextanchor="start",   # ancora as barras à esquerda
                            # fonte menor e 80% opaca
                            textfont=dict(
                                size=11, color="rgba(255,255,255,0.8)")
                            )

    fig_bench.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        bargap=0.3,
        yaxis=dict(
            side="right",  # rótulos do eixo y à direita
            tickfont=dict(size=8, color="rgba(255,255,255,0.8)")
        )
    )

    fig_bench.update_xaxes(
        dtick=15,  # distância entre os ticks/gridlines (padrão estava 20)
        gridcolor="rgba(255,255,255,0.1)",  # cor mais suave
        zeroline=False
    )

    # ---- Boxplot (métrica escolhida) ----
    col_box = METRICS[metrica][0]
    fig_box = px.box(
        dff, x="sistema", y=col_box, color="sistema",
        points=False, color_discrete_sequence=["#5DADE2", "#58D68D"],
        labels=LABELS
    )
    fig_box.update_layout(showlegend=False)
    fig_box.update_layout(
        xaxis_title_font=dict(size=12),
        yaxis_title_font=dict(size=12)
    )

    # ---- Série temporal (média sempre) ----
    grp = dff.groupby(["ano", "sistema"])[col_box].mean().reset_index()
    fig_series = px.line(
        grp, x="ano", y=col_box, color="sistema", markers=True,
        color_discrete_sequence=["#5DADE2", "#58D68D"],
        labels=LABELS
    )
    fig_series.update_xaxes(dtick=1)
    fig_series.update_layout(
        xaxis_title_font=dict(size=12),
        yaxis_title_font=dict(size=12)
    )

    # ---- Dispersão ----
    col_x = METRICS[mx][0]
    col_y = METRICS[my][0]
    fig_scatter = px.scatter(
        dff, x=col_x, y=col_y, color="sistema", size="area_ha",
        hover_data=["farm_id", "ano"],
        color_discrete_sequence=["#5DADE2", "#58D68D"],
        labels=LABELS
    )
    fig_scatter.update_layout(
        xaxis_title_font=dict(size=12),
        yaxis_title_font=dict(size=12)
    )
    fig_scatter.update_layout(
        legend=dict(
            orientation="h",        # horizontal
            yanchor="bottom",
            y=-0.3,                 # espaço abaixo do gráfico
            xanchor="center",
            x=0.5
        )
    )

    # ---- Uniformização visual ----
    for fig in (fig_bench, fig_box, fig_series, fig_scatter):
        fig.update_layout(
            margin=dict(l=8, r=8, t=30, b=8),
            height=380,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#EDEDED"),
            # xaxis_title=None,
            # yaxis_title=None,
        )
        # Linhas de grade brancas com 5% de opacidade
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")

    # ---- Tabela ----
    cols_out = [{"name": c, "id": c} for c in bench.columns]
    data_out = bench.round(2).to_dict("records")

    return kpi_cards, fig_bench, fig_box, fig_series, fig_scatter


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
