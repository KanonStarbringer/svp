# Simulação de Propagação Acústica

Esta aplicação permite simular a propagação de ondas acústicas em um meio com perfil de velocidade variável, utilizando o método de traçado de raios.

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute a aplicação:
```bash
streamlit run app.py
```

2. A aplicação oferece as seguintes funcionalidades:
   - Upload de arquivo CSV ou Excel com perfil de velocidade
   - Editor interativo de perfil de velocidade
   - Download de template para criação de perfis
   - Ajuste da posição da fonte sonora
   - Visualização em tempo real dos gráficos de perfil de velocidade e propagação de raios

## Formato do Arquivo de Perfil

O arquivo de perfil deve conter duas colunas:
- `depth`: profundidade em metros
- `speed`: velocidade do som em m/s

## Exemplo de Uso

1. Baixe o template usando o botão "Baixar template"
2. Preencha o template com seus dados
3. Faça upload do arquivo preenchido
4. Ajuste a posição da fonte conforme necessário
5. Observe os gráficos atualizados em tempo real 
