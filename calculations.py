"""calculations.py — Física III + Cálculo III"""
import numpy as np
from data import (FATOR_DESEMPENHO, MODULO_POTENCIA_WP, MODULO_AREA_M2,
                  MODULO_COEF_TEMP, TEMP_REFERENCIA, TEMP_OPERACAO_LOCAL,
                  PERDA_INVERSOR, PERDA_CABEAMENTO, PERDA_SOMBREAMENTO,
                  PERDA_SUJEIRA, PERDA_TEMPERATURA, MESES, DIAS_POR_MES, LATITUDE)

def calcular_potencia_sistema(consumo_kwh_mes, hsp_anual, pr=None):
    pr = pr or FATOR_DESEMPENHO
    pot = (consumo_kwh_mes * 1.10) / (hsp_anual * pr * 30)
    n   = int(np.ceil(pot * 1000 / MODULO_POTENCIA_WP))
    kwp = round(n * MODULO_POTENCIA_WP / 1000, 3)
    return {"potencia_kWp": kwp, "n_modulos": n, "area_m2": round(n*MODULO_AREA_M2, 2)}

def calcular_geracao_mensal(kwp, hsp_mensal, pr=None):
    pr = pr or FATOR_DESEMPENHO
    ger = {}
    for i, m in enumerate(MESES):
        ger[m] = round(kwp * hsp_mensal[m] * DIAS_POR_MES[i] * pr, 1)
    return {"geracao_kwh": ger, "anual": round(sum(ger.values()), 1)}

def perda_por_temperatura(t=TEMP_OPERACAO_LOCAL):
    return round(abs(MODULO_COEF_TEMP) * (t - TEMP_REFERENCIA) * 100, 2)

def angulo_otimo(lat, ghi):
    betas = np.arange(0, 45, 0.5)
    irrs  = [float(ghi * (0.80 + 0.20 * np.cos(np.radians(abs(lat) - b)))) for b in betas]
    idx   = int(np.argmax(irrs))
    return {"angulo": float(betas[idx]), "irrs": irrs, "betas": betas.tolist()}

def resumo_perdas():
    return {
        "Inversor":    round(PERDA_INVERSOR*100,1),
        "Cabeamento":  round(PERDA_CABEAMENTO*100,1),
        "Sombreamento":round(PERDA_SOMBREAMENTO*100,1),
        "Sujeira":     round(PERDA_SUJEIRA*100,1),
        "Temperatura": round(PERDA_TEMPERATURA*100,1),
        "Total":       round((1-FATOR_DESEMPENHO)*100,1),
    }
