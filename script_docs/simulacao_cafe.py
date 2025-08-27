import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# 0) SEMENTE E PARÂMETROS GERAIS
# -------------------------------------------------------------------
np.random.seed(42)

N_FARMS = 50
ANOS = [2022, 2023, 2024]  # pode estender depois

# Preço da saca por ano (R$)
PRECO_SACA = {
    2022: 1200,
    2023: 1800,   # pico recente
    2024: 1500
}

# Inflator de custos por ano (base 2022 = 1.00)
INFLACAO_CUSTO = {
    2022: 1.00,
    2023: 1.10,
    2024: 1.18
}

# Chuva média (mm/ano) por ano (para variar um pouco o contexto hídrico)
CHUVA_MM = {
    2022: 1100,
    2023: 950,    # ano mais seco
    2024: 1200
}

# -------------------------------------------------------------------
# 1) FATORES DE EMISSÃO (PADRÃO / PRONTOS PARA TROCA)
# -------------------------------------------------------------------
# Diesel: ~2.68 kg CO2 por litro (combustão + upstream simplificado)
EF_DIESEL_KGCO2_PER_L = 2.68

# Fertilizante N:
# - Emissões upstream (produção, transporte): ~6.3 kg CO2e/kg N (valor de ordem de grandeza; documente no README)
EF_UPSTREAM_N_KGCO2E_PER_KG = 6.3

# - Emissão no solo (Tier 1 IPCC):
#   EF1 = 0.01 kg N2O-N / kg N aplicado
#   N2O (kg) = N2O-N * (44/28) = 1.571 * N2O-N
#   CO2e = N2O * GWP100; aqui usamos AR4=298 (comum em inventários legados)
EF1_N2O_N_PER_KG_N = 0.01
N2O_TO_CO2E = 298
CONV_N2O_N_TO_N2O = 44/28  # = 1.571428...


def ghg_from_n_soil_kgco2e_per_kgN():
    return EF1_N2O_N_PER_KG_N * CONV_N2O_N_TO_N2O * N2O_TO_CO2E  # kg CO2e / kg N no solo


EF_SOIL_N_KGCO2E_PER_KG = ghg_from_n_soil_kgco2e_per_kgN()

# Total por kg de N (upstream + solo)
EF_TOTAL_N_KGCO2E_PER_KG = EF_UPSTREAM_N_KGCO2E_PER_KG + EF_SOIL_N_KGCO2E_PER_KG
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 2) SIMULAÇÃO
# -------------------------------------------------------------------
linhas = []

