import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def load_data():
    """Загружаем данные из JSON-файлов"""
    data = []
    for filename in os.listdir('results'):
        if filename.endswith('.json'):
            with open(os.path.join('results', filename)) as f:
                data.append(json.load(f))
    return data

def generate_leaderboard(data):
    """Генерируем leaderboard"""
    if not data:
        print("Нет данных для генерации leaderboard")
        return
    
    # Сортируем по времени сортировки
    sorted_data = sorted(data, key=lambda x: x['sorting_time'])
    
    # Подготавливаем данные для графика
    names = [d['username'] for d in sorted_data]
    times = [d['sorting_time'] for d in sorted_data]
    
    # Создаем график
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, times)
    plt.ylabel('Время сортировки (мс)')
    plt.title('Сравнение времени сортировки')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('leaderboard.png')
    print("График сохранен как leaderboard.png")

if __name__ == "__main__":
    if not os.path.exists('results'):
        os.makedirs('results')
    
    data = load_data()
    if data:
        generate_leaderboard(data)
    else:
        print("Нет данных для обработки")
        # Создаем демо-данные для теста
        demo_data = [{
            'username': 'test_user',
            'sorting_time': 100,
            'total_time': 150
        }]
        generate_leaderboard(demo_data)
