"""financial.py — Matemática Financeira"""
import numpy as np
from data import (TARIFA_ENERGIA_KWH, INFLACAO_ENERGIA_AA, TAXA_DESCONTO,
                  VIDA_UTIL_ANOS, TAXA_DEPRECIACAO_AA, CUSTO_MANUTENCAO_AA,
                  FATOR_EMISSAO_CO2_KG_KWH, custo_por_kwp)

def calcular_investimento(kwp):
    c = round(kwp * custo_por_kwp(kwp), 2)
    return {"custo_total":c,"custo_por_kwp":round(custo_por_kwp(kwp)),
            "custo_modulos":round(c*.45,2),"custo_inversor":round(c*.20,2),
            "custo_estrutura":round(c*.10,2),"custo_instalacao":round(c*.15,2),"custo_outros":round(c*.10,2)}

def calcular_fluxo_caixa(ger_anual, consumo_mes, custo_total):
    consumo_anual = consumo_mes * 12
    ger_util = min(ger_anual, consumo_anual)
    anos,fl,fd,acum,ecos = [],[],[],[],[]
    acc = -custo_total
    for t in range(1, VIDA_UTIL_ANOS+1):
        tar = TARIFA_ENERGIA_KWH * (1+INFLACAO_ENERGIA_AA)**t
        gt  = ger_util * (1-TAXA_DEPRECIACAO_AA)**t
        eco = gt * tar
        man = CUSTO_MANUTENCAO_AA * (1+0.045)**t
        f_l = eco - man
        f_d = f_l / (1+TAXA_DESCONTO)**t
        acc += f_l
        anos.append(t); fl.append(round(f_l,2)); fd.append(round(f_d,2))
        acum.append(round(acc,2)); ecos.append(round(eco,2))
    return {"anos":anos,"fluxo_liquido":fl,"fluxo_descontado":fd,"acumulado":acum,"economias":ecos}

def calcular_payback(acum, fd, custo_total):
    pb_s = next((i+1 for i,v in enumerate(acum) if v>=0), None)
    acc  = -custo_total; pb_d = None
    for i,v in enumerate(fd):
        acc += v
        if acc >= 0: pb_d = i+1; break
    return {"payback_simples_anos":pb_s,"payback_descontado_anos":pb_d}

def calcular_vpl(fd, custo_total):
    v = -custo_total + sum(fd)
    return {"vpl":round(v,2),"viavel":v>0}

def calcular_tir(fl, custo_total):
    fluxos = [-custo_total]+fl
    def _v(r): return sum(c/(1+r)**t for t,c in enumerate(fluxos))
    lo,hi = 0.001,5.0
    for _ in range(500):
        m=(lo+hi)/2
        if _v(m)>0: lo=m
        else: hi=m
    return round(m*100,1)

def co2_evitado(ger_anual):
    kg = ger_anual * FATOR_EMISSAO_CO2_KG_KWH
    t25 = kg * VIDA_UTIL_ANOS / 1000
    return {"kg_co2_ano":round(kg,1),"ton_co2_25anos":round(t25,1),"arvores_eq":round(t25*1000/21.77)}
