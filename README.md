# ☀️ SolarMT — Calculadora de Viabilidade Solar Fotovoltaica
### Sistema de Apoio à Decisão de Engenharia · BC&T/UFMT · Seminário Integrador IV · 2026

---

## 🚀 Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Deploy: **https://calculadorasolarmatogro.streamlit.app**

---

## 📁 Estrutura

```
solar_simulator/
├── app.py              # Interface Streamlit — wizard 3 etapas + 5 dashboards
├── dados_solar_mt.py   # 141 municípios MT com HSP mensal real (CSV LABREN/INPE)
├── calculations.py     # Física III + Cálculo III
├── financial.py        # Matemática Financeira (VPL, TIR, Payback, PMT)
├── data.py             # Constantes e funções base
└── requirements.txt
```

---

## 📊 Fontes de Dados

| Dado | Fonte |
|------|-------|
| Irradiação mensal (141 municípios) | `global_horizontal_means.csv` — LABREN/INPE |
| GHI anual (24 cidades principais) | Atlas INPE/LABREN 2017 (anotações Gemini) |
| Método de interpolação | IDW 4 vizinhos — grade 0,1°×0,1° |
| Série histórica | 17 anos (1999–2015) · satélite GOES · modelo BRASIL-SR |
| Validação | REQM ≈ 8,2% · Viés ≈ 0,2% (Atlas Tabela 4, p.42) |
| Performance Ratio | 80% — padrão Atlas Fig.52, p.57 |
| Fator Derate | 75–85% (configurável pelo usuário — slider) |
| Fator CO₂ | 0,0884 kgCO₂/kWh — ONS 2023 |
| Custos de mercado | Solturi LRV + Co2Solar — Lucas do Rio Verde/MT 2025 |

---

## 🎓 Disciplinas Integradas

| Disciplina | Aplicação |
|---|---|
| **Física III** | Efeito FV, P_kWp, PR com perdas reais, αT = −0,35%/°C |
| **Cálculo III** | β*(φ) = \|φ\| por maximização de I(β) = GHI·cos(φ−β) |
| **Matemática Financeira** | VPL, TIR (bissecção), Payback, PMT, juros compostos |
| **Prob. e Estatística** | IC 95% (n=17 anos TCL), variabilidade interanual |
| **Gestão do Conhecimento** | SAD modular documentado, GPL v3.0 |

---

## 👥 Equipe

| Nome | Papel |
|------|-------|
| **Messias Kennedy** | Desenvolvimento principal |
| **[Angélica Santos](https://www.instagram.com/angelicasantos.r/)** | Desenvolvimento |
| **Karleia** | Desenvolvimento |
| **Viviane** | Desenvolvimento |

**Referência:** Pereira, E. B. et al. Atlas Brasileiro de Energia Solar, 2ª Ed. INPE, 2017.
DOI: [10.34024/978851700089](http://doi.org/10.34024/978851700089)

**Licença:** GNU GPL v3.0