for ano in ANOS:
    for farm in range(1, N_FARMS + 1):
        sistema = np.random.choice(
            ["convencional", "regenerativo"], p=[0.5, 0.5])
        area_ha = np.random.uniform(5, 30)

        # Parâmetros base por sistema (médias realistas + variação)
        if sistema == "convencional":
            prod_ha = np.random.uniform(25, 35)                   # sacas/ha
            C_org = np.random.uniform(10, 15)                     # g/kg
            irrig_mm = np.random.uniform(300, 500)                # mm
            diesel_Lha = np.random.uniform(60, 100)               # L/ha
            N_kg_ha = np.random.uniform(150, 200)                 # kg/ha
            # L/ha de herbicida (para ilustrar)
            herb_Lha = np.random.uniform(3, 7)
            # L/ha de água para pulverização
            h2o_pulv_Lha = np.random.uniform(400, 800)
            erosao_t_ha = np.random.uniform(2.0, 6.0)             # t/ha
            infiltr_mm_h = np.random.uniform(10, 20)              # mm/h
            biodiversidade = np.random.uniform(2.0, 5.0)          # 0-10

            # Custo base (R$/ha), ajustado por inflação do ano
            custo_RSha = np.random.uniform(8000, 10000) * INFLACAO_CUSTO[ano]

        else:
            prod_ha = np.random.uniform(28, 38)
            C_org = np.random.uniform(15, 25)
            irrig_mm = np.random.uniform(200, 400)
            diesel_Lha = np.random.uniform(40, 70)
            N_kg_ha = np.random.uniform(120, 170)
            herb_Lha = np.random.uniform(0.5, 3.0)
            h2o_pulv_Lha = np.random.uniform(250, 600)
            erosao_t_ha = np.random.uniform(0.5, 3.0)
            infiltr_mm_h = np.random.uniform(20, 35)
            biodiversidade = np.random.uniform(5.0, 8.5)

            custo_RSha = np.random.uniform(7000, 9000) * INFLACAO_CUSTO[ano]

        # Produção total (sacas) e receita
        producao_sacas = prod_ha * area_ha
        preco_saca = PRECO_SACA[ano]
        receita_RSha = prod_ha * preco_saca

        # Água total (m³/ha): irrigação + água de pulverização
        # 1 mm = 1 L/m²; 1 ha = 10.000 m² => mm * 10.000 L/ha => /1000 = m³/ha
        h2o_irrig_m3ha = (irrig_mm * 10000) / 1000.0
        h2o_pulv_m3ha = h2o_pulv_Lha / 1000.0
        h2o_total_m3ha = h2o_irrig_m3ha + h2o_pulv_m3ha

        # Emissões GHG (kg CO2e/ha) — diesel + N total (upstream + solo)
        ghg_diesel_kgco2e_ha = diesel_Lha * EF_DIESEL_KGCO2_PER_L
        ghg_N_kgco2e_ha = N_kg_ha * EF_TOTAL_N_KGCO2E_PER_KG
        ghg_total_kgco2e_ha = ghg_diesel_kgco2e_ha + ghg_N_kgco2e_ha

        # Emissões por saca (kg CO2e/saca) — dividir por produtividade por ha
        ghg_kgco2e_saca = ghg_total_kgco2e_ha / max(prod_ha, 1e-6)

        # KPIs econômicos
        custo_por_saca = custo_RSha / max(prod_ha, 1e-6)
        rentabilidade_RSha = receita_RSha - custo_RSha
        margem = rentabilidade_RSha / max(receita_RSha, 1e-6)

        # KPIs ambientais/operacionais
        produtividade_hidrica = (prod_ha * 60) / \
            max(h2o_total_m3ha, 1e-6)  # kg café / m³ água
        diesel_por_saca = diesel_Lha / max(prod_ha, 1e-6)
        ci_ha_tco2e = ghg_total_kgco2e_ha / 1000.0
        ci_saca_tco2e = ghg_kgco2e_saca / 1000.0

        linhas.append(dict(
            farm_id=farm,
            ano=ano,
            sistema=sistema,
            area_ha=area_ha,
            chuva_mm=CHUVA_MM[ano],
            produtividade_sacas_ha=prod_ha,
            producao_total_sacas=producao_sacas,
            preco_saca_Reais=preco_saca,
            receita_total_RSha=receita_RSha,
            custo_total_RSha=custo_RSha,
            custo_por_saca_Reais=custo_por_saca,
            rentabilidade_RSha=rentabilidade_RSha,
            margem_liquida=margem,

            C_organico_gkg=C_org,
            erosao_ton_ha=erosao_t_ha,
            infiltracao_mm_h=infiltr_mm_h,
            biodiversidade_indice=biodiversidade,

            irrigacao_mm=irrig_mm,
            agua_pulverizacao_Lha=h2o_pulv_Lha,
            agua_total_m3ha=h2o_total_m3ha,
            produtividade_hidrica_kg_m3=produtividade_hidrica,

            diesel_Lha=diesel_Lha,
            diesel_por_saca_L=diesel_por_saca,

            N_kg_ha=N_kg_ha,
            herbicida_Lha=herb_Lha,

            GHG_diesel_kgCO2e_ha=ghg_diesel_kgco2e_ha,
            GHG_N_total_kgCO2e_ha=ghg_N_kgco2e_ha,
            GHG_total_kgCO2e_ha=ghg_total_kgco2e_ha,
            GHG_kgCO2e_saca=ghg_kgco2e_saca,
            CI_ha_tCO2e=ci_ha_tco2e,
            CI_saca_tCO2e=ci_saca_tco2e
        ))

df = pd.DataFrame(linhas)

# Ordenar para visualização amigável
df = df.sort_values(["farm_id", "ano"]).reset_index(drop=True)

# Salvar CSV
df.to_csv("dados_cafe.csv", index=False, encoding="utf-8-sig")
print("OK! 'dados_cafe.csv' gerado com", len(df), "linhas.")
print(df.head(10))
