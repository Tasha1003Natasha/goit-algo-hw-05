import sys

def parse_log_line(line: str) -> dict:
    # Функція для парсингу рядків логу
    lineData = {}

    try:
        line = line.strip()
        if not line:
            raise ValueError("Empty line")

        el = line.split(" ", 3)
        if len(el) < 4:
            raise ValueError("Incomplete line")

        lineData = {
            "date": el[0],
            "time": el[1],
            "level": el[2],
            "message": el[3]
        }

    except ValueError as e:
        print(f"Not enough data: ({e}): {line}")

    return lineData


def load_logs(file_path: str) -> list:
# Функція, яка читає і повертає з файлу інформацію про логи.
    try:
        with open(file_path, "r") as fh:
            lines = [el.strip() for el in fh.readlines() if el.strip()]
          
            logsInfo = []
        
            for line in lines:
                try:
                   parse_line = parse_log_line(line)
                   logsInfo.append(parse_line)
                  
                except ValueError:
                    print(f"{line} некоректні дані!")
                    continue

            return logsInfo
               

    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        return []
    except Exception as e:
        print(f"Помилка при читанні або обробці файлу: {e}")
        return []



def filter_logs_by_level(logs: list, level: str  = None) -> list:
    # Функція, яка фільтрує за рівнем логування.
    if not level:
        return logs
      
    spec_level = list(filter(lambda x: x.get("level").lower() == level.lower(), logs))
    return spec_level



def count_logs_by_level(logs: list) -> dict:
    #Функція, яка підраховує записи за рівнем логування
    try:
        count_by_level = {}

        for i in range(len(logs)):
            level = logs[i].get('level')

            if level in count_by_level:
                count_by_level[level] += 1
            else:
                count_by_level[level] = 1

        return count_by_level

    except Exception as e:
        print(f"Помилка: {e}")
        return {}



def display_log_counts(counts: dict) -> str:
    #Форматує та повертає результати підрахунку логів у читабельній формі.
    if not counts:
        return "Немає даних для відображення."
    
    COLOR_ERROR = "\033[95m"  
    COLOR_RESET = "\033[0m"  

    lines = []
    lines.append(f"{'Рівень логування':<20} | Кількість")
    lines.append(f"{'-'*20}-|----------")


    for level, count in counts.items():
        line = f"{level:<20} | {count}"

        if level.upper() == "ERROR":
            line = f"{COLOR_ERROR}{line}{COLOR_RESET}"

        lines.append(line)


    result = "\n".join(lines)
    return result



def main():
    if len(sys.argv) < 2:
        print("Вкажіть шлях до директорії (наприклад: python task3.py чи python task3.py info)")
        return

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)

    if level:
        filtered = filter_logs_by_level(logs, level)

        counts = count_logs_by_level(logs)
        print(display_log_counts(counts))
        print(f"Деталі логів для рівня : {level.upper()}")

        for log in filtered:
            print(f"{log['date']} {log['time']} [{log['level']}] {log['message']}")

        return 

    counts = count_logs_by_level(logs)
    print(display_log_counts(counts))


if __name__ == "__main__":
    main()
