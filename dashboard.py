import dash
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

# Carregar os dados
students_df = pd.read_csv('Students_Info.csv')
courses_df = pd.read_csv('Courses_Info.csv')

# Aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div(style={'backgroundColor': '#002D62', 'padding': '20px'}, children=[
    html.H1("Dashboard de Desempenho de Estudantes", style={'color': 'white', 'textAlign': 'center'}),

    # Quadro de informações com dropdown
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '10px'}, children=[
        html.Div([
            html.Label("Selecione o Curso:", style={'color': 'white'}),
            dcc.Dropdown(
                id='course-dropdown',
                options=[{'label': i, 'value': i} for i in courses_df['curso'].unique()],
                value=courses_df['curso'].unique()[0],
                style={'width': '200px'}
            )
        ], style={'padding': '10px'}),
        html.Div(f"Total de Alunos: {students_df['nome'].nunique()}", style={
            'color': 'white', 'padding': '20px', 'borderRadius': '15px', 'backgroundColor': '#007BFF', 'boxShadow': '2px 2px 10px #000'}),
        html.Div(f"Total de Cursos: {courses_df['curso'].nunique()}", style={
            'color': 'white', 'padding': '20px', 'borderRadius': '15px', 'backgroundColor': '#007BFF', 'boxShadow': '2px 2px 10px #000'}),
    ]),

    # Gráficos interativos para top 10 alunos e tendência
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}, children=[
        html.Div([
            dcc.Graph(id='activities-bar-chart')
        ], style={'width': '48%'}),
        html.Div([
            dcc.Graph(id='trend-line-chart')
        ], style={'width': '48%'}),
    ]),

    # Gráficos interativos para top 10 notas e top 10 atividades
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}, children=[
        html.Div([
            dcc.Graph(id='top-notas-chart')
        ], style={'width': '48%'}),
        html.Div([
            dcc.Graph(id='approval-rate-chart')
        ], style={'width': '48%'}),
    ]),

    # Gráfico para média de notas
    html.Div([
        dcc.Graph(id='compare-mean-chart')
    ])
])

# Callbacks para interatividade
@app.callback(
    Output('activities-bar-chart', 'figure'),
    Input('course-dropdown', 'value'))
def update_bar_chart(selected_course):
    filtered_df = courses_df[courses_df['curso'] == selected_course].merge(students_df, left_on='id_aluno', right_on='id')
    top_students = filtered_df.groupby('nome')['atividades_completas'].sum().nlargest(10).reset_index()
    return px.bar(top_students, x='nome', y='atividades_completas', title=f"Top 10 Alunos em {selected_course} - Atividades Completas", template='plotly_dark')

@app.callback(
    Output('top-notas-chart', 'figure'),
    Input('course-dropdown', 'value'))
def update_top_notas_chart(selected_course):
    filtered_df = courses_df[courses_df['curso'] == selected_course].merge(students_df, left_on='id_aluno', right_on='id')
    top_students = filtered_df.groupby('nome')['nota_teste'].max().nlargest(10).reset_index()
    return px.bar(top_students, x='nome', y='nota_teste', title=f"Top 10 Alunos em {selected_course} - Melhores Notas", template='plotly_dark')

@app.callback(
    Output('trend-line-chart', 'figure'),
    Input('course-dropdown', 'value'))
def update_line_chart(selected_course):
    filtered_df = courses_df[courses_df['curso'] == selected_course]
    line_data = filtered_df.groupby('id_aluno')['nota_teste'].mean().reset_index()
    return px.line(line_data, x='id_aluno', y='nota_teste', title=f'Tendência de Notas para {selected_course}', template='plotly_dark')

@app.callback(
    Output('approval-rate-chart', 'figure'),
    Input('course-dropdown', 'value'))
def update_approval_chart(selected_course):
    filtered_df = courses_df[courses_df['curso'] == selected_course]
    approvals = filtered_df[filtered_df['nota_teste'] >= 70].shape[0]
    failures = filtered_df[filtered_df['nota_teste'] < 70].shape[0]
    data = {
        'Category': ['Aprovações', 'Reprovações'],
        'Count': [approvals, failures]
    }
    df_plot = pd.DataFrame(data)
    return px.pie(df_plot, names='Category', values='Count', title=f"Taxa de Aprovação e Reprovação para {selected_course}", template='plotly_dark')

@app.callback(
    Output('compare-mean-chart', 'figure'),
    [Input('course-dropdown', 'value')])
def update_mean_chart(selected_course):
    # This now shows data for all courses
    mean_scores = courses_df.groupby('curso')['nota_teste'].mean().reset_index()
    return px.bar(mean_scores, x='curso', y='nota_teste', title="Média de Notas por Curso", template='plotly_dark')

if __name__ == '__main__':
    app.run_server(debug=True)
