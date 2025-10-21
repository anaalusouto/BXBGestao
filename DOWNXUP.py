import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HIGHLIGHT_COLOR = "#1F6AA5"
SUCCESS_COLOR = "#4CAF50"
REAL_COLOR_BURNDOWN = "#E74C3C"
PROGRESS_COLOR_BURNUP = "#3498DB"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class AppGraficosVisuais(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.daily_inputs = []
        self.canvas_widget = None
        self.grafico_selecionado = ctk.StringVar(value="Burndown")

        self.title("Ferramenta Ágil de Visualização")
        self.geometry("1100x750")
        self.resizable(True, True)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(self, width=380, corner_radius=15)
        self.input_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(9, weight=1)

        ctk.CTkLabel(self.input_frame,
                     text="PAINEL DE DADOS ÁGEIS",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=HIGHLIGHT_COLOR).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.cria_input("Nome do Gráfico (Sprint/Projeto):", 1, "Sprint Principal", "projeto_entry")

        ctk.CTkLabel(self.input_frame, text="1. Escolha o Gráfico:", anchor="w", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=20, pady=(15, 0), sticky="ew")
        self.optionmenu_grafico = ctk.CTkOptionMenu(self.input_frame,
                                                    values=["Burndown", "Burnup"],
                                                    variable=self.grafico_selecionado,
                                                    command=self.regenerar_formulario,
                                                    font=ctk.CTkFont(size=14),
                                                    button_color=HIGHLIGHT_COLOR)
        self.optionmenu_grafico.grid(row=4, column=0, padx=20, pady=(5, 15), sticky="ew")

        self.cria_input("2. Dias Úteis Totais:", 5, "10", "dias_uteis_entry", command=self.regenerar_formulario)
        self.cria_input("3. DEMANDA INICIAL (Pontos/Horas):", 7, "100.0", "demanda_inicial_entry",
                        command=self.regenerar_formulario)

        self.scroll_frame = ctk.CTkScrollableFrame(self.input_frame,
                                                   label_text="4. DADOS DIÁRIOS (ENTRADA)",
                                                   label_font=ctk.CTkFont(weight="bold", size=14),
                                                   corner_radius=10)
        self.scroll_frame.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.gerar_button = ctk.CTkButton(self.input_frame,
                                          text="GERAR VISUALIZAÇÃO",
                                          command=self.gerar_e_plotar,
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          fg_color=HIGHLIGHT_COLOR,
                                          hover_color="#18507E",
                                          height=40)
        self.gerar_button.grid(row=10, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.mensagem_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", wraplength=360)
        self.mensagem_label.grid(row=11, column=0, padx=20, pady=5, sticky="ew")

        self.plot_frame = ctk.CTkFrame(self, corner_radius=15)
        self.plot_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_rowconfigure(0, weight=1)

        self.placeholder_label = ctk.CTkLabel(self.plot_frame,
                                              text="O gráfico escolhido será exibido aqui.",
                                              font=ctk.CTkFont(size=18, slant="italic"))
        self.placeholder_label.pack(expand=True, fill="both", padx=20, pady=20)

        self.regenerar_formulario()

    def cria_input(self, label_text, row, default_value, attribute_name, command=None):
        label = ctk.CTkLabel(self.input_frame, text=label_text, anchor="w", font=ctk.CTkFont(weight="bold"))
        label.grid(row=row, column=0, padx=20, pady=(10, 0), sticky="ew")

        entry = ctk.CTkEntry(self.input_frame, corner_radius=8)
        entry.insert(0, default_value)
        entry.grid(row=row + 1, column=0, padx=20, pady=(0, 10), sticky="ew")

        if command:
            entry.bind("<FocusOut>", lambda event: command())

        setattr(self, attribute_name, entry)

    def mostrar_mensagem(self, texto, cor="red"):
        self.mensagem_label.configure(text=texto, text_color=cor)

    def regenerar_formulario(self, *args):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.daily_inputs = []

        try:
            dias_uteis = int(self.dias_uteis_entry.get())
            demanda_inicial = float(self.demanda_inicial_entry.get())

            if dias_uteis <= 0 or demanda_inicial <= 0:
                raise ValueError("Dias e Demanda Inicial devem ser maiores que zero.")
        except ValueError:
            ctk.CTkLabel(self.scroll_frame, text="Verifique os campos de dias e demanda inicial.",
                         text_color="red").pack(pady=10)
            return

        grafico = self.grafico_selecionado.get()

        for i in range(1, dias_uteis + 1):
            frame_dia = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
            frame_dia.pack(fill="x", padx=10, pady=5)
            frame_dia.grid_columnconfigure((0, 1), weight=1)

            ctk.CTkLabel(frame_dia, text=f"DIA {i}", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0,
                                                                                           padx=(10, 5),
                                                                                           pady=(5, 0), columnspan=2,
                                                                                           sticky="w")

            daily_data = {}

            if grafico == "Burndown":
                ctk.CTkLabel(frame_dia, text="Restante:", anchor="w").grid(row=1, column=0, padx=(10, 5), sticky="w")
                restante_entry = ctk.CTkEntry(frame_dia, width=100)
                restante_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")
                daily_data['restante'] = restante_entry

                ctk.CTkLabel(frame_dia, text="Meta Total:", anchor="w").grid(row=2, column=0, padx=(10, 5), sticky="w")
                demandas_entry = ctk.CTkEntry(frame_dia, width=100)
                demandas_entry.insert(0, str(demanda_inicial))
                demandas_entry.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")
                daily_data['demandas'] = demandas_entry

            else:
                ctk.CTkLabel(frame_dia, text="Entregas Acum.:", anchor="w").grid(row=1, column=0, padx=(10, 5),
                                                                                 sticky="w")
                entregas_entry = ctk.CTkEntry(frame_dia, width=100)
                entregas_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")
                daily_data['entregas'] = entregas_entry

                ctk.CTkLabel(frame_dia, text="Demandas Totais:", anchor="w").grid(row=2, column=0, padx=(10, 5),
                                                                                  sticky="w")
                demandas_entry = ctk.CTkEntry(frame_dia, width=100)
                demandas_entry.insert(0, str(demanda_inicial))
                demandas_entry.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")
                daily_data['demandas'] = demandas_entry

            self.daily_inputs.append(daily_data)

        self.scroll_frame.configure(label_text=f"4. DADOS DIÁRIOS ({grafico})")
        self.mostrar_mensagem(f"Formulário {grafico} criado. Preencha os dados.", cor=SUCCESS_COLOR)
        self.preencher_exemplo()

    def preencher_exemplo(self):

        dias_uteis = int(self.dias_uteis_entry.get())
        if dias_uteis < 10: return

        grafico = self.grafico_selecionado.get()

        try:
            if grafico == "Burndown":
                ex_restante = [95, 88, 75, 50, 30, 15, 8, 4, 1, 0]
                ex_meta = [100, 100, 100, 105, 105, 105, 105, 105, 105, 105]
                for i in range(min(dias_uteis, len(ex_restante))):
                    self.daily_inputs[i]['restante'].delete(0, 'end')
                    self.daily_inputs[i]['restante'].insert(0, str(ex_restante[i]))
                    self.daily_inputs[i]['demandas'].delete(0, 'end')
                    self.daily_inputs[i]['demandas'].insert(0, str(ex_meta[i]))

            else:
                ex_entregas = [5, 12, 18, 25, 38, 55, 68, 80, 88, 92]
                ex_demandas = [100, 100, 105, 105, 105, 110, 110, 115, 115, 118]
                for i in range(min(dias_uteis, len(ex_entregas))):
                    self.daily_inputs[i]['entregas'].delete(0, 'end')
                    self.daily_inputs[i]['entregas'].insert(0, str(ex_entregas[i]))
                    self.daily_inputs[i]['demandas'].delete(0, 'end')
                    self.daily_inputs[i]['demandas'].insert(0, str(ex_demandas[i]))
        except Exception:
            pass

    def parse_inputs(self):
        dados = {}
        try:
            dias_uteis = int(self.dias_uteis_entry.get())
            demanda_inicial = float(self.demanda_inicial_entry.get())

            dados['nome'] = self.projeto_entry.get()
            dados['dias'] = np.arange(0, dias_uteis + 1)
            dados['dias_uteis'] = dias_uteis
            dados['demanda_inicial'] = demanda_inicial
            dados['grafico'] = self.grafico_selecionado.get()

            taxa_ideal = demanda_inicial / dias_uteis

            demandas_diarias = []

            if dados['grafico'] == "Burndown":
                dados['planejado'] = (demanda_inicial - (dados['dias'] * taxa_ideal)).tolist()

                restante_diario = []
                for d in self.daily_inputs:
                    restante_diario.append(float(d['restante'].get()))
                    demandas_diarias.append(float(d['demandas'].get()))

                dados['real'] = [demanda_inicial] + restante_diario
                dados['demandas'] = [demanda_inicial] + demandas_diarias  # Meta Total

            else:
                dados['planejado'] = (dados['dias'] * taxa_ideal).tolist()

                entregas_diarias = []
                for d in self.daily_inputs:
                    entregas_diarias.append(float(d['entregas'].get()))
                    demandas_diarias.append(float(d['demandas'].get()))

                dados['entregas'] = [0.0] + entregas_diarias
                dados['demandas'] = [demanda_inicial] + demandas_diarias  # Escopo Total

            return dados

        except ValueError:
            self.mostrar_mensagem("Erro: Certifique-se de que todos os valores são numéricos e preenchidos.", cor="red")
            return None
        except Exception as e:
            self.mostrar_mensagem(f"Erro inesperado: {e}", cor="red")
            return None

    def gerar_e_plotar(self):
        dados = self.parse_inputs()
        if dados is None:
            return

        self.mostrar_mensagem(f"Gráfico {dados['grafico']} em geração...", cor=HIGHLIGHT_COLOR)

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        plt.style.use('default')

        ax.set_facecolor('white')
        ax.grid(True, linestyle=':', alpha=0.6, color='gray')

        TEXT_COLOR = 'black'


        if dados['grafico'] == "Burndown":
            ax.plot(dados['dias'], dados['demandas'], label='Meta (Total)', color='darkgray', linestyle=':',
                    linewidth=1.5)
            ax.plot(dados['dias'], dados['planejado'], label='Planejado (Ideal)', color=SUCCESS_COLOR, linestyle='--',
                    linewidth=2)
            ax.plot(dados['dias'], dados['real'], label='Real (Restante)', color=REAL_COLOR_BURNDOWN, linewidth=3,
                    marker='o')

            ax.set_title(f"GRÁFICO BURNDOWN: {dados['nome']}", color=TEXT_COLOR, fontsize=16)
            ax.set_ylabel('DEMANDA (Restante)', color=TEXT_COLOR)
            ax.set_ylim(0, np.max(dados['demandas']) * 1.2)

        else:  # Burnup
            ax.plot(dados['dias'], dados['demandas'], label='Demandas (Escopo Total)', color=REAL_COLOR_BURNDOWN,
                    linewidth=3)
            ax.plot(dados['dias'], dados['entregas'], label='Entregas (Concluído)', color=PROGRESS_COLOR_BURNUP,
                    linewidth=3, marker='o')
            ax.plot(dados['dias'], dados['planejado'], label='Planejado (Ideal)', color=SUCCESS_COLOR, linestyle='--',
                    linewidth=2)

            ax.set_title(f"GRÁFICO BURNUP: {dados['nome']}", color=TEXT_COLOR, fontsize=16)
            ax.set_ylabel('DEMANDA (Acumulada)', color=TEXT_COLOR)
            ax.set_ylim(0, np.max(dados['demandas']) * 1.2)

        ax.set_xlabel('TEMPO', color=TEXT_COLOR)
        ax.set_xticks(dados['dias'])
        ax.tick_params(axis='x', colors=TEXT_COLOR)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        ax.spines['bottom'].set_color(TEXT_COLOR)
        ax.spines['left'].set_color(TEXT_COLOR)

        ax.legend(loc='upper right', facecolor='white', edgecolor='black')
        plt.tight_layout()

        self.plot_figure(fig)
        self.mostrar_mensagem(f"Gráfico {dados['grafico']} gerado com sucesso!", cor=HIGHLIGHT_COLOR)

    def plot_figure(self, fig):
        if self.canvas_widget:
            self.canvas_widget.destroy()

        if self.placeholder_label:
            self.placeholder_label.destroy()
            self.placeholder_label = None

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)
        canvas.draw()


if __name__ == "__main__":
    app = AppGraficosVisuais()
    app.mainloop()