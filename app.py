"""
app.py — SolarMT | Sistema de Apoio à Decisão de Engenharia Solar Fotovoltaica
BC&T · UFMT · Seminário Integrador IV · 2026
Atlas Brasileiro de Energia Solar — INPE/LABREN 2017 | DOI: 10.34024/978851700089
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dados_solar_mt import buscar_dados_municipio, MUNICIPIOS
from data import (MESES, DIAS_POR_MES, TARIFA_ENERGIA_KWH, VIDA_UTIL_ANOS,
                  PERDA_INVERSOR, PERDA_CABEAMENTO, PERDA_SOMBREAMENTO,
                  PERDA_SUJEIRA, PERDA_TEMPERATURA, FATOR_DESEMPENHO,
                  MODULO_POTENCIA_WP, MODULO_AREA_M2, TEMP_OPERACAO_LOCAL,
                  TEMP_REFERENCIA, custo_por_kwp)
from calculations import resumo_perdas
from financial import (calcular_investimento, calcular_fluxo_caixa,
                       calcular_payback, calcular_vpl, calcular_tir, co2_evitado)

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="SolarMT", page_icon="☀️",
                   layout="wide", initial_sidebar_state="collapsed")

if "step" not in st.session_state:       st.session_state.step = 1
if "form" not in st.session_state:       st.session_state.form = {}
if "modal_fechado" not in st.session_state: st.session_state.modal_fechado = False

# ── Paleta ──────────────────────────────────────────────────────────────────
BG="#f0f5fb"; BG2="#ffffff"; BG3="#e4edf8"
BLUE="#1d6fbf"; BLUE2="#2580d6"; BLUED="#0d3d6e"
GREEN="#16a34a"; ORANGE="#ea8000"; RED="#dc2626"
MUTED="#5a7099"; TEXT="#1a2744"; GRID="rgba(29,111,191,0.06)"

def theme(fig, h=280):
    fig.update_layout(paper_bgcolor=BG2, plot_bgcolor="#f8fbff",
        font=dict(family="Inter,sans-serif", color=TEXT, size=11),
        legend=dict(bgcolor=BG2, bordercolor="#c8d9ef", font=dict(color=MUTED, size=10)),
        height=h, margin=dict(l=8,r=8,t=38,b=8))
    fig.update_xaxes(gridcolor=GRID, zerolinecolor="#c8d9ef",
                     linecolor="#c8d9ef", tickfont=dict(color=MUTED,size=10))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor="#c8d9ef",
                     linecolor="#c8d9ef", tickfont=dict(color=MUTED,size=10))
    return fig

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root{
  --bg:#f0f5fb;--bg2:#fff;--bg3:#e4edf8;--card:#fff;--cb:#c8d9ef;
  --text:#1a2744;--muted:#5a7099;--dim:#9ab0cc;
  --blue:#1d6fbf;--blue2:#2580d6;--blued:#0d3d6e;
  --bbg:#deeaf8;--bbd:#a8c8ee;
  --green:#16a34a;--gbg:#dcfce7;--gbd:#86efac;
  --orange:#ea8000;--obg:#fff3e0;--obd:#fbbf70;
  --red:#dc2626;--rbg:#fee2e2;--rbd:#fca5a5;
}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background-color:var(--bg)!important;color:var(--text)!important;}
.stApp{background-color:var(--bg)!important;}
#MainMenu,footer,header[data-testid="stHeader"]{display:none!important;}
section[data-testid="stSidebar"]{display:none!important;}
.block-container{max-width:900px!important;padding:0 16px 80px!important;margin:0 auto!important;}

.topbar{padding:14px 0 12px;display:flex;align-items:center;gap:12px;border-bottom:2px solid var(--cb);background:var(--bg);}
.logo-icon{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#1d6fbf,#0d3d6e);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}
.logo-text{font-size:17px;font-weight:700;color:var(--blued);}
.logo-text span{color:var(--blue);}
.htag{margin-left:auto;font-size:10px;color:var(--muted);background:var(--bg3);border:1px solid var(--cb);border-radius:20px;padding:3px 12px;white-space:nowrap;}

.hero{text-align:center;padding:30px 16px 16px;}
.hero h1{font-size:clamp(20px,5vw,33px);font-weight:700;background:linear-gradient(135deg,var(--blued) 20%,var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:8px;line-height:1.2;}
.hero p{color:var(--muted);font-size:13px;max-width:540px;margin:0 auto 14px;}
.hero-badges{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;}
.badge{background:var(--bg3);border:1px solid var(--bbd);border-radius:20px;padding:4px 12px;font-size:11px;color:var(--blue);font-weight:500;}

.stepper{display:flex;align-items:center;justify-content:center;padding:16px;max-width:460px;margin:0 auto 20px;}
.step{display:flex;align-items:center;gap:7px;}
.snum{width:32px;height:32px;border-radius:50%;background:#e4edf8;border:1.5px solid var(--dim);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;color:var(--dim);}
.slabel{font-size:12px;color:var(--dim);font-weight:500;}
.step.active .snum{background:var(--blue);border-color:var(--blue);color:#fff;}
.step.active .slabel{color:var(--blue);font-weight:600;}
.step.done .snum{background:var(--green);border-color:var(--green);color:#fff;}
.step.done .slabel{color:var(--green);}
.sline{flex:1;height:2px;background:var(--dim);margin:0 8px;min-width:28px;border-radius:2px;}
.sline.done{background:var(--green);}

.card{background:var(--card);border:1px solid var(--cb);border-radius:14px;padding:22px 20px;margin-bottom:14px;box-shadow:0 1px 6px rgba(29,111,191,0.07);}
.card-h{font-size:16px;font-weight:600;margin-bottom:4px;color:var(--blued);}
.card-sub{font-size:13px;color:var(--muted);margin-bottom:18px;}

.geo-card{background:var(--bbg);border:1px solid var(--bbd);border-radius:12px;padding:14px 16px;margin-bottom:14px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;}
.geo-item{display:flex;flex-direction:column;gap:2px;min-width:80px;}
.geo-label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;}
.geo-value{font-size:17px;font-weight:700;color:var(--blued);}
.geo-sub{font-size:10px;color:var(--muted);}
.geo-badge{background:var(--blue);color:#fff;font-size:10px;border-radius:20px;padding:2px 10px;font-weight:600;white-space:nowrap;}

.mg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:12px;}
.mc{border-radius:12px;padding:14px 12px;background:#fff;border:1px solid var(--cb);box-shadow:0 1px 4px rgba(29,111,191,0.06);}
.mc.a{background:var(--obg);border-color:var(--obd);}
.mc.g{background:var(--gbg);border-color:var(--gbd);}
.mc.b{background:var(--bbg);border-color:var(--bbd);}
.ml{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px;}
.mv{font-size:19px;font-weight:700;line-height:1.2;color:var(--blued);}
.mc.a .mv{color:var(--orange);}
.mc.g .mv{color:var(--green);}
.mc.b .mv{color:var(--blue);}
.mu{font-size:10px;color:var(--dim);margin-top:2px;}

.tir-card{display:flex;align-items:center;gap:16px;background:var(--gbg);border:1px solid var(--gbd);border-radius:12px;padding:16px 18px;margin-bottom:12px;flex-wrap:wrap;}
.tir-val{font-size:28px;font-weight:700;color:var(--green);}
.tir-msg{flex:1;min-width:200px;font-size:12px;color:#166534;line-height:1.5;}

.ibox{background:var(--bbg);border:1px solid var(--bbd);border-radius:8px;padding:12px 14px;font-size:13px;color:var(--blued);margin-bottom:12px;line-height:1.6;}
.ibox-w{background:var(--obg);border:1px solid var(--obd);border-radius:8px;padding:12px 14px;font-size:13px;color:#7c3b00;margin-bottom:12px;line-height:1.6;}
.ibox-r{background:var(--rbg);border:1px solid var(--rbd);border-radius:8px;padding:12px 14px;font-size:13px;color:var(--red);margin-bottom:12px;}
.atlas-tag{display:inline-block;background:var(--gbg);border:1px solid var(--gbd);color:var(--green);font-size:10px;border-radius:20px;padding:2px 10px;margin-left:6px;vertical-align:middle;font-weight:600;}

.disc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px;}
.dcard{border-radius:8px;padding:12px;border:1px solid;}
.da{background:var(--obg);border-color:var(--obd);}
.db{background:var(--bbg);border-color:var(--bbd);}
.dg{background:var(--gbg);border-color:var(--gbd);}
.dp{background:#f5f0ff;border-color:#c4b5fd;}
.full{grid-column:span 2;}
.dcard h4{font-size:12px;font-weight:600;margin-bottom:4px;}
.da h4{color:var(--orange);}.db h4{color:var(--blue);}.dg h4{color:var(--green);}.dp h4{color:#7c3aed;}
.dcard p{font-size:11px;color:var(--muted);line-height:1.5;}

.footer{margin-top:36px;padding:20px 0 14px;border-top:2px solid var(--cb);text-align:center;color:var(--muted);font-size:12px;line-height:1.9;}
.footer a{color:var(--blue);text-decoration:none;font-weight:600;}
.footer a:hover{text-decoration:underline;}
.footer-brand{color:var(--blued);font-weight:700;font-size:14px;margin-bottom:4px;}
.footer-team{font-size:11px;color:var(--dim);margin-top:4px;}

input,textarea{background:#fff!important;color:var(--text)!important;caret-color:var(--blue)!important;}
div[data-testid="stNumberInput"] input{background:#fff!important;border:1.5px solid var(--cb)!important;border-radius:8px!important;color:var(--text)!important;font-size:15px!important;-webkit-text-fill-color:var(--text)!important;min-height:44px!important;}
div[data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#fff!important;border:1.5px solid var(--cb)!important;border-radius:8px!important;color:var(--text)!important;min-height:44px!important;}
div[data-testid="stSelectbox"] div[data-baseweb="select"] *{color:var(--text)!important;}
label[data-testid="stWidgetLabel"] p{font-size:11px!important;font-weight:600!important;color:var(--muted)!important;text-transform:uppercase;letter-spacing:.06em!important;}
div[data-testid="stSlider"] p{color:var(--muted)!important;}
div[data-testid="stButton"]>button{border-radius:8px!important;font-family:'Inter',sans-serif!important;font-weight:600!important;font-size:14px!important;padding:10px 22px!important;min-height:44px!important;transition:all .2s!important;}
div[data-testid="stButton"]>button[kind="primary"]{background:var(--blue)!important;color:#fff!important;border:none!important;}
div[data-testid="stButton"]>button[kind="primary"]:hover{background:var(--blue2)!important;box-shadow:0 4px 14px rgba(29,111,191,0.3)!important;}
div[data-testid="stButton"]>button[kind="secondary"]{background:#fff!important;color:var(--muted)!important;border:1.5px solid var(--cb)!important;}
div[data-testid="stTabs"] button{color:var(--muted)!important;font-size:12px!important;}
div[data-testid="stTabs"] button[aria-selected="true"]{color:var(--blue)!important;border-bottom-color:var(--blue)!important;font-weight:600!important;}
div[data-testid="stTabs"]>div:first-child{overflow-x:auto!important;flex-wrap:nowrap!important;scrollbar-width:none;}
div[data-testid="stExpander"]{background:#fff!important;border:1px solid var(--cb)!important;border-radius:10px!important;}

@media(max-width:680px){
  .mg{grid-template-columns:1fr 1fr!important;}
  .disc-grid{grid-template-columns:1fr!important;}
  .full{grid-column:span 1!important;}
  .hero h1{font-size:22px;} .tir-card{flex-direction:column;gap:8px;}
  .htag,.geo-badge{display:none;}
  .geo-card{flex-direction:column;gap:8px;}
  div[data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;}
  div[data-testid="stHorizontalBlock"]>div{min-width:100%!important;flex:1 1 100%!important;}
  .card{padding:16px 14px;} .mv{font-size:17px;}
}
@media(max-width:380px){.mg{grid-template-columns:1fr!important;}}
</style>
""", unsafe_allow_html=True)

