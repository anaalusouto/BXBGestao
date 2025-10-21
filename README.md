# 📊 Ferramenta de Visualização Ágil (Burndown & Burnup)

Este projeto é uma aplicação desktop em Python projetada para equipes Ágeis (Scrum/Kanban) que precisam monitorar o progresso de Sprints ou projetos de forma visual e intuitiva. Ela permite a geração seletiva dos gráficos **Burndown** e **Burnup** a partir de entradas de dados simples, ajudando a garantir transparência e a tomar decisões baseadas em dados.

## ✨ Destaques do Projeto

  * **Seleção de Gráfico:** Alternância fácil entre as visualizações Burndown e Burnup.
  * **Entrada de Dados Simplificada:** Formulário dinâmico que se ajusta ao número de dias da Sprint.
  * **Foco Global:** Os gráficos rastreiam o progresso do time em relação à meta (em Horas ou Pontos).

## 🚀 Tecnologias Utilizadas

  * **Python 3.x**
  * **CustomTkinter:** Para a criação da interface gráfica (GUI).
  * **Matplotlib:** Para plotar e renderizar os gráficos.
  * **NumPy:** Para cálculos eficientes de dados (linhas ideais e acumuladas).

## 📋 Como Utilizar

A aplicação foi projetada para ser simples e autoexplicativa:

### Configuração Inicial

1.  **Nome do Projeto:** Defina o título do gráfico.
2.  **Escolha o Gráfico:** Selecione **Burndown** ou **Burnup**.
3.  **Dias Úteis:** Informe a duração da sua Sprint.
4.  **Demanda Inicial:** Informe o total de Horas/Pontos no início da Sprint.

### Entrada de Dados Diária (Seção 4)

O formulário de **Dados Diários** será gerado automaticamente.

| Gráfico Selecionado | Campo Principal | O que Inserir |
| :--- | :--- | :--- |
| **Burndown** | **Trabalho RESTANTE** | A estimativa total de Horas/Pontos que *ainda precisa ser feita* no final do dia. |
| **Burnup** | **Entregas Acumuladas** | O total acumulado de Horas/Pontos *concluídos* até o final do dia. |
| **Ambos** | **Demandas Totais (Meta)** | O Escopo total de Horas/Pontos. Altere este valor apenas se houver **adição ou remoção formal** de trabalho na Sprint. |

-----

## 🎨 Cores dos Gráficos (Baseado no Código)

| Gráfico | Linha | Significado | Cor |
| :--- | :--- | :--- | :--- |
| **Ambos** | Planejado (Ideal) | Ritmo de progresso esperado. | Verde (`#4CAF50`) |
| **Burndown** | Real | O trabalho que *resta*. | Vermelho (`#E74C3C`) |
| **Burnup** | Entregas | O trabalho *concluído* (Progresso Real). | Azul (`#3498DB`) |
| **Burndown** | Meta Total | O Escopo Total (Muda se houver *Scope Creep*). | Cinza (`darkgray`) |

## 🤝 Contribuições

Contribuições são bem-vindas\! Se você encontrar um bug ou tiver ideias para novos recursos (como persistência de dados em SQLite), sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

**Desenvolvido com Python, Matplotlib e CustomTkinter.**
