from src.reports.report_generator import Consultas
import os

class Information:
    def main(self):
        consultas = Consultas()
        result = consultas.evolucoes()

        if result:
            print("Evoluções obtidas com sucesso!")
            print(f"Relatórios salvos em: {os.path.join('reports', 'relatorio_diario.md')}")
            print(f"Relatórios salvos em: {os.path.join('reports', 'relatorio_semanal.md')}")
            print(f"Relatórios salvos em: {os.path.join('reports', 'relatorio_mensal.md')}")
            print(f"Relatórios salvos em: {os.path.join('reports', 'relatorio_anual.md')}")
            print(f"Relatório HTML gerado em: {os.path.join('reports', 'bitcoin_price_report.html')}")
        else:
            print("Falha ao obter evoluções.")

if __name__ == "__main__":
    info = Information()
    info.main()