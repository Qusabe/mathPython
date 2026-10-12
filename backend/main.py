from sympy import Matrix, symbols, N, latex
import pandas as pd
import sympy as sp
import json
from sympy import latex, Matrix
from typing import Callable, Tuple, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd
import numpy as np
from typing import List
import matplotlib.pyplot as plt

from datetime import datetime
import csv
import string
import random
import pypandoc

#Приложение преобразования координатных данных
# Инициализация FastAPI приложения
app = FastAPI(
    title="Excel to Markdown API",
    description="API для преобразования координатных данных в другую систему координат из Excel-файлов и генерации отчетов в формате Markdown",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Корневой маршрут, возвращающий информацию о сервисе"""
    return {
        "message": "Excel to Markdown API работает",
        "endpoints": {
            "/process-excel/": "Загрузка и обработка Excel-файла с генерацией отчета в формате Markdown",
            "/markdown-result": "Получение результата в формате Markdown"
        }
    }

'''
#Генерируем синтетические данные
def generate_csv(file_path, num_rows):
    # Генерация случайного имени
    def random_name(length=5):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    # Генерация случайного числа больше 100000
    def random_number():
        return random.randint(100000000, 999999000)/1000

    # Создание и запись в CSV-файл
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'X', 'Y', 'Z'])  # Заголовки столбцов

        for _ in range(num_rows):
            writer.writerow([random_name(), random_number(), random_number(), random_number()])

# Пример использования функции
generate_csv('example.csv', 10)
 '''
#_____________________________

'''
"""Формирование файла с параметрами перехода"""
import json
import numpy as np


# Задаем параметры перехода в виде словаря
parameters = {
    "СК-42": {
        "ΔX": 23.56,
        "ΔY": -140.86,
        "ΔZ": -79.77,
        "ωx": np.radians(-0.001738 / 3600),
        "ωy": np.radians(-0.346441 / 3600),
        "ωz": np.radians(-0.794263 / 3600),
        "m": -0.22274 * 10**6
    },
    "СК-95": {
        "ΔX": 24.46,
        "ΔY": -130.80,
        "ΔZ": -81.53,
        "ωx": np.radians(-0.001738 / 3600),
        "ωy": np.radians(0.003559 / 3600),
        "ωz": np.radians(-0.134263 / 3600),
        "m": -0.22274 * 10**6
    },
    "ПЗ-90": {
        "ΔX": -1.443,
        "ΔY": 0.142,
        "ΔZ": 0.230,
        "ωx": np.radians(-0.001738 / 3600),
        "ωy": np.radians(0.003559 / 3600),
        "ωz": np.radians(-0.134263 / 3600),
        "m": -0.22274 * 10**6
    },
    "ПЗ-90.02": {
        "ΔX": -0.373,
        "ΔY": 0.172,
        "ΔZ": 0.210,
        "ωx": np.radians(-0.001738 / 3600),
        "ωy": np.radians(0.003559 / 3600),
        "ωz": np.radians(-0.004263 / 3600),
        "m": -0.0074 * 10**6
    },
    "ПЗ-90.11": {
        "ΔX": 0.000,
        "ΔY": -0.014,
        "ΔZ": 0.008,
        "ωx": np.radians(0.0000562 / 3600),
        "ωy": np.radians(0.0000019 / 3600),
        "ωz": np.radians(-0.0000053 / 3600),
        "m": 0.00006 * 10**6
    },
    "WGS-84 (G1150)": {
        "ΔX": -0.013,
        "ΔY": 0.092,
        "ΔZ": 0.030,
        "ωx": np.radians(-0.001738 / 3600) * np.pi / 180,
        "ωy": np.radians(0.003559 / 3600) * np.pi / 180,
        "ωz": np.radians(-0.004263 / 3600) * np.pi / 180,
        "m": -0.0074 * 10**6
    },
    "ITRF-2008": {
        "ΔX": 0.003,
        "ΔY": -0.013,
        "ΔZ": 0.008,
        "ωx": np.radians(0.0000543 / 3600) * np.pi / 180,
        "ωy": np.radians(-0.0000061 / 3600) * np.pi / 180,
        "ωz": np.radians(-0.0000055 / 3600) * np.pi / 180,
        "m": 0.00006 * 10**6
    }
}

# Путь к файлу для сохранения
file_path = 'parameters.json'

# Сохранение данных в JSON файл
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(parameters, f, ensure_ascii=False, indent=4)

print(f"Файл {file_path} успешно создан.")
'''
#______________________________
"""Функция преобразования координат """


def union_eq(*args):
  eq = '$$'
  for i in range(len(args)):
    flag = 1 if len(args[i]) == 1 else 0
    eq += latex(args[i])
    print(latex(args[i]))

    if  (i != (len(args)-1)) and flag != 1 and (len(args[i+1]) != 1):
      eq += "="

  return eq + '$$'




def generate_markdown_report(func: Callable):
    def wrapper(*args, **kwargs):
        original_df = args[0]
        target_system = args[1]
        params_file = args[2]

        # Выполним преобразование координат
        transformed_df, formulas, transformation_params = func(original_df, target_system, params_file)

        # Определение символьных переменных
        X, Y, Z = symbols('X Y Z')
        delta_X, delta_Y, delta_Z = symbols('ΔX ΔY ΔZ')
        omega_x, omega_y, omega_z = symbols('ωx ωy ωz')
        m_sym = symbols('m')

        # Матрицы для общей формулы
        vec_B = Matrix([X, Y, Z]).subs({X: 'X_B', Y: 'Y_B', Z: 'Z_B'})
        vec_A = Matrix([X, Y, Z]).subs({X: 'X_A', Y: 'Y_A', Z: 'Z_A'})
        translation_vec = Matrix([delta_X, delta_Y, delta_Z])
        rotation_matrix = Matrix([
            [1, omega_z, -omega_y],
            [-omega_z, 1, omega_x],
            [omega_y, -omega_x, 1]
        ])

        general_formula_left = vec_B
        general_formula_right = (1 + m_sym) * rotation_matrix * vec_A + translation_vec
        general_formula = union_eq(general_formula_left, general_formula_right)

        # Формула с подставленными параметрами
        X_new, Y_new, Z_new = formulas if formulas else (0, 0, 0)
        specific_formula = (
            f"$$ X_{{r}} = {latex(X_new)}, $$ \n\n"
            f"$$ Y_{{r}} = {latex(Y_new)}, $$ \n\n"
            f"$$ Z_{{r}} = {latex(Z_new)} $$"
        )

        first_point = original_df.iloc[0]
        point_subs = {X: first_point['X'], Y: first_point['Y'], Z: first_point['Z']}

        # Подстановка параметров в формулу
        X_new_with_params = X_new
        Y_new_with_params = Y_new
        Z_new_with_params = Z_new
        # Подстановка координат точки
        X_new_with_coords = X_new_with_params.subs(point_subs)
        Y_new_with_coords = Y_new_with_params.subs(point_subs)
        Z_new_with_coords = Z_new_with_params.subs(point_subs)

        report_content = f"# Отчёт по преобразованию координат\n\n"
        report_content += f"## Параметры ввода\n\n"
        report_content += f"- **Исходная таблица данных**: {original_df.shape[0]} точек\n"
        report_content += f"- **Начальная система координат**: ГСК-2011\n"
        report_content += f"- **Конечная система координат**: {target_system}\n"
        report_content += f"- **Параметры преобразования**:\n"
        report_content += f"  - ΔX: {transformation_params['ΔX']}\n"
        report_content += f"  - ΔY: {transformation_params['ΔY']}\n"
        report_content += f"  - ΔZ: {transformation_params['ΔZ']}\n"
        report_content += f"  - ωx: {transformation_params['ωx']:.10f}\n"
        report_content += f"  - ωy: {transformation_params['ωy']:.10f}\n"
        report_content += f"  - ωz: {transformation_params['ωz']:.10f}\n"
        report_content += f"  - m: {transformation_params['m']:.10f}\n\n"

        # Пункт 1: Общая формула
        report_content += f"## 1: Общая формула преобразования\n\n"
        report_content += f"{general_formula}\n\n"

        # Пункт 2: Формула с подставленными параметрами
        report_content += f"## 2: Общая формула с подставленными параметрами перехода\n\n"
        report_content += f"{specific_formula}\n\n"

        # Пункт 3: Пример последовательных преобразований для первой точки
        report_content += f"## 3: Пример последовательных преобразований для первой точки\n\n"
        report_content += f"Для точки {first_point['Name']} с начальными координатами:\n"
        report_content += f"X = {first_point['X']}\n"
        report_content += f"Y = {first_point['Y']}\n"
        report_content += f"Z = {first_point['Z']}\n\n"
        report_content += f"### Шаг 1: Общая формула\n\n"
        report_content += f"{general_formula}\n\n"
        report_content += f"### Шаг 2: Подстановка параметров перехода\n\n"
        report_content += f"$$ X_{{r}} = {latex(X_new_with_params)} $$\n\n"
        report_content += f"$$ Y_{{r}} = {latex(Y_new_with_params)} $$\n\n"
        report_content += f"$$ Z_{{r}} = {latex(Z_new_with_params)} $$\n\n"
        report_content += f"### Шаг 3: Подстановка начальных координат\n\n"
        report_content += f"$$ X_{{r}} = {latex(X_new_with_coords)} $$\n\n"
        report_content += f"$$ Y_{{r}} = {latex(Y_new_with_coords)} $$\n\n"
        report_content += f"$$ Z_{{r}} = {latex(Z_new_with_coords)} $$\n\n"
        report_content += f"### Шаг 4: Вычисленные конечные координаты\n\n"
        first_transformed = transformed_df.iloc[0]
        report_content += f"$$ X_{{r}} = {first_transformed['X']} $$\n"
        report_content += f"$$ Y_{{r}} = {first_transformed['Y']} $$\n"
        report_content += f"$$ Z_{{r}} = {first_transformed['Z']} $$\n\n"

        # Пункт 4: Таблица и статистика
        report_content += f"## 4: Таблица с координатами до и после преобразования и общая статистика\n\n"
        report_content += f"### Таблица координат до и после преобразования\n\n"
        report_content += "| Name | Начальная X | Начальная Y | Начальная Z | Конечная X | Конечная Y | Конечная Z |\n"
        report_content += "| --- | --- | --- | --- | --- | --- | --- |\n"
        for index, row in original_df.iterrows():
            transformed_row = transformed_df[transformed_df['Name'] == row['Name']].iloc[0]
            report_content += f"| {row['Name']} | {row['X']:.6f} | {row['Y']:.6f} | {row['Z']:.6f} | {transformed_row['X']:.6f} | {transformed_row['Y']:.6f} | {transformed_row['Z']:.6f} |\n"
        report_content += f"\n### Общая статистика\n\n"
        report_content += f"#### Средние значения до преобразования\n\n"
        report_content += f"- X: {original_df['X'].mean():.6f}\n"
        report_content += f"- Y: {original_df['Y'].mean():.6f}\n"
        report_content += f"- Z: {original_df['Z'].mean():.6f}\n\n"
        report_content += f"#### Средние значения после преобразования\n\n"
        report_content += f"- X: {transformed_df['X'].mean():.6f}\n"
        report_content += f"- Y: {transformed_df['Y'].mean():.6f}\n"
        report_content += f"- Z: {transformed_df['Z'].mean():.6f}\n\n"

        return report_content

    return wrapper

@generate_markdown_report
def transform_coordinates(input_data: pd.DataFrame, target_system: str, params_file: str, save_to_file: Optional[str] = None) -> Tuple[pd.DataFrame, Tuple[sp.Expr, sp.Expr, sp.Expr], dict]:
    """
    Returns:
    - Tuple containing (transformed DataFrame, transformation formulas, parameters)
    """
    # Чтение параметров перехода из JSON-файла
    with open(params_file, 'r', encoding='utf-8') as f:
        all_params = json.load(f)

    if target_system not in all_params:
        raise ValueError(f"Параметры перехода для системы '{target_system}' не найдены в файле {params_file}.")

    # Извлечение параметров для целевой системы
    params = all_params[target_system]

    # Извлечение параметров
    required_keys = ['ΔX', 'ΔY', 'ΔZ', 'ωx', 'ωy', 'ωz', 'm']
    for key in required_keys:
        if key not in params:
            raise KeyError(f"В файле {params_file} для системы {target_system} отсутствует параметр '{key}'.")

    dx, dy, dz = params['ΔX'], params['ΔY'], params['ΔZ']
    wx, wy, wz = params['ωx'], params['ωy'], params['ωz']
    m = params['m'] * 1e-6  # Масштабный коэффициент в микрoradiанах

    # Чтение данных
    if isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        df = pd.read_csv(input_data)

    # Проверка наличия необходимых столбцов
    required_columns = ['Name', 'X', 'Y', 'Z']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Входные данные должны содержать столбцы: Name, X, Y, Z")

    # Определение символьных переменных
    ΔX, ΔY, ΔZ, ωx, ωy, ωz, m_sym = symbols('ΔX ΔY ΔZ ωx ωy ωz m')
    X, Y, Z = symbols('X Y Z')

    # Формула преобразования
    formula = (1 + m_sym) * Matrix([[1, ωz, -ωy], [-ωz, 1, ωx], [ωy, -ωx, 1]]) @ Matrix([[X], [Y], [Z]]) + Matrix([[ΔX], [ΔY], [ΔZ]])

    # Подстановка константных параметров
    elements_const = {
        ΔX: dx,
        ΔY: dy,
        ΔZ: dz,
        ωx: wx,
        ωy: wy,
        ωz: wz,
        m_sym: m
    }

    transformed = []

    for _, row in df.iterrows():
        elements = {
            **elements_const,
            X: row['X'],
            Y: row['Y'],
            Z: row['Z']
        }
        results_vector = formula.subs(elements).applyfunc(N)
        transformed.append([
            row['Name'],
            float(results_vector[0]),
            float(results_vector[1]),
            float(results_vector[2])
        ])

    df_result = pd.DataFrame(transformed, columns=['Name', 'X', 'Y', 'Z'])

    if save_to_file:
        df_result.to_csv(save_to_file, index=False)

    # Возвращаем формулу для отчета
    X_new = formula[0].subs(elements_const)
    Y_new = formula[1].subs(elements_const)
    Z_new = formula[2].subs(elements_const)

    return df_result, (X_new, Y_new, Z_new), params

data = pd.DataFrame({
    'Name': [f'Точка{i}' for i in range(1, 10)],
    'X': [289800.551866, 212515.085716, 196718.595874, 212530.882205, 212594.068165, 244108.0654, 180922.106032, 275701.045086, 212214.952409],
    'Y': [162974.043594, 119511.368417, 110627.968456, 119520.251817, 119555.785416, 137278.168338, 101744.568496, 155044.96826, 119342.583817],
    'Z': [102.724491, 105.153865, 103.723702, 106.176772, 104.723702, 107.200385, 105.723702, 108.22405, 106.723702]
})

@app.post("/process-excel/")
async def process_excel(file: UploadFile = File(...)):
    """
    Обрабатывает загруженный Excel-файл и возвращает отчет в формате Markdown
    """
    # Проверка формата файла
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Поддерживаются только файлы Excel (.xlsx, .xls)"
        )

    try:
        # Чтение содержимого файла
        contents = await file.read()
        buffer = BytesIO(contents)

        # Загрузка Excel-файла в DataFrame
        df = pd.read_excel(buffer)

        # Генерация отчета в формате Markdown на основе данных
        report = generate_markdown_report(df)

        # Создание байтового объекта для хранения отчета
        output = BytesIO(report.encode())
        output.seek(0)

        # Возвращаем отчет как скачиваемый файл
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        return StreamingResponse(
            output,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

@app.get("/markdown-results")
async def markdown_results (file: UploadFile = File(...)):
    return {}
'''
# Выполнение преобразования и создание отчёта
report = transform_coordinates(
    data,
    'СК-42',
    'parameters.json'
)

# Сохранение отчёта в файл Markdown
with open('coordinate_transformation_report.md', 'w', encoding='utf-8') as f:
    f.write(report)
print("Отчёт успешно создан: coordinate_transformation_report.md")

#!pandoc coordinate_transformation_report.md -o report.docx
pypandoc.convert_file(
    "coordinate_transformation_report.md",
    "docx",
    outputfile="report.docx",
)
'''