# ── Topbar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="logo-icon">☀️</div>
  <span class="logo-text">Solar<span>MT</span></span>
  <div class="htag">BC&T · UFMT · Seminário Integrador IV · 2026</div>
</div>
<div class="hero">
  <h1>Calculadora de Viabilidade<br>Solar Fotovoltaica</h1>
  <p>Sistema de Apoio à Decisão de Engenharia com dados reais do
  <strong>Atlas Brasileiro de Energia Solar</strong> (INPE/LABREN 2017) —
  141 municípios do Mato Grosso georreferenciados via CSV.</p>
  <div class="hero-badges">
    <span class="badge">⚡ Física III</span>
    <span class="badge">∫ Cálculo III</span>
    <span class="badge">💰 Mat. Financeira</span>
    <span class="badge">📊 Prob. e Estatística</span>
    <span class="badge">🧠 Gestão do Conhecimento</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Modal de boas-vindas (primeira visita) ──────────────────────────────────
if not st.session_state.modal_fechado:
    import streamlit.components.v1 as _comp_modal
    _comp_modal.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    .overlay{
      position:fixed;inset:0;
      background:rgba(13,61,110,0.55);
      backdrop-filter:blur(4px);
      display:flex;align-items:center;justify-content:center;
      z-index:99999;padding:16px;
      animation:fadeIn .25s ease;
    }
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    .modal{
      background:#fff;border-radius:20px;
      max-width:520px;width:100%;
      box-shadow:0 24px 60px rgba(13,61,110,0.22);
      overflow:hidden;
      animation:slideUp .3s ease;
    }
    @keyframes slideUp{from{transform:translateY(30px);opacity:0}to{transform:translateY(0);opacity:1}}
    .modal-header{
      background:linear-gradient(135deg,#0d3d6e 0%,#1d6fbf 100%);
      padding:28px 28px 22px;text-align:center;
    }
    .modal-icon{font-size:44px;margin-bottom:10px;}
    .modal-title{color:#fff;font-family:'Inter',sans-serif;font-size:20px;font-weight:700;
      line-height:1.2;margin-bottom:6px;}
    .modal-sub{color:rgba(255,255,255,0.80);font-family:'Inter',sans-serif;font-size:13px;}
    .modal-body{padding:24px 28px;}
    .project-badge{
      display:inline-flex;align-items:center;gap:8px;
      background:#e4edf8;border:1.5px solid #a8c8ee;
      border-radius:30px;padding:6px 14px;
      font-family:'Inter',sans-serif;font-size:11px;font-weight:600;
      color:#0d3d6e;margin-bottom:18px;
    }
    .desc{font-family:'Inter',sans-serif;font-size:14px;color:#334155;
      line-height:1.7;margin-bottom:18px;}
    .desc strong{color:#0d3d6e;}
    .pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px;}
    .pill{background:#f0f5fb;border:1px solid #c8d9ef;border-radius:20px;
      padding:5px 13px;font-family:'Inter',sans-serif;font-size:11px;
      color:#1d6fbf;font-weight:500;}
    .team{background:#f8fbff;border-radius:10px;padding:12px 16px;
      margin-bottom:22px;border:1px solid #deeaf8;}
    .team-label{font-family:'Inter',sans-serif;font-size:10px;font-weight:600;
      text-transform:uppercase;letter-spacing:.07em;color:#5a7099;margin-bottom:6px;}
    .team-names{font-family:'Inter',sans-serif;font-size:13px;color:#1a2744;
      font-weight:500;line-height:1.6;}
    .btn-entrar{
      width:100%;padding:14px;
      background:linear-gradient(135deg,#1d6fbf,#0d3d6e);
      color:#fff;border:none;border-radius:10px;
      font-family:'Inter',sans-serif;font-size:15px;font-weight:700;
      cursor:pointer;letter-spacing:.02em;
      box-shadow:0 4px 16px rgba(29,111,191,0.35);
      transition:opacity .15s,transform .15s;
    }
    .btn-entrar:hover{opacity:.9;transform:translateY(-1px);}
    .modal-footer{text-align:center;padding:0 28px 20px;
      font-family:'Inter',sans-serif;font-size:11px;color:#9ab0cc;}
    .modal-footer a{color:#1d6fbf;text-decoration:none;font-weight:600;}
    </style>

    <div class="overlay" id="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-icon">☀️</div>
          <div class="modal-title">Bem-vindo ao SolarMT</div>
          <div class="modal-sub">Calculadora de Viabilidade Solar Fotovoltaica</div>
        </div>
        <div class="modal-body">
          <div style="text-align:center;margin-bottom:16px">
            <span class="project-badge">
              🎓 Projeto Acadêmico · BC&T · UFMT
            </span>
          </div>
          <p class="desc">
            Esta calculadora faz parte do <strong>Seminário Integrador IV</strong>
            do curso de <strong>Bacharelado em Ciência e Tecnologia</strong> da
            <strong>Universidade Federal de Mato Grosso (UFMT)</strong> —
            campus de Lucas do Rio Verde/MT.
          </p>
          <p class="desc" style="margin-top:-8px">
            Nosso objetivo é <strong>democratizar o acesso à informação</strong>
            sobre energia solar fotovoltaica, permitindo que qualquer pessoa —
            produtor rural, morador ou empresa — possa simular o custo,
            a geração e o retorno de um sistema solar sem precisar contratar
            uma consultoria especializada.
          </p>
          <div class="pills">
            <span class="pill">⚡ Dados reais do Atlas INPE 2017</span>
            <span class="pill">📍 141 municípios do MT</span>
            <span class="pill">💰 Preços reais de mercado</span>
            <span class="pill">🆓 100% gratuito</span>
          </div>
          <div class="team">
            <div class="team-label">👥 Equipe de Desenvolvimento</div>
            <div class="team-names">
              Messias Kennedy · Angélica Santos · Karleia · Viviane
            </div>
          </div>
          <button class="btn-entrar" onclick="
            document.getElementById('modal-overlay').style.display='none';
            window.parent.postMessage({type:'streamlit:setComponentValue',value:true},'*');
          ">
            ☀️ Começar simulação gratuita
          </button>
        </div>
        <div class="modal-footer">
          Dados: <a href="http://doi.org/10.34024/978851700089" target="_blank">Atlas INPE/LABREN 2017</a>
          &nbsp;·&nbsp; Licença: GNU GPL v3.0
        </div>
      </div>
    </div>
    """, height=620)

    # Botão Streamlit real para fechar o modal
    col_m1, col_m2, col_m3 = st.columns([1,2,1])
    with col_m2:
        if st.button("☀️ Começar simulação gratuita", type="primary",
                     use_container_width=True, key="btn_modal"):
            st.session_state.modal_fechado = True
            st.rerun()
    st.stop()

# ── Stepper ──────────────────────────────────────────────────────────────────
def render_stepper(s):
    lbls = ["Consumo","Instalação","Resultados"]
    h = '<div class="stepper">'
    for i,lb in enumerate(lbls,1):
        cls = "active" if i==s else ("done" if i<s else "")
        h += f'<div class="step {cls}"><div class="snum">{"✓" if i<s else i}</div><span class="slabel">{lb}</span></div>'
        if i<3: h += f'<div class="sline {"done" if s>i else ""}"></div>'
    st.markdown(h+"</div>", unsafe_allow_html=True)

render_stepper(st.session_state.step)

# ══════════════════════════════════════════════════════════════════
# ETAPA 1 — CONSUMO
# ══════════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="card"><div class="card-h">⚡ Dados de Consumo</div>'
                '<div class="card-sub">Selecione o município e informe os dados da sua conta de energia.</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        idx_default = MUNICIPIOS.index("Lucas do Rio Verde") if "Lucas do Rio Verde" in MUNICIPIOS else 0
        cidade = st.selectbox("Município — Mato Grosso", MUNICIPIOS, index=idx_default,
            help="141 municípios com dados reais do Atlas Brasileiro de Energia Solar (INPE 2017)")
    with c2:
        tipo = st.selectbox("Tipo de Propriedade",
            ["Residencial","Rural / Produtor","Comercial / Industrial"])

    # Geo Card em tempo real
    dc = buscar_dados_municipio(cidade)
    lat_c=dc["lat"]; lon_c=dc["lon"]; ghi_c=dc["global"]
    hs = "S" if lat_c<0 else "N"; hm = "O" if lon_c<0 else "L"
    st.markdown(f"""
    <div class="geo-card">
      <div class="geo-item"><span class="geo-label">📍 Latitude</span>
        <span class="geo-value">{abs(lat_c):.2f}°{hs}</span></div>
      <div class="geo-item"><span class="geo-label">📍 Longitude</span>
        <span class="geo-value">{abs(lon_c):.2f}°{hm}</span></div>
      <div class="geo-item"><span class="geo-label">☀️ GHI Médio Anual</span>
        <span class="geo-value">{ghi_c:.2f}</span>
        <span class="geo-sub">kWh/m²/dia</span></div>
      <div class="geo-item"><span class="geo-label">📐 Ângulo Ótimo</span>
        <span class="geo-value">{abs(lat_c):.1f}°</span>
        <span class="geo-sub">inclinação norte</span></div>
      <div style="margin-left:auto"><span class="geo-badge">Atlas INPE 2017 · CSV</span></div>
    </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        consumo = st.number_input("Consumo Médio Mensal (kWh)", 50, 100000, 350, 10,
            help='Campo "Consumo" da sua conta de energia — média dos últimos 12 meses')
    with c4:
        tarifa = st.number_input("Tarifa de Energia (R$/kWh)", 0.20, 5.00, 0.87, 0.01,
            format="%.2f", help="ENERGISA MT — Subgrupo B1 Residencial 2025: R$ 0,87/kWh")

    st.markdown("</div>", unsafe_allow_html=True)
    _, bc = st.columns([3,1])
    with bc:
        if st.button("Próximo →", type="primary", use_container_width=True):
            st.session_state.form.update({"cidade":cidade,"tipo":tipo,
                "consumo":consumo,"tarifa":tarifa,"dados_cidade":dc})
            st.session_state.step = 2; st.rerun()

# ══════════════════════════════════════════════════════════════════
# ETAPA 2 — INSTALAÇÃO
# ══════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="card"><div class="card-h">🏠 Dados de Instalação</div>'
                '<div class="card-sub">Configure os parâmetros técnicos e financeiros do projeto.</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        area = st.number_input("Área Disponível no Telhado (m²)", 0, 50000, 0, 5,
            help="Cada painel ocupa ≈ 2,56 m². Deixe 0 para calcular automaticamente.")
    with c2:
        orcamento = st.number_input("Orçamento Máximo (R$) — Opcional", 0, 9999999, 0, 1000,
            help="Deixe 0 para calcular o sistema ideal sem limite financeiro.")

    # Fator Derate — exigência da tutora
    st.markdown('<div style="background:#f0f7ff;border:1.5px solid #a8c8ee;border-radius:10px;padding:14px 16px;margin-bottom:14px">',
                unsafe_allow_html=True)
    derate = st.slider("⚙️ Fator Derate — Eficiência Real do Sistema (%)",
        75, 85, 80, 1,
        help="Perdas combinadas: térmicas + sujeira + cabeamento + inversor + sombreamento. "
             "Atlas Brasileiro recomenda 80% para sistemas bem instalados (Fig.52, p.57).")
    st.markdown(f"""<div style="font-size:11px;color:#5a7099;margin-top:4px">
      <strong>{derate}%</strong> →
      Temperatura {round(abs(-0.0035)*(45-25)*100,1)}% +
      Sujeira 2,0% + Cabeamento 1,5% + Inversor 3,0% + Sombreamento 2,5%
    </div></div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        modalidade = st.selectbox("Modalidade de Compra",
            ["À vista","Financiado (BNDES / banco)","Consórcio","Leasing solar"])
    with c4:
        inflacao = st.slider("Inflação da Energia (% a.a.)", 1.0, 15.0, 6.5, 0.5,
            help="Histórico ANEEL 2015–2025 ≈ 6,5% a.a.") / 100

    taxa_desc = st.slider("Taxa de Desconto / SELIC (% a.a.)", 5.0, 20.0, 12.0, 0.5) / 100

    taxa_fin = prazo_fin = None
    if "Financiado" in modalidade:
        f1, f2 = st.columns(2)
        with f1:
            taxa_fin = st.number_input("Taxa de Juros Anual (%)", 0.0, 40.0, 10.0, 0.1,
                help="BNDES Mais Solar: ≈ 6–8% a.a.") / 100
        with f2:
            prazo_fin = st.number_input("Prazo (meses)", 12, 240, 60, 12)

    st.markdown("</div>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Anterior", type="secondary", use_container_width=True):
            st.session_state.step = 1; st.rerun()
    with b2:
        if st.button("☀️ Calcular Viabilidade", type="primary", use_container_width=True):
            st.session_state.form.update({"area":area,"orcamento":orcamento,
                "derate":derate/100,"modalidade":modalidade,
                "inflacao":inflacao,"taxa_desc":taxa_desc,
                "taxa_fin":taxa_fin,"prazo_fin":prazo_fin})
            st.session_state.step = 3; st.rerun()

# ══════════════════════════════════════════════════════════════════
# ETAPA 3 — RESULTADOS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    f   = st.session_state.form
    consumo   = f["consumo"]; tarifa = f["tarifa"]
    inflacao  = f["inflacao"]; taxa_desc = f["taxa_desc"]
    PR        = f["derate"]
    dc        = f["dados_cidade"]
    lat_c=dc["lat"]; lon_c=dc["lon"]; ghi_c=dc["global"]; mensal_c=dc["mensal"]

    # Atualiza módulos financeiros
    import financial as fin, data as dados
    dados.TARIFA_ENERGIA_KWH=tarifa; dados.INFLACAO_ENERGIA_AA=inflacao; dados.TAXA_DESCONTO=taxa_desc
    fin.TARIFA_ENERGIA_KWH=tarifa;   fin.INFLACAO_ENERGIA_AA=inflacao;   fin.TAXA_DESCONTO=taxa_desc

    # ── Dimensionamento ──────────────────────────────────────────────────
    # P_kWp = (Consumo × 1,10) / (GHI × PR × 30)   [Física III]
    pot_ideal = (consumo * 1.10) / (ghi_c * PR * 30)
    n = int(np.ceil(pot_ideal * 1000 / MODULO_POTENCIA_WP))
    if f["area"] > 0:     n = min(n, int(f["area"] / MODULO_AREA_M2))
    if f["orcamento"] > 0: n = min(n, int(f["orcamento"] / (custo_por_kwp(n*MODULO_POTENCIA_WP/1000)*MODULO_POTENCIA_WP/1000)))
    n = max(n, 1)
    kwp      = round(n * MODULO_POTENCIA_WP / 1000, 3)
    area_nec = round(n * MODULO_AREA_M2, 1)

    # ── Geração mensal com HSP real por município ────────────────────────
    # E_mes = P_kWp × HSP_mes × dias × PR  [Física III]
    ger = {m: round(kwp * mensal_c[m] * DIAS_POR_MES[i] * PR, 1) for i,m in enumerate(MESES)}
    ger_ano = round(sum(ger.values()), 1)
    eco = {m: round(min(v, consumo) * tarifa, 2) for m,v in ger.items()}
    eco_mes = round(np.mean(list(eco.values())), 2)
    cob = min(100, round(sum(ger.values())/12 / consumo * 100))

    # IC 95% (variabilidade interanual Atlas Fig.39)
    ic_lo = {m: round(max(v*0.91,0),1) for m,v in ger.items()}
    ic_hi = {m: round(v*1.09,1) for m,v in ger.items()}

    # ── Financeiro ───────────────────────────────────────────────────────
    inv = calcular_investimento(kwp)
    fc  = calcular_fluxo_caixa(ger_ano, consumo, inv["custo_total"])
    pb  = calcular_payback(fc["acumulado"], fc["fluxo_descontado"], inv["custo_total"])
    vpl = calcular_vpl(fc["fluxo_descontado"], inv["custo_total"])
    tir = calcular_tir(fc["fluxo_liquido"], inv["custo_total"])
    co2 = co2_evitado(ger_ano)
    per = resumo_perdas()

    pb_s = pb["payback_simples_anos"] or ">25"
    pb_d = pb["payback_descontado_anos"] or ">25"
    vpl_fmt = ("−" if vpl['vpl']<0 else "")+"R$ {:,.0f}".format(abs(vpl['vpl']))
    cor_vpl = GREEN if vpl["viavel"] else RED

    if tir>=15:   tir_txt="🟢 Excelente! Supera amplamente a Selic e renda fixa."
    elif tir>=10: tir_txt="🟢 Ótima rentabilidade. Superior à Selic histórica."
    elif tir>=7:  tir_txt="🟡 Boa rentabilidade. Comparável a CDBs de longo prazo."
    elif tir>=4:  tir_txt="🟡 Moderada. Avalie negociar o custo de instalação."
    else:         tir_txt="🔴 Baixa. Reduza o sistema ou busque outro orçamento."

    pmt_val = saldo_val = None
    if "Financiado" in f["modalidade"] and f.get("taxa_fin") and f.get("prazo_fin"):
        rm=f["taxa_fin"]/12; pf=int(f["prazo_fin"])
        pmt_val   = round(inv["custo_total"]*rm*(1+rm)**pf/((1+rm)**pf-1)) if rm>0 else round(inv["custo_total"]/pf)
        saldo_val = round(eco_mes - pmt_val)

    # ── Geo card resultado ───────────────────────────────────────────────
    hs="S" if lat_c<0 else "N"; hm="O" if lon_c<0 else "L"
    angot = round(abs(lat_c),1)
    st.markdown(f"""
    <div class="geo-card">
      <div class="geo-item"><span class="geo-label">📍 Município</span>
        <span class="geo-value" style="font-size:14px">{f["cidade"]}</span>
        <span class="geo-sub">{f["tipo"]}</span></div>
      <div class="geo-item"><span class="geo-label">Lat / Lon</span>
        <span class="geo-value" style="font-size:13px">{abs(lat_c):.2f}°{hs} · {abs(lon_c):.2f}°{hm}</span></div>
      <div class="geo-item"><span class="geo-label">☀️ GHI Médio</span>
        <span class="geo-value">{ghi_c:.2f}</span>
        <span class="geo-sub">kWh/m²/dia</span></div>
      <div class="geo-item"><span class="geo-label">⚙️ Derate</span>
        <span class="geo-value">{PR*100:.0f}%</span></div>
      <div class="geo-item"><span class="geo-label">📐 Ângulo Ótimo</span>
        <span class="geo-value">{angot}°</span>
        <span class="geo-sub">inclinação norte</span></div>
      <div style="margin-left:auto"><span class="geo-badge">Atlas INPE 2017</span></div>
    </div>""", unsafe_allow_html=True)

    if f["area"]>0 and area_nec>f["area"]:
        st.markdown(f'<div class="ibox-r">⚠️ Sistema limitado pela área ({f["area"]} m²). Área ideal: {area_nec:.0f} m².</div>',
                    unsafe_allow_html=True)

    # ── Métricas ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="mg">
      <div class="mc a"><div class="ml">Painéis</div><div class="mv">{n}</div><div class="mu">× 550 Wp monocristalino</div></div>
      <div class="mc a"><div class="ml">Potência</div><div class="mv">{kwp:.2f} kWp</div><div class="mu">kilowatt-pico</div></div>
      <div class="mc a"><div class="ml">Área Necessária</div><div class="mv">{area_nec:.0f} m²</div><div class="mu">telhado útil</div></div>
    </div>
    <div class="mg">
      <div class="mc g"><div class="ml">Geração Anual</div><div class="mv">{ger_ano:,.0f}</div><div class="mu">kWh / ano</div></div>
      <div class="mc g"><div class="ml">Cobertura</div><div class="mv">{cob}%</div><div class="mu">do consumo mensal</div></div>
      <div class="mc g"><div class="ml">CO₂ Evitado</div><div class="mv">{co2["ton_co2_25anos"]:.1f} t</div><div class="mu">em 25 anos</div></div>
    </div>
    <div class="mg">
      <div class="mc b"><div class="ml">Investimento</div><div class="mv" style="font-size:15px">R$ {inv["custo_total"]:,.0f}</div><div class="mu">R$ {inv["custo_por_kwp"]:,.0f}/kWp</div></div>
      <div class="mc b"><div class="ml">Economia Mensal</div><div class="mv">R$ {eco_mes:,.0f}</div><div class="mu">média / mês</div></div>
      <div class="mc b"><div class="ml">Payback Simples</div><div class="mv">{pb_s}</div><div class="mu">anos</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="tir-card">
      <div style="font-size:30px">📈</div>
      <div>
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:{MUTED};margin-bottom:3px">TIR — Taxa Interna de Retorno</div>
        <div class="tir-val">{tir}% a.a.</div>
      </div>
      <div class="tir-msg">{tir_txt}<br>
        <small>VPL 25 anos: <strong>{vpl_fmt}</strong> · Payback descontado: <strong>{pb_d} anos</strong> · SELIC: {taxa_desc*100:.1f}% a.a.</small>
      </div>
    </div>""", unsafe_allow_html=True)

    if pmt_val is not None:
        sc = GREEN if saldo_val>=0 else RED
        st.markdown(f"""
        <div class="card"><div class="card-h">🏦 Financiamento</div>
          <div class="mg" style="margin-top:10px">
            <div class="mc b"><div class="ml">Parcela Mensal</div><div class="mv">R$ {pmt_val:,}</div><div class="mu">R$/mês</div></div>
            <div class="mc g"><div class="ml">Saldo Líquido</div><div class="mv" style="color:{sc}">{"+" if saldo_val>=0 else ""}R$ {abs(saldo_val):,}</div><div class="mu">economia − parcela</div></div>
            <div class="mc"><div class="ml">Taxa / Prazo</div><div class="mv" style="color:{MUTED}">{f["taxa_fin"]*100:.1f}%</div><div class="mu">{int(f["prazo_fin"])} meses</div></div>
          </div></div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # DASHBOARDS — 5 abas
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div style="font-size:13px;font-weight:600;color:#5a7099;margin:20px 0 10px">📊 Dashboard de Análise</div>',
                unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["☀️ Geração vs Consumo","💸 Retorno Financeiro",
                                         "🔬 Física do Sistema","📊 Estatística Solar","🌿 Impacto Ambiental"])

    # ── Tab 1: Geração vs Consumo ─────────────────────────────────────
    with tab1:
        gv = [ger[m] for m in MESES]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=MESES+MESES[::-1],
            y=[ic_hi[m] for m in MESES]+[ic_lo[m] for m in MESES[::-1]],
            fill="toself", fillcolor="rgba(29,111,191,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="IC 95%", hoverinfo="skip"))
        fig1.add_trace(go.Bar(x=MESES, y=gv, name="Geração Est. (kWh)",
            marker_color="rgba(29,111,191,0.72)",
            marker_line_color=BLUE, marker_line_width=1,
            text=[f"{v:,.0f}" for v in gv],
            textposition="outside", textfont=dict(size=9,color=BLUED)))
        fig1.add_trace(go.Scatter(x=MESES, y=[consumo]*12,
            name=f"Consumo ({consumo} kWh)",
            line=dict(color=RED, width=2.5, dash="dash"), mode="lines"))
        fig1.add_trace(go.Scatter(x=MESES, y=gv, mode="lines+markers",
            line=dict(color=BLUE, width=2), marker=dict(size=7,color=BLUE),
            showlegend=False))
        fig1.update_layout(
            title=f"Geração vs Consumo — {f['cidade']} | GHI={ghi_c:.2f} kWh/m²/dia · Derate={PR*100:.0f}%",
            barmode="overlay", yaxis_title="kWh/mês",
            legend=dict(orientation="h",y=-0.30))
        theme(fig1, 340); st.plotly_chart(fig1, use_container_width=True)

        df = pd.DataFrame({
            "Mês": MESES,
            "HSP (kWh/m²/dia)": [round(mensal_c[m],3) for m in MESES],
            "Geração (kWh)": gv,
            "IC −95%": [ic_lo[m] for m in MESES],
            "IC +95%": [ic_hi[m] for m in MESES],
            "Consumo (kWh)": [consumo]*12,
            "Saldo (kWh)": [round(g-consumo,1) for g in gv],
            "Economia (R$)": [eco[m] for m in MESES],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown(f"""<div class="ibox-w" style="font-size:11px;margin-top:8px">
          📐 <strong>Fórmula (Física III):</strong> E_mês = P_kWp × HSP_mês × dias × PR<br>
          HSP mensal de <strong>{f['cidade']}</strong> extraído do arquivo
          <code>global_horizontal_means.csv</code> (LABREN/INPE) por IDW 4 vizinhos
          (lat {lat_c:.2f}°, lon {lon_c:.2f}°). Fator Derate: <strong>{PR*100:.0f}%</strong>.
        </div>""", unsafe_allow_html=True)

    # ── Tab 2: Retorno Financeiro ─────────────────────────────────────
    with tab2:
        anos_l=[f"Ano {a}" for a in fc["anos"]]
        fig2=make_subplots(rows=2,cols=1,
            subplot_titles=["Fluxo de Caixa Líquido (R$)","Retorno Acumulado — Payback (R$)"],
            vertical_spacing=0.14)
        fig2.add_trace(go.Bar(x=anos_l, y=fc["fluxo_liquido"],
            marker_color=[GREEN if v>=0 else RED for v in fc["fluxo_liquido"]],
            name="Fluxo Líquido"), row=1,col=1)
        fig2.add_trace(go.Scatter(x=anos_l, y=fc["acumulado"], mode="lines+markers",
            line=dict(color=ORANGE,width=2.5),
            marker=dict(color=[GREEN if v>=0 else RED for v in fc["acumulado"]],size=5),
            name="Acumulado"), row=2,col=1)
        fig2.add_shape(type="line",x0=0,x1=1,y0=0,y1=0,xref="x2 domain",yref="y2",
            line=dict(dash="dash",color=RED,width=1.2))
        if pb["payback_simples_anos"]:
            pi=pb["payback_simples_anos"]-1
            fig2.add_shape(type="line",x0=pi,x1=pi,y0=0,y1=1,xref="x2",yref="y2 domain",
                line=dict(dash="dot",color=BLUE,width=1.8))
            fig2.add_annotation(x=pi,y=1,xref="x2",yref="y2 domain",
                text=f"Payback Ano {pb['payback_simples_anos']}",
                showarrow=False,yanchor="bottom",font=dict(color=BLUE,size=10))
        fig2.update_layout(showlegend=True)
        theme(fig2,520); st.plotly_chart(fig2,use_container_width=True)

        fig_d=go.Figure(go.Pie(
            labels=["Módulos 45%","Inversor 20%","Estrutura 10%","Instalação 15%","Outros 10%"],
            values=[inv["custo_modulos"],inv["custo_inversor"],inv["custo_estrutura"],
                    inv["custo_instalacao"],inv["custo_outros"]],
            hole=0.52, marker_colors=[BLUE,BLUED,GREEN,ORANGE,MUTED],
            textfont=dict(size=10,color=TEXT)))
        fig_d.update_layout(title="Composição do Investimento",
            legend=dict(orientation="h",y=-0.18,font=dict(color=MUTED)))
        theme(fig_d,260); st.plotly_chart(fig_d,use_container_width=True)

        st.markdown(f"""
| Indicador | Valor |
|---|---|
| **VPL (25 anos)** | {vpl_fmt} |
| **TIR** | {tir}% a.a. |
| **Payback simples** | {pb_s} anos |
| **Payback descontado** | {pb_d} anos |
| **Economia anual (ano 1)** | R$ {eco_mes*12:,.0f} |
| **Total economizado (25 anos)** | R$ {sum(fc["economias"]):,.0f} |
""")

    # ── Tab 3: Física ─────────────────────────────────────────────────
    with tab3:
        c3a, c3b = st.columns(2)
        with c3a:
            lp=[k for k in per if k!="Total"]; vp=[per[k] for k in lp]
            fig_per=go.Figure(go.Bar(x=lp,y=vp,
                marker_color="rgba(220,38,38,0.7)",
                marker_line_color=RED,marker_line_width=1,
                text=[f"{v}%" for v in vp],textposition="outside",
                textfont=dict(color=MUTED)))
            fig_per.update_layout(title=f"Perdas do Sistema — Derate Padrão: {per['Total']}%",
                yaxis_title="Perda (%)")
            theme(fig_per,250); st.plotly_chart(fig_per,use_container_width=True)
            st.latex(r"PR=1-(\eta_{inv}+\eta_{cab}+\eta_{som}+\eta_{suj}+\alpha_T\Delta T)")
            st.markdown(f"**Derate configurado pelo usuário:** {PR*100:.0f}%")

        with c3b:
            betas=np.arange(0,45,0.5)
            irrs=[float(ghi_c*(0.80+0.20*np.cos(np.radians(abs(lat_c)-b)))) for b in betas]
            beta_opt=betas[int(np.argmax(irrs))]
            fig_ang=go.Figure(go.Scatter(x=betas,y=irrs,mode="lines",
                line=dict(color=BLUE,width=2.5),fill="tozeroy",
                fillcolor="rgba(29,111,191,0.08)"))
            fig_ang.add_vline(x=beta_opt,line_dash="dash",line_color=GREEN,
                annotation_text=f"β*={beta_opt:.1f}°≈|φ|={abs(lat_c):.1f}°",
                annotation_font_color=GREEN)
            fig_ang.update_layout(title="Ângulo Ótimo — Cálculo III",
                xaxis_title="β (graus)",yaxis_title="GHI estimado (kWh/m²/dia)")
            theme(fig_ang,250); st.plotly_chart(fig_ang,use_container_width=True)
            st.latex(r"I(\beta)=GHI\cdot\cos(\varphi-\beta)\Rightarrow\beta^*\approx|\varphi|")

        temps=np.arange(25,75,1)
        perda_t=[round(abs(-0.0035)*(t-25)*100,2) for t in temps]
        fig_t=go.Figure(go.Scatter(x=temps,y=perda_t,mode="lines",
            line=dict(color=RED,width=2),fill="tozeroy",
            fillcolor="rgba(220,38,38,0.06)"))
        fig_t.add_vline(x=TEMP_OPERACAO_LOCAL,line_dash="dash",line_color=ORANGE,
            annotation_text=f"T={TEMP_OPERACAO_LOCAL}°C → {per['Temperatura']}% perda",
            annotation_font_color=ORANGE)
        fig_t.update_layout(title="Perda por Temperatura — αT=−0,35%/°C (Física III)",
            xaxis_title="T (°C)",yaxis_title="Perda (%)")
        theme(fig_t,220); st.plotly_chart(fig_t,use_container_width=True)

    # ── Tab 4: Estatística Solar ──────────────────────────────────────
    with tab4:
        irr_v=[mensal_c[m] for m in MESES]
        med=np.mean(irr_v); std=np.std(irr_v)
        m1,m2,m3=st.columns(3)
        m1.metric("HSP Médio Anual",f"{med:.3f} kWh/m²/dia")
        m2.metric("Desvio Padrão",f"{std:.3f} kWh/m²/dia")
        m3.metric("Coef. Variação",f"{std/med*100:.1f}%")

        fig_s=go.Figure()
        fig_s.add_trace(go.Bar(x=MESES,y=irr_v,name="HSP Mensal",
            marker_color="rgba(29,111,191,0.72)",
            marker_line_color=BLUE,marker_line_width=1))
        fig_s.add_hline(y=med,line_dash="dash",line_color=GREEN,
            annotation_text=f"Média={med:.3f}",annotation_font_color=GREEN)
        fig_s.add_hline(y=med+std,line_dash="dot",line_color=MUTED,
            annotation_text="+1σ",annotation_font_color=MUTED)
        fig_s.add_hline(y=med-std,line_dash="dot",line_color=MUTED,
            annotation_text="-1σ",annotation_font_color=MUTED)
        fig_s.update_layout(
            title=f"Irradiância Mensal — {f['cidade']} (CSV LABREN/INPE · IDW)",
            yaxis_title="HSP (kWh/m²/dia)")
        theme(fig_s,300); st.plotly_chart(fig_s,use_container_width=True)

        mu_g=ger_ano; sg=mu_g*0.06
        xd=np.linspace(mu_g-3*sg,mu_g+3*sg,280)
        yd=(1/(sg*np.sqrt(2*np.pi)))*np.exp(-0.5*((xd-mu_g)/sg)**2)
        lo95=mu_g-1.96*sg; hi95=mu_g+1.96*sg
        fig_n=go.Figure()
        fig_n.add_trace(go.Scatter(x=xd,y=yd,mode="lines",
            line=dict(color=BLUE,width=2),fill="tozeroy",
            fillcolor="rgba(29,111,191,0.08)"))
        fig_n.add_vrect(x0=lo95,x1=hi95,fillcolor="rgba(22,163,74,0.06)",
            layer="below",line_width=0,
            annotation_text="IC 95%",annotation_font_color=GREEN)
        fig_n.add_vline(x=mu_g,line_dash="dash",line_color=GREEN,
            annotation_text=f"μ={mu_g:.0f} kWh/ano",annotation_font_color=GREEN)
        fig_n.update_layout(
            title=f"Distribuição Anual — IC 95%: [{lo95:.0f} ; {hi95:.0f}] kWh/ano",
            xaxis_title="kWh/ano",yaxis_title="Densidade de Probabilidade")
        theme(fig_n,240); st.plotly_chart(fig_n,use_container_width=True)
        st.latex(r"\bar{X}\pm1{,}96\cdot\frac{\sigma}{\sqrt{17}}\quad(n=17\text{ anos — série Atlas})")

    # ── Tab 5: Ambiental ──────────────────────────────────────────────
    with tab5:
        ca,cb_col,cc=st.columns(3)
        ca.metric("CO₂ evitado/ano",f"{co2['kg_co2_ano']:,.0f} kg")
        cb_col.metric("CO₂ em 25 anos",f"{co2['ton_co2_25anos']:.1f} t")
        cc.metric("Equiv. em árvores",f"{co2['arvores_eq']:,} 🌳")
        fig_c=go.Figure(go.Scatter(
            x=[f"Ano {a}" for a in fc["anos"]],
            y=[co2["kg_co2_ano"]*a/1000 for a in fc["anos"]],
            mode="lines+markers",line=dict(color=GREEN,width=2.5),
            fill="tozeroy",fillcolor="rgba(22,163,74,0.08)",
            marker=dict(size=4,color=GREEN)))
        fig_c.update_layout(title="CO₂ Evitado Acumulado (25 anos)",yaxis_title="CO₂ (t)")
        theme(fig_c,240); st.plotly_chart(fig_c,use_container_width=True)
        st.markdown("""<div class="ibox-w" style="font-size:11px">
          🌱 Fator de emissão: <strong>0,0884 kgCO₂/kWh</strong> (Fator Médio SIN — ONS 2023).<br>
          Equivalência arbórea: 1 árvore ≈ 21,77 kgCO₂/ano absorvidos.
        </div>""", unsafe_allow_html=True)

    # ── Disciplinas ───────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card" style="margin-top:16px">
      <div class="card-h">📚 Articulação com as Disciplinas — BC&T/UFMT</div>
      <div class="card-sub">Como cada componente curricular fundamenta este Sistema de Apoio à Decisão:</div>
      <div class="disc-grid">
        <div class="dcard da"><h4>⚡ Física III</h4>
          <p>Efeito fotovoltaico, potência de pico (kWp), Fator Derate e perdas físicas reais.
          Coeficiente αT=−0,35%/°C. HSP mensal por município via CSV LABREN/INPE (IDW).</p></div>
        <div class="dcard db"><h4>∫ Cálculo III</h4>
          <p>Otimização β*(φ)=|φ| por maximização de I(β)=GHI·cos(φ−β).
          Para {f['cidade']}: β*≈{angot}° — minimiza integral da irradiância não captada.</p></div>
        <div class="dcard dg"><h4>💰 Matemática Financeira</h4>
          <p>VPL, TIR (bissecção numérica), Payback simples e descontado, PMT para
          financiamento, juros compostos, inflação {inflacao*100:.1f}% a.a., depreciação 0,5%/ano.</p></div>
        <div class="dcard dp"><h4>📊 Prob. e Estatística</h4>
          <p>17 anos de dados satelitais (1999–2015). IC 95% via Teorema Central do Limite
          (n=17). Variabilidade interanual σ={std:.3f} kWh/m²/dia para {f['cidade']}.</p></div>
        <div class="dcard da full"><h4>🧠 Gestão do Conhecimento</h4>
          <p>Democratiza análises antes restritas a especialistas — capacitando produtores rurais,
          moradores e empresas do MT. 141 municípios georreferenciados com dados reais do CSV
          Atlas INPE (IDW). Código modular (dados_solar_mt · data · calculations · financial · app).
          Licença GNU GPL v3.0.</p></div>
      </div>
    </div>""", unsafe_allow_html=True)

    with st.expander("📐 Fórmulas e Fundamentação Teórica"):
        f1,f2=st.columns(2)
        with f1:
            st.markdown("**⚡ Física III**")
            st.latex(r"E_{mes}=P_{kWp}\cdot HSP_{mes}\cdot d_{mes}\cdot PR_{derate}")
            st.latex(r"P_{kWp}=\frac{C_{mes}\times1{,}10}{GHI\cdot PR\cdot30}")
            st.markdown("**∫ Cálculo III**")
            st.latex(r"\beta^*=\arg\max_\beta GHI\cdot\cos(\varphi-\beta)\approx|\varphi|")
        with f2:
            st.markdown("**💰 Matemática Financeira**")
            st.latex(r"VPL=-C_0+\sum_{t=1}^{25}\frac{FC_t}{(1+i)^t}")
            st.latex(r"PMT=PV\cdot\frac{r(1+r)^n}{(1+r)^n-1}")
            st.markdown("**📊 Probabilidade e Estatística**")
            st.latex(r"IC_{95\%}=\bar{X}\pm1{,}96\cdot\frac{\sigma}{\sqrt{17}}")

    # ── Compartilhar ──────────────────────────────────────────────────
    import urllib.parse, streamlit.components.v1 as components
    _url = "https://calculadorasolarmatogro.streamlit.app"
    _txt = (f"Simulei meu sistema solar em {f['cidade']}/MT com a SolarMT! "
            f"{kwp:.1f} kWp, retorno em {pb_s} anos, TIR {tir}% a.a. — BC&T/UFMT:")
    _te=urllib.parse.quote(_txt); _ue=urllib.parse.quote(_url)
    _mb=urllib.parse.quote(
        f"{_txt}\n{_url}\n\nMunicípio: {f['cidade']} | GHI: {ghi_c:.2f} kWh/m²/dia\n"
        f"Derate: {PR*100:.0f}% | Painéis: {n}×550Wp={kwp:.2f}kWp\n"
        f"Geração: {ger_ano:,.0f} kWh/ano | Economia: R${eco_mes:,.0f}/mês\n"
        f"Investimento: R${inv['custo_total']:,.0f} | Payback: {pb_s}a | TIR: {tir}%")
    _mail=f"mailto:?subject={urllib.parse.quote('Simulação Solar — SolarMT/BC&T UFMT')}&body={_mb}"

    st.markdown('<div style="font-size:12px;font-weight:600;color:#5a7099;margin:16px 0 8px">📣 Compartilhar resultado</div>',
                unsafe_allow_html=True)
    components.html(f"""
    <style>
    .sr{{display:flex;gap:8px;flex-wrap:wrap;}}
    .sb{{display:flex;align-items:center;gap:6px;padding:9px 14px;border-radius:8px;
         border:none;font-size:12px;font-weight:600;cursor:pointer;text-decoration:none;
         transition:opacity .15s;white-space:nowrap;}}
    .sb:hover{{opacity:.82;}}
    .wa{{background:#25d366;color:#fff;}}.tw{{background:#1da1f2;color:#fff;}}
    .li{{background:#0077b5;color:#fff;}}.fb{{background:#1877f2;color:#fff;}}
    .em{{background:#f0f5fb;color:#1a2744;border:1px solid #c8d9ef;}}
    .cp{{background:#deeaf8;color:#1d6fbf;border:1px solid #a8c8ee;}}
    .ok{{background:#16a34a!important;color:#fff!important;border-color:transparent!important;}}
    </style>
    <div class="sr">
      <a class="sb wa" href="https://wa.me/?text={_te}%20{_ue}" target="_blank">💬 WhatsApp</a>
      <a class="sb tw" href="https://twitter.com/intent/tweet?text={_te}&url={_ue}" target="_blank">𝕏 Twitter</a>
      <a class="sb li" href="https://www.linkedin.com/sharing/share-offsite/?url={_ue}" target="_blank">💼 LinkedIn</a>
      <a class="sb fb" href="https://www.facebook.com/sharer/sharer.php?u={_ue}" target="_blank">👍 Facebook</a>
      <a class="sb em" href="{_mail}">✉️ E-mail</a>
      <button class="sb cp" id="cpb"
        onclick="navigator.clipboard.writeText('{_url}').then(()=>{{
          var b=document.getElementById('cpb');b.textContent='✓ Copiado!';b.classList.add('ok');
          setTimeout(()=>{{b.textContent='🔗 Copiar link';b.classList.remove('ok');}},2500);}})">
        🔗 Copiar link</button>
    </div>""", height=52)

    st.markdown("---")
    br1,br2=st.columns(2)
    with br1:
        if st.button("← Nova Simulação", type="secondary", use_container_width=True):
            st.session_state.step=1; st.session_state.form={}; st.rerun()
    with br2:
        components.html("""
        <button onclick="window.parent.window.print()"
          style="width:100%;padding:11px 22px;background:#1d6fbf;color:#fff;
                 border:none;border-radius:8px;font-size:13px;font-weight:600;
                 cursor:pointer;min-height:44px;">🖨️ Imprimir / Salvar PDF</button>""",height=50)

    # ── Banner de Feedback ───────────────────────────────────────────
    st.markdown('''
    <div style="
      background:linear-gradient(135deg,#deeaf8 0%,#e8f5e9 100%);
      border:1.5px solid #a8c8ee;
      border-radius:14px;
      padding:18px 22px;
      margin-top:18px;
      display:flex;
      align-items:center;
      gap:16px;
      flex-wrap:wrap;
    ">
      <div style="font-size:28px">💬</div>
      <div style="flex:1;min-width:200px">
        <div style="font-size:14px;font-weight:700;color:#0d3d6e;margin-bottom:3px">
          Gostou do resultado?
        </div>
        <div style="font-size:13px;color:#5a7099;line-height:1.5">
          Nos ajude a melhorar deixando seu feedback — leva 1 minutinho 😊
        </div>
      </div>
      <a href="https://forms.gle/Ym47U8RZSGnNT35n6" target="_blank"
         style="
           display:inline-block;
           background:#1d6fbf;
           color:#fff;
           font-weight:700;
           font-size:13px;
           padding:11px 22px;
           border-radius:8px;
           text-decoration:none;
           white-space:nowrap;
           box-shadow:0 3px 10px rgba(29,111,191,0.25);
           transition:opacity .15s;
         ">
        ✍️ Deixar feedback
      </a>
    </div>
    ''', unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-brand">SolarMT — Sistema de Apoio à Decisão de Engenharia Solar</div>
  <p>Bacharelado em Ciência e Tecnologia ·
     <strong style="color:#0d3d6e">UFMT — Universidade Federal de Mato Grosso</strong><br>
     Seminário Integrador IV · Lucas do Rio Verde/MT · 2026</p>
  <div class="footer-team">
    <strong>Equipe:</strong>
    Messias Kennedy &nbsp;·&nbsp;
    <a href="https://www.instagram.com/angelicasantos.r/" target="_blank">Angélica Santos</a>
    &nbsp;·&nbsp; Karleia &nbsp;·&nbsp; Viviane
  </div>
  <p style="font-size:10px;opacity:.6;margin-top:6px">
    Atlas Brasileiro de Energia Solar, 2ª Ed. — INPE/LABREN (2017) · DOI: 10.34024/978851700089<br>
    CSV: global_horizontal_means.csv (LABREN/INPE) · Tarifa: ENERGISA-MT · CO₂: ONS 2023 · GNU GPL v3.0
  </p>
</div>
""", unsafe_allow_html=True)
