"""data.py — Constantes e funções base — Atlas INPE/LABREN 2017"""
import numpy as np

LATITUDE  = -13.05; LONGITUDE = -55.91; ALTITUDE = 384
CIDADE    = "Lucas do Rio Verde / MT"
MESES     = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
DIAS_POR_MES = [31,28,31,30,31,30,31,31,30,31,30,31]

# PR padrão Atlas (Fig.52, p.57) — sobrescrito pelo Fator Derate do usuário
PERDA_INVERSOR=0.030; PERDA_CABEAMENTO=0.015; PERDA_SOMBREAMENTO=0.025
PERDA_SUJEIRA=0.020;  MODULO_COEF_TEMP=-0.0035; TEMP_REFERENCIA=25; TEMP_OPERACAO_LOCAL=45
PERDA_TEMPERATURA = abs(MODULO_COEF_TEMP)*(TEMP_OPERACAO_LOCAL-TEMP_REFERENCIA)
FATOR_DESEMPENHO  = round(1-(PERDA_INVERSOR+PERDA_CABEAMENTO+PERDA_SOMBREAMENTO+
                             PERDA_SUJEIRA+PERDA_TEMPERATURA),4)

MODULO_POTENCIA_WP=550; MODULO_AREA_M2=2.56
TARIFA_ENERGIA_KWH=0.87; INFLACAO_ENERGIA_AA=0.065; TAXA_DESCONTO=0.12
VIDA_UTIL_ANOS=25; TAXA_DEPRECIACAO_AA=0.005; CUSTO_MANUTENCAO_AA=400.0
FATOR_EMISSAO_CO2_KG_KWH=0.0884

# ── Modelo de custo calibrado com 3 fornecedores reais (2025/2026) ──────────
# Solturi (Lucas do Rio Verde — COM instalação):
#   2,2 kWp → R$ 8.700  → R$ 3.955/kWp
#   4,4 kWp → R$ 12.600 → R$ 2.864/kWp
#   5,5 kWp → R$ 14.700 → R$ 2.673/kWp
#   8,25kWp → R$ 20.200 → R$ 2.448/kWp
# Alberti Instalações (COM instalação completa):
#   4,4 kWp → R$ 14.990 → R$ 3.407/kWp
#   5,5 kWp → R$ 17.490 → R$ 3.180/kWp
#   7,7 kWp → R$ 21.990 → R$ 2.856/kWp
#   8,8 kWp → R$ 25.990 → R$ 2.953/kWp
#  11,0 kWp → R$ 30.990 → R$ 2.817/kWp
# Super Promoção (EQUIPAMENTOS sem instalação — adicionar ~R$2.000-3.000):
#   1,85kWp → R$ 4.999  → R$ 2.697/kWp (equip.)
#   3,71kWp → R$ 8.599  → R$ 2.320/kWp (equip.)
#   7,41kWp → R$ 13.999 → R$ 1.888/kWp (equip.)
#  11,49kWp → R$ 20.799 → R$ 1.810/kWp (equip.)
# Média ponderada Solturi + Alberti (instalação completa):
_KWP_PONTOS   = [1.0,  2.2,   4.4,   5.5,   7.7,   8.5,   11.0,  20.0]
_CUSTO_PONTOS = [4500, 3955,  3135,  2926,  2856,  2700,  2817,  2200]

def custo_por_kwp(kwp):
    return float(np.interp(kwp, _KWP_PONTOS, _CUSTO_PONTOS))

CUSTO_POR_KWP = 4500  # referência média
