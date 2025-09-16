from src.reports.report_generator import Consultas

class Information:

    def main(self):
        consultas = Consultas()
        result = consultas.evolucoes()

        if result:
            print("Evoluções obtidas com sucesso!")
            # Você pode usar os DataFrames retornados, por exemplo:
            # print(result["mensal"].describe())

if __name__ == "__main__":
    info = Information()
    info.main()