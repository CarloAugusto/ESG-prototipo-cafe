# 🎨 Estilos do Dashboard — `style.css`

Este diretório contém os recursos de **estilo visual** para o dashboard (`app.py`).  
O arquivo principal é **`style.css`**, que define a identidade gráfica do protótipo, com foco em **tema escuro moderno, tipografia refinada e usabilidade**.

---

## 📌 Estrutura do `style.css`

### 🎨 Paleta de Cores
Definida em variáveis globais para fácil customização:
- **Fundo**: gradiente do cinza-azulado escuro (`--bg-start`, `--bg-end`)  
- **Cards**: tons intermediários (`--card`, `--card-hover`)  
- **Acentos**: verde `--accent` (#58D68D) e azul `--accent2` (#5DADE2)  
- **Texto**: claro (`--text`) e secundário (`--muted`)  

---

### 🖋️ Tipografia
- Fonte base: **Inter / Segoe UI / Roboto**  
- Títulos e destaques: **Playfair Display** e **DM Serif Display** (Google Fonts)  
- Subtítulos e rodapé com estilo refinado e peso leve.  

---

### 🧩 Componentes Estilizados
- **Header fixo** com título, subtítulo e "hero text".  
- **Cards** com bordas arredondadas, hover com sombra verde-azul.  
- **KPI cards** compactos, com valores destacados e diferença em verde.  
- **Dropdowns compactos (`.dd-compact`)**: altura reduzida, fundo escuro integrado ao card.  
- **Tabelas** com cabeçalho preto, corpo cinza escuro e rolagem vertical.  
- **Gráficos Plotly**: toolbar oculta, cores integradas ao tema.  
- **Rodapé** centralizado, com tipografia elegante.  

---

### ⚙️ Recursos Especiais
- **Header sticky**: permanece fixo ao rolar a página.  
- **Hero section**: destaque inicial com tipografia serifada (estilo editorial).  
- **Separadores de seção (`.section-separator`)** para espaçamento harmonioso.  
- **Responsividade**: ajustes de espaçamento com `.tight` e `gx/gy`.  

---

## 📌 Estrutura da Pasta

   ```text
   assets/
   ├── style.css # Estilos globais para o dashboard

---

## ▶️ Como funciona no Dash

O Dash reconhece automaticamente qualquer arquivo dentro da pasta **`assets/`**.  
Assim, ao rodar o `app.py`, o estilo definido em `style.css` é carregado sem necessidade de importação manual.

---

## 🎯 Objetivo do CSS

O `style.css` garante que o dashboard:
- Tenha uma **identidade visual moderna e consistente**.  
- Reforce a mensagem de **profissionalismo + sustentabilidade (verde/azul)**.  
- Seja **agradável de usar**, com foco em clareza dos KPIs e estética minimalista.  



