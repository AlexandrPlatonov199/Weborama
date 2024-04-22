"""Описание логики выполнения задачи.
1.Получение пути к файлу: Программа должна принимать входной файл как аргумент командной строки.
 Это обеспечит возможность обработки различных файлов без изменения кода.
2.Определение формата файла: Программа должна определить формат файла по его расширению.
 Это позволит выбрать соответствующий парсер для обработки файла.
3.Парсинг метаданных: Для каждого формата файла (epub и fb2) необходимо написать функцию,
 которая будет извлекать метаданные из файла. В epub-файлах метаданные обычно хранятся в специальных полях,
 в то время как в fb2-файлах метаданные оформляются в виде XML-элементов.
4.Вывод результатов: После извлечения метаданных необходимо вывести их в удобном формате, например,
 в кортежа (название, автор, издательство, год).
5.Обработка ошибок: Программа должна обрабатывать возможные ошибки, такие как отсутствие файла,
 неподдерживаемый формат или отсутствие метаданных.
"""


import os
import sys
from ebooklib import epub
import xml.etree.ElementTree as ET
from typing import Tuple, Optional


def get_book_metadata(
        book: epub,
        namespace: str,
        element: str,
) -> Optional[str]:
    """
    Получает метаданные книги.

    Parameters:
    - book (epub): Объект книги.
    - namespace (str): Пространство имен метаданных.
    - element (str): Элемент метаданных.

    Returns:
    - str or None: Значение запрошенного элемента метаданных
     или None, если элемент не найден.
    """

    return book.get_metadata(namespace, element)[0][0] \
        if book.get_metadata(namespace, element) else None


def parse_epub(
        file_path: str,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Извлекает метаданные из EPUB-файла.

    Parameters:
    - file_path (str): Путь к EPUB-файлу.

    Returns:
    - tuple: Кортеж с метаданными (название, автор, издательство, год)
    или None для отсутствующих значений.
    """
    book = epub.read_epub(file_path)

    title = get_book_metadata(book, 'DC', 'title')
    author = get_book_metadata(book, 'DC', 'creator')
    publisher = get_book_metadata(book, 'DC', 'publisher')
    year = get_book_metadata(book, 'DC', 'date')

    return title, author, publisher, year


def parse_fb2(
        file_path: str,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Извлекает метаданные из FB2-файла.

    Parameters:
    - file_path (str): Путь к FB2-файлу.

    Returns:
    - tuple: Кортеж с метаданными (название, автор, издательство, год) или None для отсутствующих значений.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    title = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title').text
    author_first_name = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name').text
    author_last_name = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name').text
    author = f"{author_first_name} {author_last_name}" if author_first_name and author_last_name else None
    publisher = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}publisher').text
    year = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}year').text

    return title, author, publisher, year


def main() -> None:
    """
    Основная функция программы. Анализирует переданный файл и выводит его метаданные.
    """
    try:
        file_path = sys.argv[1]

        file_name, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == '.epub':
            title, author, publisher, year = parse_epub(file_path)
        elif file_extension.lower() == '.fb2':
            title, author, publisher, year = parse_fb2(file_path)
        else:
            print("Unsupported file format")
            return

        print("Title:", title)
        print("Author:", author)
        print("Publisher:", publisher)
        print("Year:", year)
    except FileNotFoundError:
        print("No such file or directory")


if __name__ == "__main__":
    main()
