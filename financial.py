"""
financial.py — Módulo de análise financeira
Disciplina: Matemática Financeira
Implementa: Payback simples e descontado, VPL, TIR, juros compostos e depreciação.
"""

import numpy as np
from data import (
    CUSTO_POR_KWP, TARIFA_ENERGIA_KWH, INFLACAO_ENERGIA_AA,
    TAXA_DESCONTO, VIDA_UTIL_ANOS, TAXA_DEPRECIACAO_AA,
    CUSTO_MANUTENCAO_AA
)


# ─── 1. Investimento inicial ──────────────────────────────────────────────────
def calcular_investimento(potencia_kWp: float) -> dict:
    """
    Custo total do projeto fotovoltaico.
    Inclui módulos, inversor, estrutura, cabeamento e instalação.
    """
    custo_total = potencia_kWp * CUSTO_POR_KWP
    custo_modulos = custo_total * 0.45
    custo_inversor = custo_total * 0.20
    custo_estrutura = custo_total * 0.10
    custo_instalacao = custo_total * 0.15
    custo_outros = custo_total * 0.10

    return {
        "custo_total":      round(custo_total, 2),
        "custo_modulos":    round(custo_modulos, 2),
        "custo_inversor":   round(custo_inversor, 2),
        "custo_estrutura":  round(custo_estrutura, 2),
        "custo_instalacao": round(custo_instalacao, 2),
        "custo_outros":     round(custo_outros, 2),
        "custo_por_kWp":    CUSTO_POR_KWP,
    }


# ─── 2. Fluxo de caixa anual (Matemática Financeira — juros compostos) ───────
def calcular_fluxo_caixa(
    geracao_anual_kwh: float,
    consumo_mensal_kwh: float,
    custo_total: float
) -> dict:
    """
    Projeta o fluxo de caixa ao longo da vida útil.

    Economia anual = min(geração, consumo) × tarifa × (1 + inflação)^t
    Depreciação anual dos módulos = TAXA_DEPRECIACAO × potência
    Custo de manutenção corrigido = CUSTO_MANUT × (1 + IPCA)^t  [IPCA ≈ 4,5%]
    """
    anos = list(range(1, VIDA_UTIL_ANOS + 1))
    fluxo_liquido = []
    fluxo_descontado = []
    acumulado = []
    economias = []
    manutencoes = []

    consumo_anual_kwh = consumo_mensal_kwh * 12
    # A geração pode cobrir no máximo o consumo (excedente vai para a rede)
    geracao_util_anual = min(geracao_anual_kwh, consumo_anual_kwh)

    acum = -custo_total   # investimento inicial no ano 0

    for t in anos:
        # Tarifa com inflação (juros compostos — Mat. Financeira)
        tarifa_t = TARIFA_ENERGIA_KWH * ((1 + INFLACAO_ENERGIA_AA) ** t)

        # Degradação dos módulos (Mat. Financeira — depreciação)
        fator_degradacao = (1 - TAXA_DEPRECIACAO_AA) ** t
        geracao_t = geracao_util_anual * fator_degradacao

        # Economia bruta
        economia_bruta = geracao_t * tarifa_t

        # Manutenção corrigida (IPCA = 4,5%)
        manutencao_t = CUSTO_MANUTENCAO_AA * ((1 + 0.045) ** t)

        # Fluxo líquido anual
        fl = economia_bruta - manutencao_t
        fluxo_liquido.append(round(fl, 2))

        # Fluxo descontado (VPL — Mat. Financeira)
        fl_desc = fl / ((1 + TAXA_DESCONTO) ** t)
        fluxo_descontado.append(round(fl_desc, 2))

        acum += fl
        acumulado.append(round(acum, 2))
        economias.append(round(economia_bruta, 2))
        manutencoes.append(round(manutencao_t, 2))

    return {
        "anos":               anos,
        "fluxo_liquido":      fluxo_liquido,
        "fluxo_descontado":   fluxo_descontado,
        "acumulado":          acumulado,
        "economias":          economias,
        "manutencoes":        manutencoes,
    }


