
import json
import matplotlib
matplotlib.use('Agg')  # Важно для работы без GUI
import matplotlib.pyplot as plt
import os
import numpy as np

def load_data():
    """Загружаем данные из JSON-файлов"""
    data = []
    for filename in os.listdir('results'):
        if filename.endswith('.json'):
            path = os.path.join('results', filename)
            try:
                with open(path) as f:
                    file_data = json.load(f)
                    file_data['filename'] = filename
                    data.append(file_data)
            except json.JSONDecodeError:
                print(f"Ошибка чтения JSON в файле: {filename}")
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {str(e)}")
    return data

def generate_leaderboard(data):
    """Генерируем leaderboard и сохраняем графики"""
    if not data:
        print("Нет данных для генерации leaderboard")
        return
    
    # Сортируем по времени сортировки (чем быстрее - тем лучше)
    sorted_data = sorted(data, key=lambda x: x.get('sorting_time', float('inf')))
    
    # Подготавливаем данные для графика
    names = [entry['filename'].replace('.json', '') for entry in sorted_data]
    times = [entry.get('sorting_time', 0) for entry in sorted_data]
    total_times = [entry.get('total_time', 0) for entry in sorted_data]
    
    # Создаем график
    plt.figure(figsize=(12, 8))
    
    # График времени сортировки
    plt.subplot(2, 1, 1)
    bars = plt.bar(names, times, color='skyblue')
    plt.ylabel('Время сортировки (мс)')
    plt.title('Сравнение времени сортировки алгоритмов')
    plt.xticks(rotation=45, ha='right')
    
    # Добавляем значения на столбцах
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}', 
                 ha='center', va='bottom', rotation=0, fontsize=8)
    
    # График общего времени
    plt.subplot(2, 1, 2)
    bars_total = plt.bar(names, total_times, color='lightgreen')
    plt.ylabel('Общее время (мс)')
    plt.title('Сравнение общего времени выполнения')
    plt.xticks(rotation=45, ha='right')
    
    # Добавляем значения на столбцах
    for bar in bars_total:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}', 
                 ha='center', va='bottom', rotation=0, fontsize=8)
    
    # Настраиваем расположение и сохраняем
    plt.tight_layout()
    plt.savefig('leaderboard.png')
    print("Leaderboard сгенерирован и сохранен как leaderboard.png")
    
    # Создаем текстовый рейтинг без использования tabulate
    with open('leaderboard.txt', 'w') as f:
        f.write("Рейтинг алгоритмов сортировки\n")
        f.write("=" * 50 + "\n")
        f.write(f"{'Место':<6} {'Алгоритм':<20} {'Время сортировки (мс)':<20} {'Общее время (мс)':<15}\n")
        f.write("-" * 50 + "\n")
        
        for i, entry in enumerate(sorted_data, 1):
            name = entry['filename'].replace('.json', '')[:20]  # Ограничение длины имени
            sort_time = entry.get('sorting_time', 0)
            total_time = entry.get('total_time', 0)
            f.write(f"{i:<6} {name:<20} {sort_time:<20.2f} {total_time:<15.2f}\n")
        
        f.write("\nПримечание: Сортировка по времени сортировки (от быстрех к медленным)\n")
    
    print("Текстовый рейтинг сохранен как leaderboard.txt")

if __name__ == "__main__":
    # Проверяем существование папки с результатами
    if not os.path.exists('results'):
        print("Ошибка: Папка 'results' не найдена")
        exit(1)
    
    # Загружаем данные и генерируем leaderboard
    data = load_data()
    if data:
        generate_leaderboard(data)
    else:
        print("Нет данных для обработки")
