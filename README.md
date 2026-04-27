# ☀️ SolarSim — Simulador Fotovoltaico
## Lucas do Rio Verde / MT — Projeto Integrador BCT/UFMT

---

## 📋 Visão Geral

Sistema Web desenvolvido em Python + Streamlit que simula um projeto de energia solar fotovoltaica para a região de Lucas do Rio Verde/MT, integrando 5 disciplinas do curso de Bacharelado em Ciência e Tecnologia.

---

## 🚀 Como Executar

```bash
# 1. Clone ou extraia o projeto
cd solar_simulator/

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
streamlit run app.py

# O navegador abrirá automaticamente em: http://localhost:8501
```

---

## 📁 Estrutura do Projeto

```
solar_simulator/
│
├── app.py            # Interface principal (Streamlit)
├── calculations.py   # Cálculos fotovoltaicos (Física III + Cálculo III)
├── financial.py      # Análise financeira (Matemática Financeira)
├── data.py           # Dados de radiação e constantes (Prob. e Estatística)
├── requirements.txt  # Dependências Python
└── README.md         # Este manual
```

---

## 🎯 Como Usar o Simulador

### Passo 1 — Entrada de Dados (Sidebar esquerdo)
1. **Consumo médio mensal (kWh):** insira o valor da sua conta de energia
2. **Valor médio da conta (R$):** para referência e validação da tarifa
3. **Parâmetros avançados:** tarifa, inflação energética e taxa de desconto (SELIC)

### Passo 2 — Leitura dos KPIs
- **Dimensionamento:** potência (kWp), nº de painéis, área de telhado, geração anual
- **Financeiro:** investimento total, payback simples e descontado, VPL, TIR

### Passo 3 — Dashboard (5 abas)
| Aba | Conteúdo |
|-----|----------|
| ☀️ Geração vs Consumo | Gráfico mensal + IC 95% + tabela completa |
| 💸 Fluxo de Caixa | Payback, VPL, TIR, composição do investimento |
| 🔬 Física do Sistema | Perdas, ângulo ótimo, efeito da temperatura |
| 📊 Estatística | Distribuição de geração, intervalos de confiança |
| 🌿 Ambiental | CO₂ evitado, equivalente em árvores |

---

## 🎓 Articulação com as Disciplinas

### Física III
- **Efeito fotovoltaico:** cálculo da potência de pico (kWp)
- **Performance Ratio:** modelagem de todas as perdas do sistema
- **Coeficiente de temperatura:** queda de eficiência com o calor

### Probabilidade e Estatística
- **Médias históricas** de HSP (1994–2020) do CRESESB/INPE
- **Intervalo de Confiança de 95%** na estimativa de geração mensal
- **Teorema Central do Limite** para modelagem da distribuição de geração anual
- **Desvio padrão e coeficiente de variação** da irradiância mensal

### Matemática Financeira
- **Payback simples e descontado**
- **VPL (Valor Presente Líquido):** critério de viabilidade do investimento
- **TIR (Taxa Interna de Retorno):** calculada por bissecção numérica
- **Juros compostos:** evolução da tarifa com inflação energética
- **Depreciação:** degradação anual dos módulos (0,5%/ano)

### Cálculo III
- **Otimização de função multivariável:** ângulo de inclinação ótimo β*(φ, γ)
- **Modelagem da curva de irradiância** em função do ângulo e azimute
- **Cálculo numérico (bissecção)** para determinação da TIR

### Gestão do Conhecimento
- Código modular e documentado com docstrings
- Manual de usuário (este README)
- Dados referenciados com fonte primária
- Licença MIT para reutilização por futuros alunos

---

## 📐 Principais Equações

```
Potência (kWp):
    P = E_mes / (HSP_med × PR × 30)

Geração mensal:
    G_mes = P_kWp × HSP_mes × dias × PR

Performance Ratio:
    PR = 1 − (η_inv + η_cab + η_som + η_suj + αT·ΔT)

VPL:
    VPL = −C₀ + Σ [FCt / (1+i)^t]

TIR:
    VPL(TIR) = 0

Economia anual:
    E_t = G_t × τ₀ × (1+πe)^t,   G_t = G₀ × (1−δ)^t

IC 95%:
    X̄ ± 1.96 × (σ/√n)

Ângulo ótimo:
    β* = |φ| ≈ 13° (Lucas do Rio Verde)
```

---

## 📊 Fontes de Dados

| Dado | Fonte |
|------|-------|
| Irradiância solar (HSP) | CRESESB/INPE — Atlas Brasileiro de Energia Solar, 2ª ed. |
| Tarifa de energia | ENERGISA-MT — Subgrupo B1 Residencial (2025) |
| Fator de emissão CO₂ | ONS — Fator Médio de Emissão do SIN (2023) |
| Custo por kWp | Pesquisa de mercado — MT (2025) |
| Inflação da energia | ANEEL — histórico 2015–2025 |

---

## ⚙️ Especificações Técnicas do Módulo Simulado

| Parâmetro | Valor |
|-----------|-------|
| Potência de pico | 550 Wp |
| Eficiência | 21,5% |
| Área | 2,56 m² |
| Coef. de temperatura | −0,35%/°C |
| Vida útil | 25 anos |
| Degradação | 0,5%/ano |

---

## 📜 Licença

MIT License — livre para uso, modificação e distribuição acadêmica.

Projeto desenvolvido para o BCT/UFMT — Lucas do Rio Verde/MT.
