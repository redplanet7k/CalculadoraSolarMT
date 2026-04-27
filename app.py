"""
app.py — SolarMT | Calculadora de Viabilidade Solar Fotovoltaica
Design baseado no protótipo HTML do projeto SolarMT — BCT/UFMT
Criado por Atlas Kennedy — Graduando em Ciência e Tecnologia · UFMT
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
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input{
  background:rgba(255,255,255,0.06)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:8px!important;
  color:var(--text)!important;
  font-family:'Sora',sans-serif!important;
}
div[data-testid="stNumberInput"] input:focus{border-color:var(--amber)!important;}
div[data-testid="stSelectbox"] div[data-baseweb="select"]>div{
  background:rgba(255,255,255,0.06)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:8px!important;
  color:var(--text)!important;
}
label[data-testid="stWidgetLabel"] p{
  font-size:11px!important;font-weight:600!important;
  color:var(--muted)!important;text-transform:uppercase;
  letter-spacing:.07em!important;
}
div[data-testid="stSlider"] p{color:var(--muted)!important;}
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

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Retorno Acumulado", "🥧 Distribuição do Custo",
                                       "☀️ Geração vs Consumo", "🔬 Análise Técnica"])

    # ── Chart 1: Retorno Acumulado ────────────────────────────────
    with tab1:
        anos_l = ["Ano 0"] + [f"Ano {t}" for t in range(1, LIFE+1)]
        acum_ret = [-custo]
        acum = -custo
        for t in range(1, LIFE+1):
            acum += eco_ano * (1+INF)**(t-1)
            acum_ret.append(round(acum))

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=anos_l, y=acum_ret,
            mode="lines", name="Retorno Acumulado",
            line=dict(color=AMBER, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(245,158,11,0.08)",
        ))
        fig1.add_trace(go.Scatter(
            x=anos_l, y=[0]*(LIFE+1),
            mode="lines", name="Zero",
            line=dict(color="rgba(255,255,255,0.15)", dash="dash", width=1),
            showlegend=False,
        ))
        # Payback marker — add_shape evita erro com eixo categórico
        pb_year = round(payback)
        if 1 <= pb_year <= LIFE:
            fig1.add_shape(
                type="line",
                x0=pb_year, x1=pb_year, y0=0, y1=1,
                xref="x", yref="paper",
                line=dict(dash="dot", color=GREEN, width=2),
            )
            fig1.add_annotation(
                x=pb_year, y=0.98,
                xref="x", yref="paper",
                text=f"Payback ≈ Ano {pb_year}",
                showarrow=False, yanchor="top",
                font=dict(color=GREEN, size=11),
            )
        fig1.update_layout(
            title="Retorno Acumulado — 25 anos (R$)",
            yaxis_title="R$",
            showlegend=False,
        )
        theme(fig1, height=280)
        st.plotly_chart(fig1, use_container_width=True)

        # Tabela resumo do fluxo (anos selecionados)
        check_anos = [1,3,5,8,10,12,15,20,25]
        df_ret = pd.DataFrame({
            "Ano": [f"Ano {a}" for a in check_anos],
            "Retorno Acum. (R$)": [f"R$ {acum_ret[a]:,.0f}" for a in check_anos],
            "Status": ["✅ Positivo" if acum_ret[a] >= 0 else "🔴 Negativo" for a in check_anos],
        })
        st.dataframe(df_ret, use_container_width=True, hide_index=True)

    # ── Chart 2: Donut custo ──────────────────────────────────────
    with tab2:
        labels_pie = ["Equipamentos 60%", "Projeto/Instalação 25%", "Mão de obra 15%"]
        values_pie = [custo*0.60, custo*0.25, custo*0.15]
        fig2 = go.Figure(go.Pie(
            labels=labels_pie, values=values_pie, hole=0.55,
            marker_colors=[AMBER, BLUE, GREEN],
            textfont=dict(color=TEXT, size=11),
        ))
        fig2.update_layout(
            title="Distribuição do Custo do Sistema",
            legend=dict(orientation="h", y=-0.15, font=dict(color=MUTED)),
        )
        theme(fig2, height=300)
        st.plotly_chart(fig2, use_container_width=True)

        df_custo = pd.DataFrame({
            "Componente": labels_pie,
            "Valor (R$)": [f"R$ {v:,.0f}" for v in values_pie],
            "Proporção": ["60%", "25%", "15%"],
        })
        st.dataframe(df_custo, use_container_width=True, hide_index=True)

    # ── Chart 3: Geração mensal vs consumo ───────────────────────
    with tab3:
        ger_meses = [round(ger_mes * s) for s in SAZON]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=MESES_CURTOS, y=ger_meses,
            name="Geração Est.", marker_color="rgba(245,158,11,0.75)",
            marker_line_color=AMBER, marker_line_width=1,
        ))
        fig3.add_trace(go.Bar(
            x=MESES_CURTOS, y=[consumo]*12,
            name="Consumo", marker_color="rgba(96,165,250,0.45)",
            marker_line_color=BLUE, marker_line_width=1,
        ))
        fig3.add_trace(go.Scatter(
            x=MESES_CURTOS, y=ger_meses,
            mode="lines+markers",
            line=dict(color=AMBER, width=2),
            marker=dict(size=6, color=AMBER),
            name="Geração (curva)", showlegend=False,
        ))
        fig3.update_layout(
            title="Geração Mensal Estimada vs Consumo (kWh)",
            barmode="group", yaxis_title="kWh",
            legend=dict(orientation="h", y=-0.22),
        )
        theme(fig3, height=280)
        st.plotly_chart(fig3, use_container_width=True)

        irr_vals = list(IRRADIANCIA_MENSAL.values())
        df_ger = pd.DataFrame({
            "Mês": MESES_CURTOS,
            "HSP (kWh/m²/dia)": irr_vals,
            "Fator sazonal": SAZON,
            "Geração Est. (kWh)": ger_meses,
            "Consumo (kWh)": [consumo]*12,
            "Saldo (kWh)": [g - consumo for g in ger_meses],
        })
        st.dataframe(df_ger, use_container_width=True, hide_index=True)

    # ── Chart 4: Análise técnica ──────────────────────────────────
    with tab4:
        ang = angulo_otimo()
        per = resumo_perdas()

        c4a, c4b = st.columns(2)
        with c4a:
            # Ângulo ótimo
            fig_ang = go.Figure(go.Scatter(
                x=ang["betas"], y=ang["irradiancias"],
                mode="lines", line=dict(color=AMBER, width=2.5),
                fill="tozeroy", fillcolor="rgba(245,158,11,0.08)",
            ))
            fig_ang.add_vline(x=ang["angulo_otimo_graus"], line_dash="dash",
                              line_color=GREEN,
                              annotation_text=f"β*={ang['angulo_otimo_graus']}°",
                              annotation_font_color=GREEN)
            fig_ang.update_layout(title="Ângulo Ótimo de Inclinação (Cálculo III)",
                                  xaxis_title="β (graus)", yaxis_title="kWh/m²/dia")
            theme(fig_ang, height=260)
            st.plotly_chart(fig_ang, use_container_width=True)

        with c4b:
            # Perdas do sistema
            labels_p = [k for k in per if k != "Total"]
            vals_p   = [per[k] for k in labels_p]
            fig_per = go.Figure(go.Bar(
                x=labels_p, y=vals_p,
                marker_color=["rgba(248,113,113,0.8)"]*len(labels_p),
                marker_line_color="#f87171", marker_line_width=1,
                text=[f"{v}%" for v in vals_p], textposition="outside",
                textfont=dict(color=MUTED),
            ))
            fig_per.update_layout(title=f"Perdas do Sistema — Total {per['Total']}% (Física III)",
                                  yaxis_title="Perda (%)")
            theme(fig_per, height=260)
            st.plotly_chart(fig_per, use_container_width=True)

        # Temperatura
        temps = np.arange(25, 75, 1)
        perda_t = [perda_por_temperatura(float(t)) for t in temps]
        fig_tmp = go.Figure(go.Scatter(
            x=temps, y=perda_t, mode="lines",
            line=dict(color="#f87171", width=2),
            fill="tozeroy", fillcolor="rgba(248,113,113,0.08)",
        ))
        fig_tmp.add_vline(x=TEMP_OPERACAO_LOCAL, line_dash="dash", line_color=AMBER,
                          annotation_text=f"T_op={TEMP_OPERACAO_LOCAL}°C → {per['Temperatura']}% perda",
                          annotation_font_color=AMBER)
        fig_tmp.update_layout(title="Perda de Potência por Temperatura — αT = −0,35%/°C (Física III)",
                              xaxis_title="Temperatura (°C)", yaxis_title="Perda (%)")
        theme(fig_tmp, height=240)
        st.plotly_chart(fig_tmp, use_container_width=True)

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
    st.markdown("---")
    br1, br2 = st.columns([1,1])
    with br1:
        if st.button("← Refazer Cálculo", type="secondary", use_container_width=True):
            st.session_state.step = 1
            st.session_state.form = {}
            st.rerun()
    with br2:
        st.markdown("""
        <div style="text-align:right;padding-top:6px;">
          <small style="color:#3d5280;">
            💡 Use Ctrl+P ou o menu do navegador para imprimir / salvar em PDF
          </small>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="footer-brand">SolarMT — Lucas do Rio Verde/MT</div>
  <p>
    Criado por
    <a href="https://www.instagram.com/_atlaskennedydc" target="_blank">Atlas Kennedy</a>
    — Graduando em Ciência e Tecnologia ·
    <strong style="color:#e8f0ff;">UFMT — Universidade Federal de Mato Grosso</strong>
  </p>
  <p style="margin-top:4px;opacity:.7;font-size:11px;">
    Seminário Integrador IV · BCT/UFMT · 2026 · GNU GPL v3.0 (Software Livre)<br>
    Dados de irradiação: INMET / CRESESB · Tarifa: ENERGISA-MT · Emissão CO₂: ONS 2023
  </p>
</div>
""", unsafe_allow_html=True)
