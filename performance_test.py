import os  # куда вставить tracemallock
import time
import random
import tracemalloc
import gc
from sort_by_color_mark import ColorSort, Item


def test_perfomance(print_time_stat=False):
    def _func():
        """Выполнение сортировки 1000 маркированных элементов"""
        # Пример: накопление в глобальном списке
        marks = ['К', 'З', 'С']
        objects = [Item(marks[random.randint(0, 2)], i) for i in range(1000)]
        result = ColorSort.reorder(objects, 'К<С<З')
        expected_list = []
        for color in ('К', 'С', 'З'):
            expected_list.extend([obj for obj in objects if obj.mark == color])
        assert result == expected_list

    start = time.perf_counter()
    _func()
    work_time = time.perf_counter() - start
    if print_time_stat:
        print(f"Время выполнения: {work_time:.4f} секунд")
        print("Функция выполнена.")
    assert work_time < 1

def main():
    pid = os.getpid()
    print(f"PID процесса: {pid} (для оценки памяти ps -p {pid} -o pid,rss,vsz)")
    test_perfomance(True)

    # Принудительно собираем мусор, чтобы временные объекты были удалены
    gc.collect()
    print("Нажмите Enter, чтобы выполнить функцию повторно 10 раз и сравнить статистику использования памяти...")
    input()
    tracemalloc.start()  # Запускаем трассировку памяти
    snap_prev = tracemalloc.take_snapshot()  # Делаем первый снимок до повторного вызова функции

    for i in range(10):
        test_perfomance()
        gc.collect()
        snap_curr = tracemalloc.take_snapshot()
        diff = snap_curr.compare_to(snap_prev, 'lineno')
        print(f"--- После итерации {i + 1} ---")
        for stat in diff[:5]:
            print(stat)
        snap_prev = snap_curr

    print("Нажмите Enter, чтобы завершить программу (пока не нажимайте, чтобы проверить память).")
    input()
    print("Завершение.")

if __name__ == "__main__":
    main()