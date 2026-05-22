"""
app.py — SolarMT | Calculadora de Viabilidade Solar Fotovoltaica
Design baseado no protótipo HTML do projeto SolarMT — BCT/UFMT
Criado por Atlas Kennedy e Co-autoria de Angélica Santos— Graduandos em Ciência e Tecnologia · UFMT
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data import (
    MESES, IRRADIANCIA_MENSAL, DIAS_POR_MES,
    TARIFA_ENERGIA_KWH, CUSTO_POR_KWP, VIDA_UTIL_ANOS,
    TAXA_DESCONTO, INFLACAO_ENERGIA_AA, HSP_MEDIA_ANUAL,
    LATITUDE, TEMP_OPERACAO_LOCAL, TEMP_REFERENCIA,
)
from calculations import (
    calcular_potencia_sistema, calcular_geracao_mensal,
    angulo_otimo, resumo_perdas, perda_por_temperatura,
)
from financial import (
    calcular_investimento, calcular_fluxo_caixa,
    calcular_payback, calcular_vpl, calcular_tir,
    economia_mensal_ano1, co2_evitado,
)

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SolarMT — Viabilidade Solar Fotovoltaica",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "step" not in st.session_state:
    st.session_state.step = 1
if "form" not in st.session_state:
    st.session_state.form = {}

# ═══════════════════════════════════════════════════════════════
# DADOS LOCAIS
# ═══════════════════════════════════════════════════════════════
CIDADES_HSP = {
    "Lucas do Rio Verde": 5.5,
    "Cuiabá":             5.6,
    "Várzea Grande":      5.6,
    "Rondonópolis":       5.5,
    "Sorriso":            5.4,
    "Sinop":              5.3,
    "Alta Floresta":      5.2,
    "Tangará da Serra":   5.4,
    "Barra do Garças":    5.5,
    "Cáceres":            5.5,
    "Outro município MT": 5.4,
}

SAZON = [1.05,1.02,0.98,0.95,0.92,0.88,0.90,0.95,1.00,1.05,1.08,1.07]
MESES_CURTOS = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

# ═══════════════════════════════════════════════════════════════
# TEMA PLOTLY — dark navy igual ao HTML
# ═══════════════════════════════════════════════════════════════
BG    = "#080f1e"
BG2   = "#0c1628"
BG3   = "#111e38"
AMBER = "#f59e0b"
GREEN = "#10b981"
BLUE  = "#60a5fa"
TEXT  = "#e8f0ff"
MUTED = "#7a90b8"
GRID  = "rgba(255,255,255,0.04)"

def theme(fig, height=260):
    fig.update_layout(
        paper_bgcolor=BG2, plot_bgcolor=BG,
        font=dict(family="Sora, sans-serif", color=TEXT, size=11),
        legend=dict(bgcolor=BG2, bordercolor="rgba(255,255,255,0.09)",
                    font=dict(color=MUTED, size=11)),
        height=height,
        margin=dict(l=10, r=10, t=36, b=10),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID,
                     linecolor="rgba(255,255,255,0.09)",
                     tickfont=dict(color=MUTED, size=10))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID,
                     linecolor="rgba(255,255,255,0.09)",
                     tickfont=dict(color=MUTED, size=10))
    return fig

# ═══════════════════════════════════════════════════════════════
# CSS — fiel ao index.html
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap');

:root{
  --bg:#080f1e;--bg2:#0c1628;--bg3:#111e38;
  --card:rgba(255,255,255,0.05);--card-b:rgba(255,255,255,0.09);
  --amber:#f59e0b;--amber2:#fbbf24;
  --amber-bg:rgba(245,158,11,0.12);--amber-bd:rgba(245,158,11,0.3);
  --green:#10b981;--green-bg:rgba(16,185,129,0.1);--green-bd:rgba(16,185,129,0.3);
  --blue:#60a5fa;--blue-bg:rgba(96,165,250,0.1);--blue-bd:rgba(96,165,250,0.3);
  --purple:#c084fc;--purple-bg:rgba(192,132,252,0.1);--purple-bd:rgba(192,132,252,0.3);
  --text:#e8f0ff;--muted:#7a90b8;--dim:#3d5280;--r:14px;--rs:8px
}

html,body,[class*="css"]{
  font-family:'Sora',sans-serif!important;
  background-color:var(--bg)!important;
  color:var(--text)!important;
}
.stApp{background-color:var(--bg)!important;}
#MainMenu,footer,header[data-testid="stHeader"]{display:none!important;}
section[data-testid="stSidebar"]{display:none!important;}

.block-container{
  max-width:900px!important;
  padding:0 20px 80px!important;
  margin:0 auto!important;
}

/* ── TOPBAR ── */
.topbar{
  padding:16px 0 14px;
  display:flex;align-items:center;gap:14px;
  border-bottom:1px solid var(--card-b);
  margin-bottom:0;
}
.logo-icon{
  width:38px;height:38px;border-radius:10px;
  background:linear-gradient(135deg,#f59e0b,#f97316);
  display:flex;align-items:center;justify-content:center;
  font-size:20px;flex-shrink:0;
}
.logo-text{font-size:18px;font-weight:700;color:var(--text);}
.logo-text span{color:var(--amber);}
.header-tag{
  margin-left:auto;font-size:11px;color:var(--muted);
  background:var(--bg3);border:1px solid var(--card-b);
  border-radius:20px;padding:4px 14px;
}

/* ── HERO ── */
.hero{text-align:center;padding:44px 24px 24px;}
.hero h1{
  font-size:clamp(24px,4vw,38px);font-weight:700;
  background:linear-gradient(135deg,var(--text) 30%,var(--amber));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:12px;line-height:1.2;
}
.hero p{color:var(--muted);font-size:15px;max-width:560px;margin:0 auto 24px;}
.hero-badges{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}
.badge{
  background:var(--bg3);border:1px solid var(--card-b);
  border-radius:20px;padding:5px 14px;font-size:12px;color:var(--muted);
}

/* ── STEPPER ── */
.stepper{
  display:flex;align-items:center;justify-content:center;
  padding:20px 24px;max-width:480px;margin:0 auto 28px;
}
.step{display:flex;align-items:center;gap:8px;}
.snum{
  width:34px;height:34px;border-radius:50%;
  background:var(--bg3);border:1.5px solid var(--dim);
  display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:600;color:var(--dim);
}
.slabel{font-size:13px;color:var(--dim);font-weight:500;}
.step.active .snum{background:var(--amber);border-color:var(--amber);color:#08101e;}
.step.active .slabel{color:var(--amber);}
.step.done .snum{background:var(--green);border-color:var(--green);color:#fff;}
.step.done .slabel{color:var(--green);}
.sline{flex:1;height:1px;background:var(--dim);margin:0 10px;min-width:32px;}
.sline.done{background:var(--green);}

/* ── CARD ── */
.card{
  background:var(--card);border:1px solid var(--card-b);
  border-radius:var(--r);padding:26px 28px;margin-bottom:16px;
}
.card-h{font-size:17px;font-weight:600;margin-bottom:5px;}
.card-sub{font-size:14px;color:var(--muted);margin-bottom:20px;}

/* ── METRIC CARDS ── */
.mg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px;}
.mc{border-radius:var(--r);padding:18px 20px;background:var(--card);border:1px solid var(--card-b);}
.mc.a{background:var(--amber-bg);border-color:var(--amber-bd);}
.mc.g{background:var(--green-bg);border-color:var(--green-bd);}
.mc.b{background:var(--blue-bg);border-color:var(--blue-bd);}
.ml{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:6px;}
.mv{font-size:22px;font-weight:700;}
.mc.a .mv{color:var(--amber);}
.mc.g .mv{color:var(--green);}
.mc.b .mv{color:var(--blue);}
.mu{font-size:11px;color:var(--dim);margin-top:2px;}

/* ── TIR CARD ── */
.tir-card{
  display:flex;align-items:center;gap:20px;
  background:var(--green-bg);border:1px solid var(--green-bd);
  border-radius:var(--r);padding:20px 24px;margin-bottom:16px;
}
.tir-val{font-size:30px;font-weight:700;color:var(--green);}
.tir-msg{margin-left:auto;max-width:300px;font-size:13px;color:var(--muted);line-height:1.5;}

/* ── INFO BOX ── */
.ibox{
  background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.25);
  border-radius:var(--rs);padding:14px 18px;font-size:14px;
  color:#93c5fd;margin-bottom:16px;line-height:1.6;
}
.ibox-warn{
  background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);
  border-radius:var(--rs);padding:14px 18px;font-size:14px;
  color:#fde68a;margin-bottom:16px;line-height:1.6;
}

/* ── DISCIPLINES ── */
.disc-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:4px;}
.dcard{border-radius:var(--rs);padding:14px;border:1px solid;}
.dcard.da{background:var(--amber-bg);border-color:var(--amber-bd);}
.dcard.db{background:var(--blue-bg);border-color:var(--blue-bd);}
.dcard.dg{background:var(--green-bg);border-color:var(--green-bd);}
.dcard.dp{background:var(--purple-bg);border-color:var(--purple-bd);}
.dcard.full{grid-column:span 2;}
.dcard h4{font-size:13px;font-weight:600;margin-bottom:5px;}
.dcard.da h4{color:var(--amber);}
.dcard.db h4{color:var(--blue);}
.dcard.dg h4{color:var(--green);}
.dcard.dp h4{color:var(--purple);}
.dcard p{font-size:12px;color:var(--muted);line-height:1.5;}

/* ── FOOTER ── */
.footer{
  margin-top:40px;padding:28px 0 20px;
  border-top:1px solid var(--card-b);
  text-align:center;color:var(--muted);font-size:13px;line-height:1.8;
}
.footer a{color:var(--amber);text-decoration:none;font-weight:600;}
.footer a:hover{text-decoration:underline;}
.footer-brand{color:#fff;font-weight:600;font-size:15px;margin-bottom:4px;}

/* ── Streamlit widgets dark ── */
input, textarea {
  background:#111e38!important;
  color:#e8f0ff!important;
  caret-color:#e8f0ff!important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input{
  background:#111e38!important;
  border:1px solid rgba(255,255,255,0.15)!important;
  border-radius:8px!important;
  color:#e8f0ff!important;
  font-family:'Sora',sans-serif!important;
  font-size:14px!important;
  -webkit-text-fill-color:#e8f0ff!important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus{
  border-color:var(--amber)!important;
  box-shadow:0 0 0 2px rgba(245,158,11,0.2)!important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"]>div{
  background:#111e38!important;
  border:1px solid rgba(255,255,255,0.15)!important;
  border-radius:8px!important;
  color:#e8f0ff!important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] *{
  color:#e8f0ff!important;
}
label[data-testid="stWidgetLabel"] p{
  font-size:11px!important;font-weight:600!important;
  color:var(--muted)!important;text-transform:uppercase;
  letter-spacing:.07em!important;
}
div[data-testid="stSlider"] p{color:var(--muted)!important;}
/* Garante que o placeholder fique visível */
div[data-testid="stNumberInput"] input::placeholder{
  color:rgba(255,255,255,0.35)!important;
}
div[data-testid="stButton"]>button{
  border-radius:8px!important;
  font-family:'Sora',sans-serif!important;
  font-weight:600!important;font-size:14px!important;
  padding:10px 26px!important;transition:all .2s!important;
}
div[data-testid="stButton"]>button[kind="primary"]{
  background:var(--amber)!important;color:#08101e!important;border:none!important;
}
div[data-testid="stButton"]>button[kind="primary"]:hover{
  background:var(--amber2)!important;transform:translateY(-1px);
}
div[data-testid="stButton"]>button[kind="secondary"]{
  background:transparent!important;
  color:var(--muted)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
}
div[data-testid="stTabs"] button{color:var(--muted)!important;}
div[data-testid="stTabs"] button[aria-selected="true"]{
  color:var(--amber)!important;
  border-bottom-color:var(--amber)!important;
}
div[data-testid="stDataFrame"]{
  background:var(--bg2)!important;
  border:1px solid var(--card-b)!important;
  border-radius:8px!important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TOPBAR
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="logo-icon">☀️</div>
  <span class="logo-text">Solar<span>MT</span></span>
  <div class="header-tag">UFMT · Seminário Integrador IV · 2026</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>Calculadora de Viabilidade<br>Solar Fotovoltaica</h1>
  <p>Descubra em minutos se a energia solar é viável para você — com análise técnica e financeira completa para a realidade do Mato Grosso.</p>
  <div class="hero-badges">
    <span class="badge">⚡ Física III</span>
    <span class="badge">∫ Cálculo III</span>
    <span class="badge">💰 Matemática Financeira</span>
    <span class="badge">📊 Probabilidade e Estatística</span>
    <span class="badge">🧠 Gestão do Conhecimento</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STEPPER
# ═══════════════════════════════════════════════════════════════
def render_stepper(step):
    labels = ["Consumo", "Instalação", "Resultados"]
    html = '<div class="stepper">'
    for i, label in enumerate(labels, 1):
        cls = "active" if i == step else ("done" if i < step else "")
        num = "✓" if i < step else str(i)
        html += f'<div class="step {cls}"><div class="snum">{num}</div><span class="slabel">{label}</span></div>'
        if i < 3:
            line_cls = "done" if step > i else ""
            html += f'<div class="sline {line_cls}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

render_stepper(st.session_state.step)

# ═══════════════════════════════════════════════════════════════
# ETAPA 1 — CONSUMO
# ═══════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="card"><div class="card-h">⚡ Dados de Consumo</div><div class="card-sub">Preencha com as informações da sua conta de energia elétrica.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cidade = st.selectbox("Cidade / Região", list(CIDADES_HSP.keys()),
                              help="Dados de irradiação solar do INMET/CRESESB")
    with col2:
        tipo = st.selectbox("Tipo de Propriedade",
                            ["Residencial", "Rural / Produtor", "Comercial / Industrial"])

    col3, col4 = st.columns(2)
    with col3:
        consumo = st.number_input("Consumo Médio Mensal (kWh)", min_value=50,
                                  max_value=50000, value=350, step=10,
                                  help='Veja o valor na sua conta de luz (campo "Consumo")')
    with col4:
        tarifa = st.number_input("Tarifa de Energia (R$/kWh)", min_value=0.20,
                                 max_value=3.00, value=0.87, step=0.01, format="%.2f",
                                 help="Energisa MT residencial c/ impostos ≈ R$ 0,87/kWh")

    st.markdown("</div>", unsafe_allow_html=True)

    _, bcol = st.columns([3,1])
    with bcol:
        if st.button("Próximo →", type="primary", use_container_width=True):
            if consumo < 50:
                st.error("Informe o consumo médio mensal em kWh (mínimo 50).")
            else:
                st.session_state.form.update({"cidade": cidade, "tipo": tipo,
                                               "consumo": consumo, "tarifa": tarifa})
                st.session_state.step = 2
                st.rerun()

# ═══════════════════════════════════════════════════════════════
# ETAPA 2 — INSTALAÇÃO
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="card"><div class="card-h">🏠 Dados de Instalação</div><div class="card-sub">Informe os detalhes do local e como pretende financiar o projeto.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Área Disponível no Telhado (m²)", min_value=0,
                               max_value=10000, value=0, step=5,
                               help="Área com boa incidência solar, sem sombra. Cada painel ocupa ≈ 2 m². Deixe 0 para calcular automaticamente.")
    with col2:
        orcamento = st.number_input("Orçamento Máximo (R$) — Opcional", min_value=0,
                                    max_value=9999999, value=0, step=1000,
                                    help="Custo médio MT: R$ 4.500/kWp instalado. Deixe 0 para calcular o ideal.")

    col3, col4 = st.columns(2)
    with col3:
        modalidade = st.selectbox("Modalidade de Compra",
                                  ["À vista", "Financiado (BNDES / banco)", "Consórcio", "Leasing solar"])
    with col4:
        inflacao = st.slider("Inflação da Energia (% a.a.)", 1.0, 15.0, 6.5, 0.5,
                             help="Média histórica ANEEL 2015–2025") / 100

    taxa_desc = st.slider("Taxa de Desconto / SELIC (% a.a.)", 5.0, 20.0, 12.0, 0.5,
                          help="Usada no cálculo do VPL e Payback Descontado") / 100

    # Financiamento
    taxa_fin, prazo_fin = None, None
    if "Financiado" in modalidade:
        cf1, cf2 = st.columns(2)
        with cf1:
            taxa_fin = st.number_input("Taxa de Juros Anual (%)", 0.0, 40.0, 10.0, 0.1,
                                       help="BNDES Mais Solar: ≈ 6–8% a.a. | Bancos: 10–18% a.a.") / 100
        with cf2:
            prazo_fin = st.number_input("Prazo do Financiamento (meses)", 12, 240, 60, 12,
                                        help="BNDES permite até 240 meses (20 anos)")

    st.markdown("</div>", unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("← Anterior", type="secondary", use_container_width=True):
            st.session_state.step = 1; st.rerun()
    with bc2:
        if st.button("☀️ Calcular Viabilidade", type="primary", use_container_width=True):
            st.session_state.form.update({
                "area": area, "orcamento": orcamento, "modalidade": modalidade,
                "inflacao": inflacao, "taxa_desc": taxa_desc,
                "taxa_fin": taxa_fin, "prazo_fin": prazo_fin,
            })
            st.session_state.step = 3; st.rerun()

# ═══════════════════════════════════════════════════════════════
# ETAPA 3 — RESULTADOS
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    f = st.session_state.form

    # ── Parâmetros ──────────────────────────────────────────────
    HSP       = CIDADES_HSP.get(f["cidade"], 5.5)
    consumo   = f["consumo"]
    tarifa    = f["tarifa"]
    inflacao  = f["inflacao"]
    taxa_desc = f["taxa_desc"]
    area_disp = f["area"] or 999999
    orcamento = f["orcamento"] or 999999999
    modalidade= f["modalidade"]

    # ── Cálculos técnicos ───────────────────────────────────────
    PANEL_KWP = 0.40;  PANEL_M2 = 2.0
    SYS_EFF   = 0.80;  COST_KWP = 4500
    LIFE      = 25;    DISC     = taxa_desc
    INF       = inflacao
    CO2_FAC   = 0.0884

    gen_painel_mes = HSP * PANEL_KWP * SYS_EFF * 30
    n_paineis = int(np.ceil(consumo / gen_painel_mes))
    n_paineis = min(n_paineis, int(area_disp / PANEL_M2))
    max_orcam = int(orcamento / (COST_KWP * PANEL_KWP))
    if max_orcam > 0:
        n_paineis = min(n_paineis, max_orcam)
    n_paineis = max(n_paineis, 1)

    kwp      = round(n_paineis * PANEL_KWP, 2)
    area_nec = n_paineis * PANEL_M2
    ger_mes  = round(n_paineis * gen_painel_mes)
    ger_ano  = ger_mes * 12
    co2_25a  = round((ger_ano / 1000) * CO2_FAC * LIFE, 1)

    # ── Cálculos financeiros ────────────────────────────────────
    custo    = kwp * COST_KWP
    eco_mes  = round(min(ger_mes, consumo) * tarifa)
    eco_ano  = eco_mes * 12
    payback  = round(custo / eco_ano, 1) if eco_ano > 0 else 0

    # VPL
    cfs = [-custo] + [eco_ano * (1 + INF)**(t-1) for t in range(1, LIFE+1)]
    vpl_val = round(sum(c / (1+DISC)**t for t, c in enumerate(cfs)))

    # TIR (bissecção)
    def _vpl(r):
        return sum(c / (1+r)**t for t, c in enumerate(cfs))
    lo, hi = 0.001, 5.0
    for _ in range(300):
        mid = (lo+hi)/2
        if _vpl(mid) > 0: lo = mid
        else: hi = mid
    tir_pct = round(mid * 100, 1)

    cov = min(100, round(ger_mes / consumo * 100))

    # Mensagem TIR
    if tir_pct >= 15:
        tir_txt = "🟢 Excelente! Supera amplamente a Selic e a maioria das aplicações financeiras."
    elif tir_pct >= 10:
        tir_txt = "🟢 Ótima rentabilidade. Superior à Selic histórica de longo prazo."
    elif tir_pct >= 7:
        tir_txt = "🟡 Boa rentabilidade. Comparável a CDBs de longo prazo com liquidez restrita."
    elif tir_pct >= 4:
        tir_txt = "🟡 Rentabilidade moderada. Avalie renegociar o custo de instalação."
    else:
        tir_txt = "🔴 Baixa rentabilidade. Reduza o sistema ou busque outro orçamento."

    # Financiamento PMT
    pmt_val, saldo_val = None, None
    if "Financiado" in modalidade and f.get("taxa_fin") and f.get("prazo_fin"):
        taxa_fin = f["taxa_fin"]; prazo_fin = int(f["prazo_fin"])
        rm = taxa_fin / 12
        if rm == 0:
            pmt_val = custo / prazo_fin
        else:
            pmt_val = custo * rm * (1+rm)**prazo_fin / ((1+rm)**prazo_fin - 1)
        pmt_val   = round(pmt_val)
        saldo_val = eco_mes - pmt_val

    # ── Info box ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="ibox">
      ✅ Com <strong>{n_paineis} painéis de 400 Wp</strong>, o sistema cobre
      <strong>{cov}% do seu consumo</strong> de {consumo} kWh/mês.
      Irradiação solar local de <strong>{HSP} kWh/m²/dia</strong> — uma das maiores do Brasil.
    </div>
    """, unsafe_allow_html=True)

    # Alerta de área
    if f["area"] > 0 and area_nec > f["area"]:
        st.markdown(f"""
        <div class="ibox-warn">
          ⚠️ O sistema ideal precisa de <strong>{area_nec:.0f} m²</strong> mas você informou
          apenas <strong>{f['area']} m²</strong>. O sistema foi reduzido para caber na área disponível.
        </div>
        """, unsafe_allow_html=True)

    # ── Métricas técnicas (amber) ─────────────────────────────────
    st.markdown(f"""
    <div class="mg">
      <div class="mc a">
        <div class="ml">Painéis Necessários</div>
        <div class="mv">{n_paineis}</div>
        <div class="mu">painéis de 400 Wp</div>
      </div>
      <div class="mc a">
        <div class="ml">Potência do Sistema</div>
        <div class="mv">{kwp:.2f} kWp</div>
        <div class="mu">kilowatt-pico</div>
      </div>
      <div class="mc a">
        <div class="ml">Área Necessária</div>
        <div class="mv">{area_nec:.0f} m²</div>
        <div class="mu">metros quadrados</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Métricas de geração (green) ───────────────────────────────
    st.markdown(f"""
    <div class="mg">
      <div class="mc g">
        <div class="ml">Geração Mensal Est.</div>
        <div class="mv">{ger_mes:,}</div>
        <div class="mu">kWh / mês</div>
      </div>
      <div class="mc g">
        <div class="ml">Economia Mensal</div>
        <div class="mv">R$ {eco_mes:,}</div>
        <div class="mu">R$ / mês</div>
      </div>
      <div class="mc g">
        <div class="ml">CO₂ Evitado (25 anos)</div>
        <div class="mv">{co2_25a} t</div>
        <div class="mu">toneladas de CO₂</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Métricas financeiras (blue) ───────────────────────────────
    vpl_fmt = f"R$ {abs(vpl_val):,.0f}".replace(",","X").replace(".",",").replace("X",".")
    if vpl_val < 0: vpl_fmt = "-" + vpl_fmt
    st.markdown(f"""
    <div class="mg">
      <div class="mc b">
        <div class="ml">Custo do Sistema</div>
        <div class="mv">R$ {custo:,.0f}</div>
        <div class="mu">instalado completo</div>
      </div>
      <div class="mc b">
        <div class="ml">Payback Simples</div>
        <div class="mv">{payback} anos</div>
        <div class="mu">anos para retorno</div>
      </div>
      <div class="mc b">
        <div class="ml">VPL (25 anos)</div>
        <div class="mv">{vpl_fmt}</div>
        <div class="mu">valor presente líquido</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TIR card ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="tir-card">
      <div style="font-size:36px;">📈</div>
      <div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#7a90b8;margin-bottom:4px;">
          TIR — Taxa Interna de Retorno
        </div>
        <div class="tir-val">{tir_pct}% a.a.</div>
      </div>
      <div class="tir-msg">{tir_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Financiamento ─────────────────────────────────────────────
    if pmt_val is not None:
        saldo_cor = GREEN if saldo_val >= 0 else "#f87171"
        saldo_pfx = "+" if saldo_val >= 0 else ""
        st.markdown(f"""
        <div class="card">
          <div class="card-h">🏦 Detalhes do Financiamento</div>
          <div class="mg" style="margin-top:12px;">
            <div class="mc b">
              <div class="ml">Parcela Mensal</div>
              <div class="mv">R$ {pmt_val:,}</div>
              <div class="mu">R$ / mês</div>
            </div>
            <div class="mc g">
              <div class="ml">Saldo Mensal Líquido</div>
              <div class="mv" style="color:{saldo_cor};">{saldo_pfx}R$ {abs(saldo_val):,}</div>
              <div class="mu">economia − parcela</div>
            </div>
            <div class="mc">
              <div class="ml">Taxa Anual</div>
              <div class="mv">{f['taxa_fin']*100:.1f}%</div>
              <div class="mu">{int(f['prazo_fin'])} meses</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # GRÁFICOS — 3 charts como no HTML
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="card-h" style="margin:24px 0 14px;font-size:15px;font-weight:600;color:#7a90b8;">📊 Análise Visual</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "☀️ Geração vs Consumo",
        "💸 Fluxo de Caixa",
        "🔬 Física do Sistema",
        "📊 Estatística",
        "🌿 Ambiental",
    ])

    # ── Tab 1: Geração vs Consumo ─────────────────────────────────
    with tab1:
        from data import IRRADIANCIA_MENSAL as _irr_map
        from calculations import calcular_geracao_mensal as _calc_ger
        import financial as fin2, data as dados2
        dados2.TARIFA_ENERGIA_KWH = tarifa; dados2.INFLACAO_ENERGIA_AA = inflacao; dados2.TAXA_DESCONTO = taxa_desc
        fin2.TARIFA_ENERGIA_KWH = tarifa; fin2.INFLACAO_ENERGIA_AA = inflacao; fin2.TAXA_DESCONTO = taxa_desc
        from calculations import calcular_potencia_sistema as _cps
        _pot = _cps(consumo)
        _ger = _calc_ger(_pot["potencia_real_kWp"])
        _eco = economia_mensal_ano1(_ger["geracao_kwh"], consumo)

        ger_vals = [_ger["geracao_kwh"][m] for m in MESES]
        ic_lo    = [_ger["ic_lower"][m] for m in MESES]
        ic_hi    = [_ger["ic_upper"][m] for m in MESES]

        fig_t1 = go.Figure()
        fig_t1.add_trace(go.Scatter(
            x=MESES + MESES[::-1], y=ic_hi + ic_lo[::-1],
            fill="toself", fillcolor="rgba(245,158,11,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="IC 95% (Estatística)", hoverinfo="skip",
        ))
        fig_t1.add_trace(go.Bar(
            x=MESES, y=ger_vals, name="Geração Estimada",
            marker_color="rgba(245,158,11,0.75)",
            marker_line_color=AMBER, marker_line_width=1,
        ))
        fig_t1.add_trace(go.Scatter(
            x=MESES, y=[consumo]*12, name="Consumo Mensal",
            line=dict(color="#f87171", width=2.5, dash="dash"), mode="lines",
        ))
        fig_t1.add_trace(go.Scatter(
            x=MESES, y=ger_vals, name="Geração (linha)",
            line=dict(color=AMBER, width=2.5),
            mode="lines+markers", marker=dict(size=7, color=AMBER),
        ))
        fig_t1.update_layout(
            title="Geração Estimada vs Consumo Mensal (kWh)",
            barmode="overlay", yaxis_title="kWh",
            legend=dict(orientation="h", y=-0.28),
        )
        theme(fig_t1, height=340)
        st.plotly_chart(fig_t1, use_container_width=True)

        import pandas as pd
        df_ger = pd.DataFrame({
            "Mês":            MESES,
            "Geração (kWh)":  [_ger["geracao_kwh"][m] for m in MESES],
            "IC Inf. 95%":    [_ger["ic_lower"][m] for m in MESES],
            "IC Sup. 95%":    [_ger["ic_upper"][m] for m in MESES],
            "Consumo (kWh)":  [consumo]*12,
            "Saldo (kWh)":    [round(_ger["geracao_kwh"][m]-consumo,1) for m in MESES],
            "Economia (R$)":  [_eco[m] for m in MESES],
        })
        st.dataframe(df_ger, use_container_width=True, hide_index=True)

    # ── Tab 2: Fluxo de Caixa ─────────────────────────────────────
    with tab2:
        import financial as _fin
        _fin.TARIFA_ENERGIA_KWH = tarifa; _fin.INFLACAO_ENERGIA_AA = inflacao; _fin.TAXA_DESCONTO = taxa_desc
        from calculations import calcular_potencia_sistema as _cps2
        _pot2 = _cps2(consumo)
        from calculations import calcular_geracao_mensal as _cg2
        _ger2 = _cg2(_pot2["potencia_real_kWp"])
        _inv2 = calcular_investimento(_pot2["potencia_real_kWp"])
        _fc2  = calcular_fluxo_caixa(_ger2["media_anual"], consumo, _inv2["custo_total"])
        _pb2  = calcular_payback(_fc2["acumulado"], _fc2["fluxo_descontado"], _inv2["custo_total"])
        _vpl2 = calcular_vpl(_fc2["fluxo_descontado"], _inv2["custo_total"])
        _tir2 = calcular_tir(_fc2["fluxo_liquido"], _inv2["custo_total"])

        anos_l = [f"Ano {a}" for a in _fc2["anos"]]

        fig_t2 = make_subplots(
            rows=2, cols=1,
            subplot_titles=["Fluxo de Caixa Líquido Anual (R$)", "Fluxo Acumulado — Payback (R$)"],
            vertical_spacing=0.14,
        )
        cores_fl = [GREEN if v >= 0 else "#f87171" for v in _fc2["fluxo_liquido"]]
        fig_t2.add_trace(go.Bar(x=anos_l, y=_fc2["fluxo_liquido"],
                                marker_color=cores_fl, name="Fluxo Líquido"), row=1, col=1)
        cores_ac = [GREEN if v >= 0 else "#f87171" for v in _fc2["acumulado"]]
        fig_t2.add_trace(go.Scatter(x=anos_l, y=_fc2["acumulado"],
                                    mode="lines+markers",
                                    line=dict(color=AMBER, width=3),
                                    marker=dict(color=cores_ac, size=6),
                                    name="Acumulado"), row=2, col=1)
        # Linha zero (add_shape — compatível com eixo categórico)
        fig_t2.add_shape(type="line", x0=0, x1=1, y0=0, y1=0,
                         xref="x2 domain", yref="y2",
                         line=dict(dash="dash", color="#f87171", width=1.5))
        fig_t2.add_annotation(x=0.01, y=0, xref="x2 domain", yref="y2",
                              text="Ponto de Equilíbrio", showarrow=False,
                              xanchor="left", yanchor="bottom",
                              font=dict(color="#f87171", size=10))
        # Payback marker
        if _pb2["payback_simples_anos"]:
            pb_idx = _pb2["payback_simples_anos"] - 1
            fig_t2.add_shape(type="line", x0=pb_idx, x1=pb_idx, y0=0, y1=1,
                             xref="x2", yref="y2 domain",
                             line=dict(dash="dot", color=AMBER, width=2))
            fig_t2.add_annotation(x=pb_idx, y=1, xref="x2", yref="y2 domain",
                                  text=f"Payback: Ano {_pb2['payback_simples_anos']}",
                                  showarrow=False, yanchor="bottom",
                                  font=dict(color=AMBER, size=11))
        fig_t2.update_layout(height=560, showlegend=True)
        theme(fig_t2, height=560)
        st.plotly_chart(fig_t2, use_container_width=True)

        col_fa, col_fb = st.columns(2)
        with col_fa:
            labels_pie2 = ["Módulos 45%", "Inversor 20%", "Estrutura 10%", "Instalação 15%", "Outros 10%"]
            values_pie2 = [_inv2["custo_modulos"], _inv2["custo_inversor"],
                           _inv2["custo_estrutura"], _inv2["custo_instalacao"], _inv2["custo_outros"]]
            fig_pie2 = go.Figure(go.Pie(
                labels=labels_pie2, values=values_pie2, hole=0.5,
                marker_colors=[AMBER, BLUE, GREEN, "#c084fc", "#7a90b8"],
                textfont=dict(color=TEXT, size=10),
            ))
            fig_pie2.update_layout(title="Composição do Investimento",
                                   legend=dict(orientation="h", y=-0.2, font=dict(color=MUTED)))
            theme(fig_pie2, height=280)
            st.plotly_chart(fig_pie2, use_container_width=True)
        with col_fb:
            pb_d = _pb2["payback_descontado_anos"]
            st.markdown(f"""
| Indicador | Valor |
|-----------|-------|
| **VPL (25 anos)** | R$ {_vpl2['vpl']:,.0f} |
| **TIR** | {_tir2}% a.a. |
| **SELIC ref.** | {taxa_desc*100:.1f}% a.a. |
| **Payback simples** | {_pb2['payback_simples_anos']} anos |
| **Payback descontado** | {pb_d if pb_d else ">25"} anos |
| **Custo total** | R$ {_inv2['custo_total']:,.0f} |
| **Custo/kWp** | R$ {CUSTO_POR_KWP:,.0f} |
""")

    # ── Tab 3: Física do Sistema ──────────────────────────────────
    with tab3:
        from calculations import resumo_perdas as _rp, angulo_otimo as _ao, perda_por_temperatura as _pt
        _per = _rp(); _ang = _ao()

        st.markdown(f'<span style="background:#1a3a5c;color:#60a5fa;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:700;">Física III</span> &nbsp;Efeito Fotovoltaico · Temperatura · Otimização de Inclinação (Cálculo III)', unsafe_allow_html=True)
        st.markdown("---")

        col3a, col3b = st.columns(2)
        with col3a:
            st.markdown("**Diagrama de Perdas do Sistema (Sankey simplificado)**")
            labels_p = [k for k in _per if k != "Total"]
            vals_p   = [_per[k] for k in labels_p]
            fig_per2 = go.Figure(go.Bar(
                x=labels_p, y=vals_p,
                marker_color=["rgba(248,113,113,0.8)"]*len(labels_p),
                marker_line_color="#f87171", marker_line_width=1,
                text=[f"{v}%" for v in vals_p], textposition="outside",
                textfont=dict(color=MUTED),
            ))
            fig_per2.update_layout(title=f"Perdas do Sistema (Total: {_per['Total']}%)", yaxis_title="Perda (%)")
            theme(fig_per2, height=300)
            st.plotly_chart(fig_per2, use_container_width=True)
            st.markdown("**Equação do Performance Ratio (PR):**")
            st.latex(r"PR = 1 - (\eta_{inv}+\eta_{cab}+\eta_{som}+\eta_{suj}+lpha_T\Delta T)")
            st.latex(rf"PR = 1 - ({_per['Total']/100:.4f}) = {1-_per['Total']/100:.4f}")

        with col3b:
            st.markdown("**Curva de Irradiância vs Ângulo de Inclinação (Cálculo III)**")
            fig_ang2 = go.Figure()
            fig_ang2.add_trace(go.Scatter(
                x=_ang["betas"], y=_ang["irradiancias"],
                mode="lines", line=dict(color=AMBER, width=2.5),
                fill="tozeroy", fillcolor="rgba(245,158,11,0.08)",
            ))
            fig_ang2.add_vline(x=_ang["angulo_otimo_graus"], line_dash="dash",
                               line_color=GREEN,
                               annotation_text=f"β* = {_ang['angulo_otimo_graus']}°",
                               annotation_font_color=GREEN)
            fig_ang2.update_layout(title="Otimização do Ângulo de Inclinação",
                                   xaxis_title="Ângulo β (graus)",
                                   yaxis_title="Irradiância média (kWh/m²/dia)")
            theme(fig_ang2, height=300)
            st.plotly_chart(fig_ang2, use_container_width=True)
            st.markdown("**Equação de otimização (Cálculo III):**")
            st.latex(r"I(eta,\gamma) = I_{horiz} \cdot [\cos(arphi-eta)\cdot\cos(\gamma)]")
            st.latex(rf"eta^* = {_ang['angulo_otimo_graus']:.1f}° pprox |arphi| = {abs(LATITUDE)}°")

        st.markdown("---")
        st.markdown("**Perda por Temperatura (Física III — Coeficiente de Temperatura)**")
        _temps = np.arange(25, 80, 1)
        _perda_t = [_pt(float(t)) for t in _temps]
        fig_tmp2 = go.Figure(go.Scatter(
            x=_temps, y=_perda_t, mode="lines",
            line=dict(color="#f87171", width=2),
            fill="tozeroy", fillcolor="rgba(248,113,113,0.08)",
        ))
        fig_tmp2.add_vline(x=TEMP_OPERACAO_LOCAL, line_dash="dash", line_color=AMBER,
                           annotation_text=f"T_op={TEMP_OPERACAO_LOCAL}°C ({_per['Temperatura']}% perda)",
                           annotation_font_color=AMBER)
        fig_tmp2.update_layout(title="Perda de Potência por Temperatura (αT = −0,35%/°C)",
                               xaxis_title="Temperatura de Operação (°C)", yaxis_title="Perda (%)")
        theme(fig_tmp2, height=260)
        st.plotly_chart(fig_tmp2, use_container_width=True)
        st.latex(r"\Delta P = lpha_T \cdot (T_{op} - T_{STC}) = -0{,}0035 \cdot (T_{op} - 25°C)")

    # ── Tab 4: Estatística ────────────────────────────────────────
    with tab4:
        from data import IRRADIANCIA_MENSAL as _irr_full
        st.markdown('<span style="background:#1a3a2a;color:#10b981;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:700;">Probabilidade e Estatística</span> &nbsp;Médias Históricas · IC 95% · Distribuição de Geração', unsafe_allow_html=True)
        st.markdown("---")

        _irr_vals  = list(_irr_full.values())
        _media_irr = np.mean(_irr_vals)
        _desvio    = np.std(_irr_vals)

        ms1, ms2, ms3 = st.columns(3)
        ms1.metric("HSP Médio Anual",    f"{_media_irr:.2f} kWh/m²/dia")
        ms2.metric("Desvio Padrão",      f"{_desvio:.2f} kWh/m²/dia")
        ms3.metric("Coef. de Variação",  f"{_desvio/_media_irr*100:.1f}%")

        fig_stat2 = go.Figure()
        fig_stat2.add_trace(go.Bar(x=MESES, y=_irr_vals, name="HSP Médio",
                                   marker_color="rgba(245,158,11,0.75)",
                                   marker_line_color=AMBER, marker_line_width=1))
        fig_stat2.add_hline(y=_media_irr, line_dash="dash", line_color=GREEN,
                            annotation_text=f"Média = {_media_irr:.2f} kWh/m²/dia",
                            annotation_font_color=GREEN)
        fig_stat2.add_hline(y=_media_irr+_desvio, line_dash="dot", line_color=MUTED,
                            annotation_text="+1σ", annotation_font_color=MUTED)
        fig_stat2.add_hline(y=_media_irr-_desvio, line_dash="dot", line_color=MUTED,
                            annotation_text="-1σ", annotation_font_color=MUTED)
        fig_stat2.update_layout(title="Irradiância Solar Mensal — Lucas do Rio Verde/MT (CRESESB)",
                                yaxis_title="HSP (kWh/m²/dia)")
        theme(fig_stat2, height=340)
        st.plotly_chart(fig_stat2, use_container_width=True)

        # Distribuição normal (TCL)
        st.markdown("**Distribuição da Geração Anual — Teorema Central do Limite (n=20 anos)**")
        from calculations import calcular_potencia_sistema as _cps3, calcular_geracao_mensal as _cg3
        _pot3 = _cps3(consumo)
        _ger3 = _cg3(_pot3["potencia_real_kWp"])
        _med_ag = _ger3["media_anual"]
        _sig_ag = _med_ag * 0.06
        _x_dist = np.linspace(_med_ag - 3*_sig_ag, _med_ag + 3*_sig_ag, 300)
        _y_dist = (1/(_sig_ag*np.sqrt(2*np.pi))) * np.exp(-0.5*((_x_dist-_med_ag)/_sig_ag)**2)
        _lo95 = _med_ag - 1.96*_sig_ag; _hi95 = _med_ag + 1.96*_sig_ag
        fig_dist2 = go.Figure()
        fig_dist2.add_trace(go.Scatter(x=_x_dist, y=_y_dist, mode="lines",
                                       line=dict(color=AMBER, width=2),
                                       fill="tozeroy", fillcolor="rgba(245,158,11,0.12)"))
        fig_dist2.add_vrect(x0=_lo95, x1=_hi95, fillcolor="rgba(16,185,129,0.08)",
                            layer="below", line_width=0, annotation_text="IC 95%",
                            annotation_font_color=GREEN)
        fig_dist2.add_vline(x=_med_ag, line_dash="dash", line_color=GREEN,
                            annotation_text=f"μ = {_med_ag:.0f} kWh/ano",
                            annotation_font_color=GREEN)
        fig_dist2.update_layout(title=f"Distribuição Anual — IC 95%: [{_lo95:.0f}, {_hi95:.0f}] kWh",
                                xaxis_title="kWh/ano", yaxis_title="Densidade de Probabilidade")
        theme(fig_dist2, height=280)
        st.plotly_chart(fig_dist2, use_container_width=True)
        st.latex(r"ar{X} \pm 1{,}96 \cdot rac{\sigma}{\sqrt{n}} \quad 	ext{(Teorema Central do Limite)}")
        st.markdown(f"**Intervalo de Confiança 95%:** [{_lo95:,.0f} ; {_hi95:,.0f}] kWh/ano")

    # ── Tab 5: Ambiental ──────────────────────────────────────────
    with tab5:
        from financial import co2_evitado as _co2
        from calculations import calcular_potencia_sistema as _cps4, calcular_geracao_mensal as _cg4
        _pot4 = _cps4(consumo)
        _ger4 = _cg4(_pot4["potencia_real_kWp"])
        _co2d = _co2(_ger4["media_anual"])

        ca, cb, cc = st.columns(3)
        ca.metric("CO₂ evitado/ano",      f"{_co2d['kg_co2_ano']:,.0f} kg")
        cb.metric("CO₂ evitado (25 anos)", f"{_co2d['ton_co2_25anos']:.1f} t")
        cc.metric("Equivalente em árvores",f"{_co2d['arvores_eq']:,} 🌳")

        _anos25 = list(range(1, 26))
        _co2_acum = [_co2d["kg_co2_ano"] * a / 1000 for a in _anos25]
        fig_co2_2 = go.Figure(go.Scatter(
            x=[f"Ano {a}" for a in _anos25], y=_co2_acum,
            mode="lines+markers", line=dict(color=GREEN, width=3),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.1)",
            marker=dict(size=5, color=GREEN),
        ))
        fig_co2_2.update_layout(title="CO₂ Evitado Acumulado ao Longo de 25 Anos (toneladas)",
                                yaxis_title="CO₂ (t)")
        theme(fig_co2_2, height=280)
        st.plotly_chart(fig_co2_2, use_container_width=True)
        st.markdown(f"""
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);
                    border-radius:10px;padding:14px 18px;font-size:13px;color:#6ee7b7;margin-top:8px;">
            🌱 Em 25 anos, este sistema evitará <b>{_co2d['ton_co2_25anos']:.1f} toneladas</b> de CO₂ —
            equivalente ao plantio de aproximadamente <b>{_co2d['arvores_eq']:,} árvores</b>.<br>
            Fator de emissão da rede elétrica brasileira: <b>0,094 tCO₂/MWh</b> (ONS 2023).
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # DISCIPLINAS — igual ao HTML
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="card" style="margin-top:20px;">
      <div class="card-h">📚 Articulação com as Disciplinas do Curso</div>
      <div class="card-sub">Como os cálculos deste sistema se relacionam com cada componente curricular:</div>
      <div class="disc-grid">
        <div class="dcard da">
          <h4>⚡ Física III</h4>
          <p>Cálculo da potência solar incidente (E = P·A·η), efeito fotoelétrico, irradiação solar por região, perdas por reflexão e temperatura dos painéis. Coeficiente de temperatura αT = −0,35%/°C.</p>
        </div>
        <div class="dcard db">
          <h4>∫ Cálculo III</h4>
          <p>Modelagem da irradiação como função de múltiplas variáveis (ângulo, latitude, sazonalidade), otimização do ângulo de inclinação β* = |φ| ≈ 13° para Lucas do Rio Verde/MT.</p>
        </div>
        <div class="dcard dg">
          <h4>💰 Matemática Financeira</h4>
          <p>VPL (Valor Presente Líquido), TIR (Taxa Interna de Retorno) por bissecção numérica, payback descontado, PMT para financiamento, juros compostos e depreciação dos módulos (0,5%/ano).</p>
        </div>
        <div class="dcard dp">
          <h4>📊 Probabilidade e Estatística</h4>
          <p>Análise de séries históricas de irradiação solar (INMET/CRESESB 1994–2020), variabilidade sazonal, intervalos de confiança de 95% (Teorema Central do Limite) para estimativa de produção anual.</p>
        </div>
        <div class="dcard da full">
          <h4>🧠 Gestão do Conhecimento</h4>
          <p>Este sistema é um instrumento de disseminação do conhecimento técnico-científico para a comunidade do Mato Grosso. Democratiza análises antes restritas a engenheiros especializados, capacitando produtores rurais, moradores e pequenas empresas a tomarem decisões fundamentadas sobre energia renovável. Código modularizado e documentado para servir de base a futuros alunos do BCT/UFMT.</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fórmulas ──────────────────────────────────────────────────
    with st.expander("📐 Fórmulas e Fundamentação Teórica"):
        c_e1, c_e2 = st.columns(2)
        with c_e1:
            st.markdown("**⚡ Física III**")
            st.latex(r"G_{mes} = HSP \cdot P_{kWp} \cdot \eta_{sistema} \cdot 30")
            st.latex(r"PR = 1 - (\eta_{inv}+\eta_{cab}+\eta_{som}+\eta_{suj}+\alpha_T\Delta T)")
            st.markdown("**∫ Cálculo III**")
            st.latex(r"\beta^* = \arg\max_\beta I(\beta,\gamma) \approx |\varphi|")
        with c_e2:
            st.markdown("**💰 Matemática Financeira**")
            st.latex(r"VPL = -C_0 + \sum_{t=1}^{25}\frac{FC_t}{(1+i)^t}")
            st.latex(r"PMT = PV \cdot \frac{r(1+r)^n}{(1+r)^n - 1}")
            st.markdown("**📊 Probabilidade e Estatística**")
            st.latex(r"IC_{95\%} = \bar{X} \pm 1{,}96 \cdot \frac{\sigma}{\sqrt{n}}")

    # ── Botões ────────────────────────────────────────────────────
    # Fórmulas (Gestão do Conhecimento)
    with st.expander("📐 Fórmulas e Fundamentação Teórica — Gestão do Conhecimento"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.markdown("**⚡ Física III**")
            st.latex(r"G_{mes} = HSP \cdot P_{kWp} \cdot PR \cdot 30")
            st.latex(r"PR = 1 - (\eta_{inv}+\eta_{cab}+\eta_{som}+\eta_{suj}+\alpha_T\Delta T)")
            st.markdown("**∫ Cálculo III**")
            st.latex(r"\beta^* = \arg\max_\beta I(\beta,\gamma) \approx |\varphi|")
        with col_e2:
            st.markdown("**💰 Matemática Financeira**")
            st.latex(r"VPL = -C_0 + \sum_{t=1}^{25}\frac{FC_t}{(1+i)^t}")
            st.latex(r"PMT = PV \cdot \frac{r(1+r)^n}{(1+r)^n - 1}")
            st.markdown("**📊 Probabilidade e Estatística**")
            st.latex(r"IC_{95\%} = \bar{X} \pm 1{,}96 \cdot \frac{\sigma}{\sqrt{n}}")

    # Nota de rodapé do resultado (igual ao HTML)
    st.markdown("""
    <div style="text-align:center;font-size:12px;color:#3d5280;
                margin-top:8px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.09);">
      Sistema SolarMT — Projeto de Extensão · Seminário Integrador IV · UFMT ·
      Bacharelado em Ciência e Tecnologia · 2026<br>
      Dados de irradiação: INMET / CRESESB · Licença: GNU GPL v3.0 (Software Livre)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Compartilhar nas redes sociais ───────────────────────────
    st.markdown('<div style="font-size:13px;font-weight:600;color:#7a90b8;margin-bottom:10px;">📣 Compartilhar resultado</div>', unsafe_allow_html=True)

    import streamlit.components.v1 as components

    _share_url  = "https://calculadorasolarmatogro.streamlit.app"
    _share_text = (
        f"Simulei meu sistema solar com a SolarMT e o resultado foi incrível! "
        f"Sistema de {kwp:.1f} kWp, retorno em {payback} anos e TIR de {tir_pct}% a.a. "
        f"Feito por Atlas Kennedy — BCT/UFMT. Calcule o seu também:"
    )
    import urllib.parse
    _txt_enc  = urllib.parse.quote(_share_text)
    _url_enc  = urllib.parse.quote(_share_url)
    _wa_link  = f"https://wa.me/?text={_txt_enc}%20{_url_enc}"
    _tw_link  = f"https://twitter.com/intent/tweet?text={_txt_enc}&url={_url_enc}"
    _li_link  = f"https://www.linkedin.com/sharing/share-offsite/?url={_url_enc}"
    _fb_link  = f"https://www.facebook.com/sharer/sharer.php?u={_url_enc}"
    _mail_sub = urllib.parse.quote("Resultado da Simulação Solar — SolarMT")
    _mail_body= urllib.parse.quote(
        f"{_share_text}\n\nAcesse: {_share_url}\n\n"
        f"--- Dados da simulação ---\n"
        f"Cidade: {f['cidade']}\n"
        f"Consumo: {consumo} kWh/mês\n"
        f"Painéis: {n_paineis} x 400 Wp = {kwp:.2f} kWp\n"
        f"Área necessária: {area_nec:.0f} m²\n"
        f"Geração mensal est.: {ger_mes:,} kWh\n"
        f"Economia mensal: R$ {eco_mes:,}\n"
        f"Custo do sistema: R$ {custo:,.0f}\n"
        f"Payback: {payback} anos\n"
        f"VPL 25 anos: R$ {vpl_val:,.0f}\n"
        f"TIR: {tir_pct}% a.a.\n"
        f"CO₂ evitado 25 anos: {co2_25a} toneladas\n"
    )
    _mail_link= f"mailto:?subject={_mail_sub}&body={_mail_body}"

    components.html(f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600&display=swap');
      .share-row {{
        display: flex; gap: 10px; flex-wrap: wrap;
      }}
      .sbtn {{
        display: flex; align-items: center; gap: 8px;
        padding: 10px 18px; border-radius: 8px; border: none;
        font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600;
        cursor: pointer; text-decoration: none; transition: opacity .15s, transform .15s;
        white-space: nowrap;
      }}
      .sbtn:hover {{ opacity: .85; transform: translateY(-2px); }}
      .btn-wa   {{ background: #25d366; color: #fff; }}
      .btn-tw   {{ background: #1da1f2; color: #fff; }}
      .btn-li   {{ background: #0077b5; color: #fff; }}
      .btn-fb   {{ background: #1877f2; color: #fff; }}
      .btn-mail {{ background: #374151; color: #e8f0ff; border: 1px solid rgba(255,255,255,.15); }}
      .btn-copy {{ background: #111e38; color: #f59e0b;
                   border: 1px solid rgba(245,158,11,.4); }}
      .copied   {{ background: #10b981 !important; color: #fff !important; border-color: transparent !important; }}
    </style>
    <div class="share-row">
      <a class="sbtn btn-wa"   href="{_wa_link}"   target="_blank">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
          <path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.558 4.117 1.532 5.843L.057 23.428a.5.5 0 0 0 .611.611l5.585-1.475A11.94 11.94 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.885 0-3.656-.51-5.176-1.4l-.37-.22-3.836 1.013 1.013-3.836-.22-.37A10 10 0 1 1 12 22z"/>
        </svg>
        WhatsApp
      </a>
      <a class="sbtn btn-tw"   href="{_tw_link}"   target="_blank">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </svg>
        Twitter / X
      </a>
      <a class="sbtn btn-li"   href="{_li_link}"   target="_blank">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
        LinkedIn
      </a>
      <a class="sbtn btn-fb"   href="{_fb_link}"   target="_blank">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
        </svg>
        Facebook
      </a>
      <a class="sbtn btn-mail" href="{_mail_link}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
        </svg>
        E-mail
      </a>
      <button class="sbtn btn-copy" id="cpbtn"
        onclick="navigator.clipboard.writeText('{_share_url}').then(()=>{{
          var b=document.getElementById('cpbtn');
          b.textContent='✓ Link copiado!';
          b.classList.add('copied');
          setTimeout(()=>{{b.textContent='🔗 Copiar link';b.classList.remove('copied');}},2500);
        }})">
        🔗 Copiar link
      </button>
    </div>
    """, height=60)

    st.markdown("---")
    br1, br2 = st.columns([1,1])
    with br1:
        if st.button("← Refazer Cálculo", type="secondary", use_container_width=True):
            st.session_state.step = 1
            st.session_state.form = {}
            st.rerun()
    with br2:
        import streamlit.components.v1 as components
        components.html("""
        <button onclick="window.parent.window.print()"
            style="width:100%;padding:11px 26px;background:#f59e0b;color:#08101e;
                   border:none;border-radius:8px;
                   font-family:'Sora',sans-serif;
                   font-size:14px;font-weight:600;cursor:pointer;
                   display:flex;align-items:center;justify-content:center;gap:8px;
                   transition:background .2s;">
            🖨️&nbsp; Imprimir / Salvar PDF
        </button>
        """, height=50)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="footer-brand">SolarMT — Lucas do Rio Verde/MT</div>
  <p>
    Criado por
    <a href="https://www.instagram.com/srkennedydc/" target="_blank">Atlas Kennedy</a> & co-autorado por 
        <a href='https://www.instagram.com/angelicasantos.r/' target='_blank' style='color: #ffc107; text-decoration: none;'>Angélica Santos</a></p>
    — Graduandos em Ciência e Tecnologia ·
    <strong style="color:#e8f0ff;">UFMT — Universidade Federal de Mato Grosso</strong>
  </p>
  <p style="margin-top:4px;opacity:.7;font-size:11px;">
    Seminário Integrador IV · BCT/UFMT · 2026 · GNU GPL v3.0 (Software Livre)<br>
    Dados de irradiação: INMET / CRESESB · Tarifa: ENERGISA-MT · Emissão CO₂: ONS 2023
  </p>
</div>
""", unsafe_allow_html=True)
