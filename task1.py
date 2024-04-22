import pandas as pd
from typing import List


def load_data_csv(file_path: str) -> pd.DataFrame:
    """
    Загружает данные из CSV файла.

    Args:
    - file_path (str): Путь к CSV файлу.

    Returns:
    - pd.DataFrame: Загруженные данные в формате DataFrame.
    """
    return pd.read_csv(file_path)


def main() -> None:
    """
    Основная функция программы. Загружает данные из CSV файла, анализирует частоту повторений
    и выводит результаты на экран.
    """
    file_path = "table.csv"

    try:
        data_csv = load_data_csv(file_path)

        id_counts = data_csv['id'].value_counts()

        print(f"ID, которые встречаются только 3 раза: {id_counts[id_counts == 3].index.tolist()}")

        print("\nЧастота повторений:")
        counts = id_counts.value_counts().sort_index()
        for count, frequency in counts.items():
            print(f"{frequency} уникальных id встречаются {count} раз(а)")

    except FileNotFoundError:
        print("Файл не найден")


if __name__ == '__main__':
    main()
