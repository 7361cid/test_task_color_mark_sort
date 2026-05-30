import os  # куда вставить tracemallock
import time
import random
import tracemalloc
import gc
from sort_by_color_mark import ColorSort, Item


def test_perfomance():
    """Выполнение сортировки 1000 маркированных элементов"""
    # Пример: накопление в глобальном списке
    marks = ['К', 'З', 'С']
    objects = [Item(marks[random.randint(0, 2)], i) for i in range(1000)]
    result = ColorSort.reorder(objects, 'К<С<З')
    expected_list = []
    for color in ('К', 'С', 'З'):
        expected_list.extend([obj for obj in objects if obj.mark == color])
    assert result == expected_list

def main():
    pid = os.getpid()
    print(f"PID процесса: {pid} (для оценки памяти ps -p {pid} -o pid,rss,vsz)")
    print("Нажмите Enter, чтобы выполнить функцию...")
    input()

    # Запускаем трассировку памяти
    tracemalloc.start()
    # Делаем первый снимок до вызова функции
    snapshot_before = tracemalloc.take_snapshot()

    print("Выполняю функцию...")
    start = time.perf_counter()
    test_perfomance()
    work_time = time.perf_counter() - start
    print(f"Время выполнения: {work_time:.4f} секунд")
    print("Функция выполнена.")
    assert work_time < 1

    # Принудительно собираем мусор, чтобы временные объекты были удалены
    gc.collect()
    # Делаем второй снимок после вызова и сборки мусора
    snapshot_after = tracemalloc.take_snapshot()
    tracemalloc.stop()

    # Сравниваем снимки
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    print("\nТоп-10 изменений в памяти (выделено – освобождено):")
    for stat in top_stats[:10]:
        print(stat)

    print("Нажмите Enter, чтобы завершить программу (пока не нажимайте, чтобы проверить память).")
    input()
    print("Завершение.")

if __name__ == "__main__":
    main()