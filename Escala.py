import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from collections import defaultdict
import datetime
import calendar

class EscalaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escala de Serviço para Igreja")

        self.colaboradores = ['Breno', 'Maria', 'João', 'Ana']  # Exemplo de nomes de colaboradores
        self.dias_indisponiveis = defaultdict(list)

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0)

        self.label = ttk.Label(self.frame, text="Escala de Serviço")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.nome_label = ttk.Label(self.frame, text="Selecione o Colaborador:")
        self.nome_label.grid(row=1, column=0, pady=5, sticky=tk.W)

        self.nome_combobox = ttk.Combobox(self.frame, values=self.colaboradores, width=20, state="readonly")
        self.nome_combobox.grid(row=1, column=1, pady=5, sticky=tk.W)
        self.nome_combobox.bind("<<ComboboxSelected>>", self.atualizar_calendario)

        self.cal_label = ttk.Label(self.frame, text="Selecione as datas de indisponibilidade:")
        self.cal_label.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.calendar = Calendar(self.frame, date_pattern='dd/MM/yyyy', showweeknumbers=False)
        self.calendar.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        self.adicionar_button = ttk.Button(self.frame, text="Adicionar Indisponibilidade", command=self.adicionar_indisponibilidade)
        self.adicionar_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.gerar_button = ttk.Button(self.frame, text="Gerar Escala Mensal", command=self.gerar_escala_mensal)
        self.gerar_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.grid(row=6, column=0, columnspan=3, pady=10)

    def atualizar_calendario(self, event=None):
        # Limpar seleção anterior
        self.calendar.selection_clear()

        # Obter o nome do colaborador selecionado
        nome_selecionado = self.nome_combobox.get()

        # Se houver datas de indisponibilidade para o colaborador, marcar no calendário
        if nome_selecionado in self.dias_indisponiveis:
            for data in self.dias_indisponiveis[nome_selecionado]:
                self.calendar.calevent_create(data.year, data.month, data.day, text=data.day)

    def adicionar_indisponibilidade(self):
        nome = self.nome_combobox.get()
        datas_selecionadas = self.calendar.selection

        if nome and datas_selecionadas:
            for data in datas_selecionadas:
                if data not in self.dias_indisponiveis[nome]:
                    self.dias_indisponiveis[nome].append(data)
            self.atualizar_calendario()
            messagebox.showinfo("Sucesso", f"Dias de indisponibilidade adicionados para {nome}")
        else:
            messagebox.showwarning("Aviso", "Selecione um colaborador e pelo menos um dia de indisponibilidade")

    def gerar_escala_mensal(self):
        if not self.dias_indisponiveis:
            messagebox.showwarning("Aviso", "Adicione pelo menos um colaborador com dias de indisponibilidade!")
            return

        # Calcular os dias de quarta-feira e domingo do mês atual
        now = datetime.datetime.now()
        month_days = calendar.monthrange(now.year, now.month)[1]
        quartas = [datetime.date(now.year, now.month, day) for day in range(1, month_days + 1) if calendar.weekday(now.year, now.month, day) == 2]  # Quarta-feira
        domingos = [datetime.date(now.year, now.month, day) for day in range(1, month_days + 1) if calendar.weekday(now.year, now.month, day) == 6]  # Domingo

        # Selecionar colaboradores disponíveis para a escala
        escala_quarta = self.selecionar_colaboradores_para_dia(quartas, "Quarta-feira")
        escala_domingo = self.selecionar_colaboradores_para_dia(domingos, "Domingo")

        # Exibir a escala gerada
        resultado = "Escala de Serviço Mensal:\n"
        resultado += f"Quarta-feira:\n"
        for dia, colaboradores in escala_quarta.items():
            resultado += f"{dia.strftime('%d/%m/%Y')}: {', '.join(colaboradores)}\n"
        resultado += f"Domingo:\n"
        for dia, colaboradores in escala_domingo.items():
            resultado += f"{dia.strftime('%d/%m/%Y')}: {', '.join(colaboradores)}\n"

        self.result_label.config(text=resultado)

    def selecionar_colaboradores_para_dia(self, dias, nome_dia):
        colaboradores_disponiveis = defaultdict(list)

        for dia in dias:
            for colaborador, datas_indisponiveis in self.dias_indisponiveis.items():
                if dia not in datas_indisponiveis:
                    colaboradores_disponiveis[dia].append(colaborador)

        return colaboradores_disponiveis

def main():
    root = tk.Tk()
    app = EscalaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
