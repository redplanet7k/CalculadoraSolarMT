"""
data.py — Dados de radiação solar para Lucas do Rio Verde/MT
Fonte: CRESESB / INPE / ATLAS BRASILEIRO DE ENERGIA SOLAR (2ª edição)
Disciplina: Probabilidade e Estatística — médias históricas com margens de confiança
"""

import numpy as np

# ─── Coordenadas geográficas ────────────────────────────────────────────────
LATITUDE  = -13.05   # graus Sul
LONGITUDE = -55.91   # graus Oeste
ALTITUDE  =  384     # metros acima do nível do mar
CIDADE    = "Lucas do Rio Verde / MT"
FUSO      = "UTC-4"

# ─── Irradiância média diária (kWh/m²/dia) — plano inclinado ótimo (~13°) ───
# Valores do CRESESB para a região, série histórica 1994-2020
IRRADIANCIA_MENSAL = {
    "Janeiro":   5.10,
    "Fevereiro": 5.30,
    "Março":     5.20,
    "Abril":     5.50,
    "Maio":      5.60,
    "Junho":     5.80,
    "Julho":     6.00,
    "Agosto":    6.20,
    "Setembro":  5.70,
    "Outubro":   5.30,
    "Novembro":  5.00,
    "Dezembro":  4.90,
}

# Desvios padrão históricos (simulados com base na variabilidade regional)
DESVIO_PADRAO_MENSAL = {
    "Janeiro":   0.42,
    "Fevereiro": 0.38,
    "Março":     0.35,
    "Abril":     0.30,
    "Maio":      0.28,
    "Junho":     0.25,
    "Julho":     0.22,
    "Agosto":    0.24,
    "Setembro":  0.33,
    "Outubro":   0.40,
    "Novembro":  0.45,
    "Dezembro":  0.50,
}

MESES = list(IRRADIANCIA_MENSAL.keys())
DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# HSP média anual (horas de sol pleno)
HSP_MEDIA_ANUAL = np.mean(list(IRRADIANCIA_MENSAL.values()))

# ─── Parâmetros dos módulos fotovoltaicos (Física III) ───────────────────────
MODULO_POTENCIA_WP   = 550        # Wpico por módulo (padrão mercado 2025)
MODULO_EFICIENCIA    = 0.215      # 21,5% — eficiência típica monocristalino
MODULO_AREA_M2       = 2.56       # m² por módulo (2,278 m x 1,134 m aprox.)
MODULO_COEF_TEMP     = -0.0035    # %/°C — coeficiente de temperatura de potência
TEMP_REFERENCIA      = 25         # °C (STC)
TEMP_OPERACAO_LOCAL  = 45         # °C — temperatura de operação em Lucas do Rio Verde

# ─── Perdas do sistema (Física III) ─────────────────────────────────────────
PERDA_INVERSOR       = 0.035      # 3,5%
PERDA_CABEAMENTO     = 0.015      # 1,5%
PERDA_SOMBREAMENTO   = 0.030      # 3,0%
PERDA_SUJEIRA        = 0.020      # 2,0%
PERDA_TEMPERATURA    = abs(MODULO_COEF_TEMP) * (TEMP_OPERACAO_LOCAL - TEMP_REFERENCIA)
FATOR_DESEMPENHO     = 1 - (PERDA_INVERSOR + PERDA_CABEAMENTO +
                             PERDA_SOMBREAMENTO + PERDA_SUJEIRA + PERDA_TEMPERATURA)

# ─── Dados financeiros (Matemática Financeira) ───────────────────────────────
CUSTO_POR_KWP        = 4_200.0    # R$/kWp instalado (mercado MT, 2025)
TARIFA_ENERGIA_KWH   = 0.87       # R$/kWh (ENERGISA MT — Subgrupo B1 Residencial)
INFLACAO_ENERGIA_AA  = 0.065      # 6,5% ao ano (histórico ANEEL 2015-2025)
TAXA_DESCONTO        = 0.12       # 12% ao ano (SELIC referência)
VIDA_UTIL_ANOS       = 25         # vida útil do sistema (garantia de fabricante)
TAXA_DEPRECIACAO_AA  = 0.005      # 0,5% ao ano (degradação dos módulos)
CUSTO_MANUTENCAO_AA  = 350.0      # R$/ano (limpeza + revisão inversor)
INCENTIVO_ICMS       = 0.00       # MT isenta ICMS para microgeração (Lei 10.348/2016)

# ─── Dados estatísticos para IC (Probabilidade e Estatística) ────────────────
Z_95 = 1.96   # z-score para intervalo de confiança de 95%
Z_90 = 1.645  # z-score para intervalo de confiança de 90%

def intervalo_confianca_geracao(geracao_media: float, mes: str, n_anos: int = 20) -> tuple:
    """
    Retorna o intervalo de confiança de 95% para a geração mensal estimada.
    Usa o Teorema Central do Limite com série histórica de n_anos.
    """
    sigma = DESVIO_PADRAO_MENSAL[mes]
    erro_padrao = sigma / np.sqrt(n_anos)
    margem = Z_95 * erro_padrao * DIAS_POR_MES[MESES.index(mes)]
    return (geracao_media - margem, geracao_media + margem)
