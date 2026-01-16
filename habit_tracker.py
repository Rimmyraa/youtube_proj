import json
from datetime import date

FILE_NAME = "habits.json"

def load_habits():
    """Load habits from JSON file"""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_habits(habits):
    """Save habits to JSON file"""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(habits, file, indent=2)


# -------------------------
# Core Features
# -------------------------

def add_habit(habits):
    """Add a new habit"""
    name = input("Habit name: ").strip()

    if name in habits:
        print("Habit already exists.")
        return

    habits[name] = []
    save_habits(habits)
    print("Habit added successfully.")


def mark_habit(habits):
    """Mark habit as completed today"""
    name = input("Habit name: ").strip()

    if name not in habits:
        print("Habit not found.")
        return

    today = str(date.today())

    if today in habits[name]:
        print("Already marked for today.")
    else:
        habits[name].append(today)
        save_habits(habits)
        print("Habit marked as completed.")


def show_stats(habits):
    """Display statistics"""
    print("\nHabit Statistics")
    print("-" * 20)

    for habit, days in habits.items():
        print(f"{habit}: {len(days)} days completed")


def show_menu():
    print("""
1. Add habit
2. Mark habit as completed
3. Show statistics
4. Exit
""")


def main():
    habits = load_habits()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_habit(habits)
        elif choice == "2":
            mark_habit(habits)
        elif choice == "3":
            show_stats(habits)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
