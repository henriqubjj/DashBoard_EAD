import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

# Definindo os parâmetros
num_students = 500
num_courses = 5
courses = ['Matemática', 'Literatura', 'Biologia', 'História', 'Informática']

# Gerar dados dos alunos
student_data = {
    'id': np.arange(1, num_students + 1),
    'nome': [fake.unique.name() for _ in range(num_students)],  # Usando fake.unique para garantir nomes únicos
    'idade': np.random.randint(15, 19, num_students),
    'sexo': np.random.choice(['Masculino', 'Feminino'], num_students),
    'data_login': pd.to_datetime(np.random.choice(pd.date_range(start='2023-01-01', periods=30), num_students)),
    'hora_login': pd.to_datetime(np.random.randint(360, 1080, num_students) * 60, unit='s').strftime('%H:%M:%S'),
    'data_logout': pd.to_datetime(np.random.choice(pd.date_range(start='2023-01-01', periods=30), num_students)),
    'hora_logout': pd.to_datetime(np.random.randint(360, 1080, num_students) * 60, unit='s').strftime('%H:%M:%S'),
    'participacao_forum': np.random.randint(0, 50, num_students)
}

students_df = pd.DataFrame(student_data)

# Gerar dados dos cursos para cada aluno
course_data = []
for student_id in student_data['id']:
    for course in courses:
        course_data.append({
            'id_aluno': student_id,
            'curso': course,
            'nota_teste': np.random.randint(10, 101),
            'atividades_completas': np.random.randint(0, 101),
            'tempo_atividade': np.random.randint(60, 300)  # tempo em minutos
        })

courses_df = pd.DataFrame(course_data)

# Salvando os dados em CSV
students_csv_path = 'Students_Info.csv'
courses_csv_path = 'Courses_Info.csv'

students_df.to_csv(students_csv_path, index=False)
courses_df.to_csv(courses_csv_path, index=False)

students_csv_path, courses_csv_path
