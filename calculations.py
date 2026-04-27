"""
calculations.py — Módulo de cálculos fotovoltaicos
Disciplinas: Física III + Cálculo III
Aplica leis do efeito fotovoltaico, eficiência dos módulos e otimização de superfície.
"""

import numpy as np
from data import (
    LATITUDE,
    IRRADIANCIA_MENSAL, DIAS_POR_MES, MESES,
    MODULO_POTENCIA_WP, MODULO_AREA_M2, MODULO_EFICIENCIA,
    FATOR_DESEMPENHO, MODULO_COEF_TEMP, TEMP_REFERENCIA,
    TEMP_OPERACAO_LOCAL, HSP_MEDIA_ANUAL,
    PERDA_INVERSOR, PERDA_CABEAMENTO, PERDA_SOMBREAMENTO,
    PERDA_SUJEIRA, PERDA_TEMPERATURA,
    intervalo_confianca_geracao
)


# ─── 1. Potência do sistema necessária (Física III) ──────────────────────────
def calcular_potencia_sistema(consumo_kwh_mes: float) -> dict:
    """
    Calcula a potência de pico (kWp) do sistema fotovoltaico.

    Equação base (Física III):
        P_pico = E_mes / (HSP_med × PR × 30)
    onde:
        E_mes  = energia mensal consumida [kWh]
        HSP    = Horas de Sol Pleno médias [h/dia]
        PR     = Performance Ratio (fator de desempenho global)

    Retorna dict com potência, nº de módulos e área.
    """
    # Acrescenta 10% de folgura para perdas residuais e crescimento de carga
    consumo_com_folga = consumo_kwh_mes * 1.10

    potencia_kWp = consumo_com_folga / (HSP_MEDIA_ANUAL * FATOR_DESEMPENHO * 30)

    n_modulos = int(np.ceil(potencia_kWp * 1000 / MODULO_POTENCIA_WP))
    potencia_real_kWp = (n_modulos * MODULO_POTENCIA_WP) / 1000
    area_total_m2 = n_modulos * MODULO_AREA_M2

    return {
        "potencia_nominal_kWp": round(potencia_kWp, 3),
        "potencia_real_kWp":    round(potencia_real_kWp, 3),
        "n_modulos":            n_modulos,
        "area_total_m2":        round(area_total_m2, 2),
        "fator_desempenho":     round(FATOR_DESEMPENHO, 4),
    }


# ─── 2. Geração mensal estimada (Física III + Prob. e Estatística) ───────────
def calcular_geracao_mensal(potencia_kWp: float) -> dict:
    """
    Estima a energia gerada mês a mês com base na irradiância local (Lucas/MT).

    Fórmula (Física III):
        G_mes = P_pico [kWp] × HSP_mes [h/dia] × dias × PR

    Inclui Intervalo de Confiança de 95% (Prob. e Estatística).
    """
    geracao = {}
    ic_lower = {}
    ic_upper = {}

    for i, mes in enumerate(MESES):
        hsp = IRRADIANCIA_MENSAL[mes]
        dias = DIAS_POR_MES[i]
        g_mes = potencia_kWp * hsp * dias * FATOR_DESEMPENHO
        geracao[mes] = round(g_mes, 1)

        lo, hi = intervalo_confianca_geracao(g_mes, mes)
        ic_lower[mes] = round(max(lo, 0), 1)
        ic_upper[mes] = round(hi, 1)

    return {
        "geracao_kwh": geracao,
        "ic_lower":    ic_lower,
        "ic_upper":    ic_upper,
        "media_anual": round(sum(geracao.values()), 1),
    }


# ─── 3. Efeito da temperatura (Física III — coeficiente de temperatura) ──────
def perda_por_temperatura(temp_operacao: float = TEMP_OPERACAO_LOCAL) -> float:
    """
    Calcula a perda de potência por temperatura acima de STC (25°C).

    ΔP/P = α × (T_op - T_ref)  [Física III — coeficiente de temperatura]
    """
    delta_T = temp_operacao - TEMP_REFERENCIA
    perda_frac = abs(MODULO_COEF_TEMP) * delta_T
    return round(perda_frac * 100, 2)   # em %


# ─── 4. Otimização de inclinação (Cálculo III — função de múltiplas variáveis) ─
def irradiancia_inclinacao(beta_deg: float, azimute_deg: float = 0.0) -> float:
    """
    Modelo simplificado da irradiância em função do ângulo de inclinação β
    e azimute (0 = Norte verdadeiro no hemisfério Sul).

    Usa modelo cossenoidal derivado do ângulo solar zenital médio para
    Lucas do Rio Verde (Cálculo III — otimização de função multivariável).

    I(β, γ) = I_horiz × [cos(β) + sin(β) × cos(γ) × f(φ, δ)]
    Simplificado como função polinomial ajustada para a latitude local.
    """
    lat_rad   = np.radians(abs(LATITUDE))
    beta_rad  = np.radians(beta_deg)
    az_rad    = np.radians(azimute_deg)

    # Componente direta maximizada na latitude local (Cálculo III)
    fator_lat = np.cos(lat_rad - beta_rad) * np.cos(az_rad)
    fator_lat = max(fator_lat, 0)

    irradiancia_base = HSP_MEDIA_ANUAL
    return round(irradiancia_base * (0.80 + 0.20 * fator_lat), 3)


def angulo_otimo() -> dict:
    """
    Encontra o ângulo de inclinação β* que maximiza a irradiância anual.
    Varredura numérica (Cálculo III — otimização via gradiente discreto).
    """
    betas = np.arange(0, 45, 0.5)
    irr = [irradiancia_inclinacao(b) for b in betas]
    idx_max = int(np.argmax(irr))
    return {
        "angulo_otimo_graus": float(betas[idx_max]),
        "irradiancia_maxima": float(irr[idx_max]),
        "betas": betas.tolist(),
        "irradiancias": irr,
    }


# ─── 5. Resumo das perdas do sistema ─────────────────────────────────────────
def resumo_perdas() -> dict:
    return {
        "Inversor":         round(PERDA_INVERSOR * 100, 1),
        "Cabeamento":       round(PERDA_CABEAMENTO * 100, 1),
        "Sombreamento":     round(PERDA_SOMBREAMENTO * 100, 1),
        "Sujeira":          round(PERDA_SUJEIRA * 100, 1),
        "Temperatura":      round(PERDA_TEMPERATURA * 100, 1),
        "Total":            round((1 - FATOR_DESEMPENHO) * 100, 1),
    }
