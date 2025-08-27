# Pasta `data/`

Esta pasta contém os **dados simulados** que alimentam o protótipo de dashboard ESG para a cafeicultura.

---

## Arquivo Principal

### `dados_cafe.csv`

- **Origem:** gerado automaticamente pelo script [`simulacao_cafe.py`](../docs/simulacao_cafe.py).  
- **Objetivo:** servir como **banco de dados fictício** para análises comparativas entre **manejo convencional** e **manejo regenerativo**.  
- **Granularidade:** 50 fazendas simuladas, em 3 anos (2022, 2023, 2024).  

---

### Estrutura dos Dados

Cada linha do CSV representa uma **fazenda em um determinado ano**.  
As colunas incluem variáveis **econômicas, ambientais e produtivas**:

- 🔑 `farm_id` — identificação da fazenda  
- 📅 `ano` — ano de referência  
- 🌱 `sistema` — manejo (`convencional` ou `regenerativo`)  
- 📐 `area_ha` — área da fazenda (hectares)  
- ☔ `chuva_mm` — chuva média anual  

### Indicadores Produtivos
- `produtividade_sacas_ha` — sacas produzidas por hectare  
- `producao_total_sacas` — produção total em sacas  
- `custo_por_saca_Reais` — custo unitário (R$/saca)  

### Indicadores Econômicos
- `receita_total_RSha` — receita por hectare (R$/ha)  
- `custo_total_RSha` — custo total por hectare (R$/ha)  
- `rentabilidade_RSha` — rentabilidade por hectare (R$/ha)  
- `margem_liquida` — proporção de lucro sobre receita  

### Indicadores Ambientais
- `C_organico_gkg` — carbono orgânico do solo (g/kg)  
- `erosao_ton_ha` — erosão (t/ha)  
- `infiltracao_mm_h` — infiltração de água (mm/h)  
- `biodiversidade_indice` — índice de biodiversidade (0–10)  

### Indicadores de Insumos
- `diesel_Lha` — consumo de diesel por hectare (L/ha)  
- `N_kg_ha` — fertilizante nitrogenado aplicado (kg/ha)  
- `herbicida_Lha` — herbicida (L/ha)  
- `irrigacao_mm` — irrigação (mm/ano)  
- `agua_pulverizacao_Lha` — água usada em pulverização (L/ha)  
- `agua_total_m3ha` — uso total de água (m³/ha)  

### Emissões de GEE
- `GHG_diesel_kgCO2e_ha` — emissões de diesel (kg CO₂e/ha)  
- `GHG_N_total_kgCO2e_ha` — emissões de fertilizantes (kg CO₂e/ha)  
- `GHG_total_kgCO2e_ha` — emissões totais (kg CO₂e/ha)  
- `GHG_kgCO2e_saca` — emissões por saca (kg CO₂e/saca)  
- `CI_ha_tCO2e` — intensidade de carbono por hectare (t CO₂e/ha)  
- `CI_saca_tCO2e` — intensidade de carbono por saca (t CO₂e/saca)  

---

## Como usar

Este dataset é usado por:

- [`app.py`](../docs/app.py) → para alimentar o **dashboard interativo**.  
- Análises estatísticas e de benchmarking em Python/Power BI.  

Exemplo de carregamento em Python:

```python
import pandas as pd

df = pd.read_csv("data/dados_cafe.csv")
print(df.head())

> **Nota**  
> Estes dados são **totalmente simulados**.  
> Eles **não representam valores reais** de produtividade ou emissões da cafeicultura, e têm apenas caráter **educacional e de prototipagem ESG**.

