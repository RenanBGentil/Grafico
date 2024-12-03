from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/grafico', methods=['POST'])
def grafico():
    try:
        # Pegando os valores dos 4 trimestres
        trimestre1 = float(request.form['trimestre1'])
        trimestre2 = float(request.form['trimestre2'])
        trimestre3 = float(request.form['trimestre3'])
        trimestre4 = float(request.form['trimestre4'])

        # Definindo os rótulos e valores
        rotulos = [
            '1º Trimestre', '2º Trimestre', '3º Trimestre', '4º Trimestre'
        ]
        valores = [trimestre1, trimestre2, trimestre3, trimestre4]

        # Gerando o gráfico
        fig, ax = plt.subplots(figsize=(
            12, 6
        ), dpi=150)  # Aumentando a resolução (dpi) para uma imagem mais nítida

        # Estilo do gráfico (cores mais profissionais e sombras nas barras)
        colors = ['#4CAF50', '#2196F3', '#FF9800',
                  '#9C27B0']  # Cores vibrantes, mas sofisticadas
        bars = ax.bar(rotulos,
                      valores,
                      color=colors,
                      edgecolor='black',
                      linewidth=1.2)

        # Títulos e rótulos com fontes mais refinadas
        ax.set_title('Balanço Anual da Empresa',
                     fontsize=20,
                     fontweight='bold',
                     color='#333',
                     fontname='Arial')
        ax.set_xlabel('Trimestres', fontsize=14, fontname='Arial')
        ax.set_ylabel('Valor em R$', fontsize=14, fontname='Arial')

        # Melhora da legibilidade: Ajuste do tamanho da fonte nos eixos
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Adicionando os valores nas barras, ajustando a posição para ficar acima das barras
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'R${height:,.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0,
                        8),  # Ajuste para posicionar o texto acima das barras
                textcoords='offset points',
                ha='center',
                va='bottom',
                fontsize=12,
                color='black',
                fontname='Arial')

        # Adicionando linha de grade mais sutil
        ax.grid(True, axis='y', linestyle='--', alpha=0.6)

        # Adicionando uma borda e sombra nas barras para uma aparência mais profissional
        for bar in bars:
            bar.set_zorder(3)
            bar.set_edgecolor('gray')  # Cor da borda das barras
            bar.set_linewidth(1.5)

        # Remover a borda superior e direita
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Ajustar margens para dar mais espaço ao gráfico
        plt.tight_layout()

        # Convertendo o gráfico para imagem base64
        img = io.BytesIO()
        fig.savefig(
            img, format='png',
            bbox_inches='tight')  # Salvar a imagem com bordas ajustadas
        img.seek(0)
        img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return render_template('grafico.html', img_b64=img_b64)

    except ValueError:
        return "Por favor, insira valores numéricos válidos para os trimestres.", 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