# ─── 3. Payback simples e descontado (Matemática Financeira) ─────────────────
def calcular_payback(acumulado: list, fluxo_descontado: list,
                     custo_total: float) -> dict:
    """
    Payback Simples: primeiro ano em que o fluxo acumulado ≥ 0.
    Payback Descontado: considera o valor do dinheiro no tempo.
    """
    payback_simples = None
    for i, val in enumerate(acumulado):
        if val >= 0:
            payback_simples = i + 1
            break

    # Payback descontado — acumulado dos fluxos descontados
    acum_desc = -custo_total
    payback_descontado = None
    for i, fd in enumerate(fluxo_descontado):
        acum_desc += fd
        if acum_desc >= 0:
            payback_descontado = i + 1
            break

    return {
        "payback_simples_anos":     payback_simples,
        "payback_descontado_anos":  payback_descontado,
        "payback_simples_meses":    payback_simples * 12 if payback_simples else None,
    }


# ─── 4. VPL — Valor Presente Líquido (Matemática Financeira) ─────────────────
def calcular_vpl(fluxo_descontado: list, custo_total: float) -> dict:
    """
    VPL = -C0 + Σ [FC_t / (1 + i)^t]
    Critério: VPL > 0 → investimento viável.
    """
    vpl = -custo_total + sum(fluxo_descontado)
    return {
        "vpl": round(vpl, 2),
        "viavel": vpl > 0,
        "taxa_desconto_usada": TAXA_DESCONTO * 100,
    }


# ─── 5. TIR — Taxa Interna de Retorno (Matemática Financeira) ────────────────
def calcular_tir(fluxo_liquido: list, custo_total: float) -> float:
    """
    TIR: taxa i* tal que VPL(i*) = 0.
    Calculada por bissecção numérica (Cálculo III — métodos numéricos).
    """
    fluxos = [-custo_total] + fluxo_liquido

    def vpl_para_taxa(taxa):
        return sum(fc / (1 + taxa) ** t for t, fc in enumerate(fluxos))

    # Bissecção no intervalo [0.001, 1.0]
    lo, hi = 0.001, 1.0
    for _ in range(1000):
        mid = (lo + hi) / 2
        v = vpl_para_taxa(mid)
        if abs(v) < 0.01:
            return round(mid * 100, 2)
        if v > 0:
            lo = mid
        else:
            hi = mid
    return round(mid * 100, 2)


# ─── 6. Economia mensal (ano 1) ───────────────────────────────────────────────
def economia_mensal_ano1(geracao_mensal_kwh: dict, consumo_mensal_kwh: float) -> dict:
    """
    Calcula a economia mensal no 1º ano de operação para cada mês.
    """
    economia = {}
    for mes, g in geracao_mensal_kwh.items():
        util = min(g, consumo_mensal_kwh)
        economia[mes] = round(util * TARIFA_ENERGIA_KWH, 2)
    return economia


# ─── 7. CO₂ evitado ───────────────────────────────────────────────────────────
def co2_evitado(geracao_anual_kwh: float) -> dict:
    """
    Fator de emissão da rede elétrica brasileira: 0,0940 tCO₂/MWh (ONS 2023)
    """
    FATOR_EMISSAO = 0.0940 / 1000   # tCO₂/kWh → kgCO₂/kWh
    kg_por_ano = geracao_anual_kwh * FATOR_EMISSAO * 1000
    total_25_anos = kg_por_ano * 25 / 1000  # toneladas
    return {
        "kg_co2_ano":        round(kg_por_ano, 1),
        "ton_co2_25anos":    round(total_25_anos, 1),
        "arvores_eq":        round(total_25_anos * 1000 / 21.77),  # 1 árvore ≈ 21,77 kgCO₂/ano
    }
