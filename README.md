# Café Regenerativo | Protótipo ESG 

O protótipo parte de um problema real da cafeicultura (erosão, baixa infiltração e perda de produtividade) e demonstra uma solução simulada via práticas de agricultura regenerativa (cobertura vegetal entre linhas), avaliando impactos em indicadores econômicos e ambientais.

O protótipo está disponível em Hugging Face Spaces:

👉 [**Acesse o Dashboard Interativo aqui**](https://huggingface.co/spaces/Carlosaugusto-fre/cafe-regenera)

Este repositório apresenta um **dashboard interativo em Python/Dash** para análise comparativa entre os sistemas de **manejo convencional** e **regenerativo** na cafeicultura.  

O protótipo utiliza **dados simulados** e indicadores-chave de desempenho (**KPIs**) para ilustrar como práticas de agricultura regenerativa podem gerar ganhos em **sustentabilidade, eficiência de recursos e rentabilidade** — em alinhamento às diretrizes ESG e ao Pacto Global 2030.

**Objetivos Gerais:**
1. Apoiar produtores e empresas no monitoramento ESG.
2. Traduzir dados ambientais em métricas econômicas comparáveis.
3. Apoiar a transição para cadeias de suprimento mais sustentáveis.
   
---

## Introdução | Problema e Motivação

A cafeicultura brasileira enfrenta **desafios** como perda de solo, compactação, baixa infiltração de água, escorrimento superficial e redução da matéria orgânica. Esses fatores comprometem **produtividade, estabilidade do sistema e resiliência climática**.

A **agricultura regenerativa** surge como resposta, promovendo práticas que restauram a saúde do solo e alinham a produção com os princípios **ESG** (Environmental, Social, Governance). A iniciativa está em sintonia com o **Pacto Global da ONU (Agenda 2030)**, especialmente com os Objetivos de Desenvolvimento Sustentável:

- **ODS 2** — Fome Zero e Agricultura Sustentável  
- **ODS 12** — Consumo e Produção Responsáveis  
- **ODS 13** — Ação contra a Mudança Global do Clima  
- **ODS 15** — Vida Terrestre  

Além disso, normas como **ISO 14001 (Gestão Ambiental)**, **ISO 14064 (Inventário de GEE)** e **ISO 26000 (Responsabilidade Social)** fornecem referências para estruturar projetos que mensuram impacto ambiental e garantem boas práticas de governança.

---

### 1) Escopo do protótipo | Cobertura vegetal entre linhas de café

Uma das práticas centrais da agricultura regenerativa é a **cobertura vegetal entre as ruas de café**, que pode incluir diferentes espécies forrageiras e de adubação verde, como:

- *Arachis pintoi* — Amendoim forrageiro  
- *Brachiaria spp.* — Braquiária  
- *Cynodon spp.* — Tifton  
- *Pennisetum clandestinum* — Kikuyo  
- *Stylosanthes spp.* — Estilosantes  
- *Crotalaria spp.* — Crotalária  
- *Avena strigosa* — Aveia-preta  
- *Secale cereale* — Centeio  
- *Vicia sativa* — Ervilhaca  
- *Canavalia ensiformis* — Feijão-de-porco  
- *Cajanus cajan* — Guandu  

---

### 2) Principais benefícios

- 🌧️ **Proteção do solo** contra impacto direto da chuva e insolação  
- 💧 **Maior infiltração e retenção de umidade útil**  
- 🌱 **Aumento do carbono orgânico do solo (COS)** e da estabilidade de agregados  
- 🚫 **Redução de plantas daninhas** e menor erosão  
- 🌡️ **Melhoria do microclima**, refletindo em produtividade e qualidade dos grãos  


---


## 3) Objetivos do Protótipo

- Demonstrar como boas práticas de **cobertura vegetal entre linhas de café** influenciam:
  - Produtividade
  - Uso de água
  - Consumo de diesel
  - Fertilizantes
  - Carbono orgânico do solo
  - Pegada de carbono
  - Rentabilidade e margem líquida

- Construir um **painel interativo** que permita:
  - Visualizar KPIs financeiros e ambientais
  - Comparar sistemas convencional vs regenerativo
  - Explorar dados em gráficos dinâmicos
  - Benchmarking de indicadores

---

## Ferramentas

- **Python 3.12+**
- [Dash](https://dash.plotly.com/) (Plotly)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- **CSS Customizado** (Design e UX inspirados em Basedash)
- [Hugging Face Spaces](https://huggingface.co/spaces) (Deploy do protótipo)

---

## 📂 Estrutura do Repositório

```text
regenera-cafe-prototipo/
 ├── app.py              # Código principal do dashboard
 ├── dados_cafe.csv      # Base de dados simulada
 ├── style.css           # Estilos e tipografia customizada
 ├── README.md           # Documentação principal
 └── requirements.txt    # Dependências do projeto


