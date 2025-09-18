import pandas as pd
from src.db.repository import Repository
import os
import json
from datetime import datetime

class Consultas:
    def __init__(self):
        self.media_diaria = "vw_media_diaria"
        self.media_semanal = "vw_media_semanal"
        self.media_mensal = "vw_media_mensal"
        self.media_anual = "vw_media_anual"
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)

    def generate_report(self, df, period, filename):
        """Gera um relatório em Markdown com estatísticas e dicas de investimento."""
        stats = df['average_price'].describe()
        trend = "crescente" if df['average_price'].iloc[-1] > df['average_price'].iloc[0] else "decrescente"
        volatility = stats['std'] / stats['mean'] * 100  # Volatilidade em %

        investment_tip = ""
        if trend == "crescente" and volatility < 10:
            investment_tip = "Tendência de alta com baixa volatilidade. Considere comprar se o preço atual estiver próximo à média."
        elif trend == "crescente" and volatility >= 10:
            investment_tip = "Tendência de alta, mas alta volatilidade. Monitore o mercado antes de investir."
        elif trend == "decrescente" and volatility < 10:
            investment_tip = "Tendência de baixa com baixa volatilidade. Pode ser uma oportunidade de compra na baixa."
        else:
            investment_tip = "Tendência de baixa com alta volatilidade. Cautela, aguarde maior estabilidade."

        report = f"""
# Relatório de Preços do Bitcoin - {period}

## Estatísticas
- **Média**: ${stats['mean']:.2f}
- **Mínimo**: ${stats['min']:.2f}
- **Máximo**: ${stats['max']:.2f}
- **Desvio Padrão**: ${stats['std']:.2f}
- **Volatilidade**: {volatility:.2f}%

## Tendência
- A tendência dos preços no período é **{trend}**.

## Dica de Investimento
{investment_tip}

## Dados
{df.head().to_markdown(index=False)}
"""
        with open(os.path.join(self.report_dir, filename), 'w', encoding='utf-8') as f:
            f.write(report)
        return report

    def generate_html_report(self, chart_data):
        """Gera uma página HTML com gráficos Chart.js para cada período."""
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Preços do Bitcoin</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chart-container { margin: 20px 0; }
        canvas { max-width: 800px; }
    </style>
</head>
<body>
    <h1>Relatório de Preços do Bitcoin</h1>
    <div class="chart-container">
        <h2>Evolução Diária</h2>
        <canvas id="dailyChart"></canvas>
    </div>
    <div class="chart-container">
        <h2>Evolução Semanal</h2>
        <canvas id="weeklyChart"></canvas>
    </div>
    <div class="chart-container">
        <h2>Evolução Mensal</h2>
        <canvas id="monthlyChart"></canvas>
    </div>
    <div class="chart-container">
        <h2>Evolução Anual</h2>
        <canvas id="yearlyChart"></canvas>
    </div>

    <script>
        const chartData = """ + json.dumps(chart_data, indent=2) + """;

        new Chart(document.getElementById('dailyChart'), {
            type: 'line',
            data: {
                labels: chartData.diaria.labels,
                datasets: [{
                    label: 'Preço Médio Diário (USD)',
                    data: chartData.diaria.data,
                    borderColor: '#4B0082',
                    backgroundColor: 'rgba(75, 0, 130, 0.2)',
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Data' } },
                    y: { title: { display: true, text: 'Preço Médio (USD)' } }
                }
            }
        });

        new Chart(document.getElementById('weeklyChart'), {
            type: 'line',
            data: {
                labels: chartData.semanal.labels,
                datasets: [{
                    label: 'Preço Médio Semanal (USD)',
                    data: chartData.semanal.data,
                    borderColor: '#008000',
                    backgroundColor: 'rgba(0, 128, 0, 0.2)',
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Semana' } },
                    y: { title: { display: true, text: 'Preço Médio (USD)' } }
                }
            }
        });

        new Chart(document.getElementById('monthlyChart'), {
            type: 'line',
            data: {
                labels: chartData.mensal.labels,
                datasets: [{
                    label: 'Preço Médio Mensal (USD)',
                    data: chartData.mensal.data,
                    borderColor: '#FF4500',
                    backgroundColor: 'rgba(255, 69, 0, 0.2)',
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Mês' } },
                    y: { title: { display: true, text: 'Preço Médio (USD)' } }
                }
            }
        });

        new Chart(document.getElementById('yearlyChart'), {
            type: 'line',
            data: {
                labels: chartData.anual.labels,
                datasets: [{
                    label: 'Preço Médio Anual (USD)',
                    data: chartData.anual.data,
                    borderColor: '#1E90FF',
                    backgroundColor: 'rgba(30, 144, 255, 0.2)',
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Ano' } },
                    y: { title: { display: true, text: 'Preço Médio (USD)' } }
                }
            }
        });
    </script>
</body>
</html>
"""
        output_path = os.path.join(self.report_dir, "bitcoin_price_report.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Relatório HTML gerado em: {output_path}")

    def evolucoes(self):
        repo = Repository()
        try:
            print("\n📊 Evolução diária:")
            df_diaria = repo.get_view(self.media_diaria)
            print(df_diaria.head())

            print("\n📊 Média semanal:")
            df_semanal = repo.get_view(self.media_semanal)
            print(df_semanal.head())

            print("\n📊 Média mensal:")
            df_mensal = repo.get_view(self.media_mensal)
            print(df_mensal.head())

            print("\n📊 Média anual:")
            df_anual = repo.get_view(self.media_anual)
            print(df_anual.head())

            self.generate_report(df_diaria, "Diário", "relatorio_diario.md")
            self.generate_report(df_semanal, "Semanal", "relatorio_semanal.md")
            self.generate_report(df_mensal, "Mensal", "relatorio_mensal.md")
            self.generate_report(df_anual, "Anual", "relatorio_anual.md")

            chart_data = {
                "diaria": {
                    "labels": df_diaria['day_start'].dt.strftime('%Y-%m-%d').tolist(),
                    "data": df_diaria['average_price'].tolist()
                },
                "semanal": {
                    "labels": df_semanal['week_start'].dt.strftime('%Y-%m-%d').tolist(),
                    "data": df_semanal['average_price'].tolist()
                },
                "mensal": {
                    "labels": df_mensal['month_start'].dt.strftime('%Y-%m').tolist(),
                    "data": df_mensal['average_price'].tolist()
                },
                "anual": {
                    "labels": df_anual['year_start'].dt.strftime('%Y').tolist(),
                    "data": df_anual['average_price'].tolist()
                }
            }

            self.generate_html_report(chart_data)

            return {
                "dataframes": {
                    "diaria": df_diaria,
                    "semanal": df_semanal,
                    "mensal": df_mensal,
                    "anual": df_anual
                },
                "chart_data": chart_data
            }
        except Exception as e:
            print(f"Erro ao obter evoluções: {type(e).__name__}: {str(e)}")
            return None