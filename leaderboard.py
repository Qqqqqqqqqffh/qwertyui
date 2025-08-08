import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate

def init_db():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benchmark_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            generation_time REAL NOT NULL,
            sorting_time REAL NOT NULL,
            total_time REAL NOT NULL,
            correctly_sorted BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_leaderboard():
    print("="*60)
    print("🏆 Starting Code Execution Leaderboard Generation")
    print("="*60)
  
    init_db()
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, 
               generation_time/1000 as generation_time_s,
               sorting_time/1000 as sorting_time_s,
               total_time/1000 as total_time_s,
               correctly_sorted
        FROM benchmark_results
        ORDER BY total_time
    ''')
    sorted_results = [
        {
            'username': row[0],
            'generation_time': row[1]*1000,
            'sorting_time': row[2]*1000,
            'total_time': row[3]*1000,
            'generation_time_s': row[1],
            'sorting_time_s': row[2],
            'total_time_s': row[3],
            'correctly_sorted': row[4]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    
    if not sorted_results:
        print("❌ No results found in database. Creating sample data...")
        sorted_results = [
            {
                "username": "sample_user", 
                "generation_time": 15230, 
                "sorting_time": 25410,
                "total_time": 40640,
                "correctly_sorted": True,
                "total_time_s": 40.64,
                "generation_time_s": 15.23,
                "sorting_time_s": 25.41
            }
        ]

    leaderboard_md = "# 🏆 Code Execution Leaderboard\n\n"
    leaderboard_md += "Rank | Username | Total Time (s) | Generation (s) | Sorting (s) | Correctly Sorted\n"
    leaderboard_md += "-----|----------|----------------|----------------|-------------|-----------------\n"
    
    for i, result in enumerate(sorted_results, 1):
        status_icon = "✅" if result['correctly_sorted'] else "❌"
        leaderboard_md += (
            f"{i} | {result['username']} | {result['total_time_s']:.2f} | "
            f"{result['generation_time_s']:.2f} | {result['sorting_time_s']:.2f} | "
            f"{status_icon}\n"
        )
    
    if sorted_results:
        usernames = [result['username'] for result in sorted_results]
        total_times = [result['total_time_s'] for result in sorted_results]
        
        plt.figure(figsize=(14, 8))
        bars = plt.barh(usernames, total_times, color='skyblue')
        plt.xlabel('Total Time (s)')
        plt.title('Code Execution Leaderboard (Lower is Better)')
        plt.gca().invert_yaxis()
        
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                     f'{width:.2f}s', 
                     ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('leaderboard.png')
        print("\n📊 Generated leaderboard.png visualization")
    
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    
    print("\n" + "="*60)
    print(f"🏁 Leaderboard generation complete! Top performer: {sorted_results[0]['username']}")
    print(f"  - Total time: {sorted_results[0]['total_time_s']:.2f}s")
    print("="*60)

def save_to_db(username, result_data):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO benchmark_results 
        (username, generation_time, sorting_time, total_time, correctly_sorted)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        username,
        result_data['generation_time'],
        result_data['sorting_time'],
        result_data['total_time'],
        result_data['correctly_sorted']
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_leaderboard()
