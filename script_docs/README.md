# ☕️ Simulação de Dados & Dashboard — Cafeicultura Convencional vs Regenerativa

Este diretório contém os scripts e recursos necessários para gerar dados fictícios de **cafeicultura convencional e regenerativa** e apresentá-los em um **dashboard interativo em Python (Dash + Plotly + Bootstrap)**.

---

## 📌 Estrutura da Pasta

```text
scrip_docs/
├── simulacao_cafe.py # Script de geração dos dados simulados
├── app.py # Dashboard interativo (Dash/Plotly)
├── dados_cafe.csv # Base de dados gerada pela simulação
└── assets/ # Recursos estáticos para o dashboard (CSS customizado, imagens, etc.)


---

## 📌 1) Simulação de Dados — `simulacao_cafe.py`

📍 **Função**  
- Gera o arquivo `dados_cafe.csv` com informações de **50 fazendas**, para os anos de 2022 a 2024:contentReference[oaicite:0]{index=0}.  
- Variáveis simuladas incluem:
  - **Econômicas**: custo total, receita, margem, rentabilidade.  
  - **Produtivas**: produtividade (sacas/ha), custo por saca, produção total.  
  - **Ambientais**: carbono orgânico no solo, erosão, biodiversidade, infiltração, uso de água, emissões de GEE (diesel + fertilizantes).  

📤 **Saída**: `dados_cafe.csv`

---

## 📌 2) Dashboard Interativo — `app.py`

📍 **Função**  
- Consome o arquivo `dados_cafe.csv` e gera um **dashboard interativo**.  
- Permite explorar os impactos econômicos e ambientais da **agricultura regenerativa vs convencional**.  

📊 **Recursos disponíveis**:
- Cartões de **KPIs principais** (produtividade, custo por saca, margem líquida, pegada de carbono etc.).  
- **Gráficos interativos**:
  - Benchmark de diferenças (%).  
  - Dispersão (correlações entre indicadores).  
  - Boxplots por manejo.  
  - Séries temporais.  
- Design customizado via **`assets/style.css`**.

📤 **Saída**: aplicação acessível em `http://localhost:7860`

---

## 📌 3) Pasta de Estilos — `assets/`

📍 **Função**  
- Contém o arquivo **CSS personalizado** que ajusta a estética do dashboard.  
- Permite modificar cores, fontes, margens e identidade visual do protótipo.  

---

## ▶️ Como Executar o Projeto

1. **Instale as dependências**  
   ```bash
   pip install numpy pandas dash plotly dash-bootstrap-components

2. **Gere os dados simulados**
   ```bash
   python simulacao_cafe.py

3. Rode o dashboard
   ```bash
   python app.py

---


## 🎯 4) Objetivo do Projeto

**Este pipeline demonstra como:**

-Dados simulados podem representar cenários agrícolas realistas.

-KPIs econômicos e ambientais ajudam a comparar práticas de manejo.

-Dashboards interativos comunicam de forma clara e dinâmica os resultados.

**Aplicações possíveis:**

-Estudos em agricultura regenerativa vs convencional.

-Treinamento em ESG e indicadores de sustentabilidade.

-Protótipo de portfólio em ciência de dados aplicada ao agro.
