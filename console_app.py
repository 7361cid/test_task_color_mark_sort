import sys
from sort_by_color_mark import ColorSort, Item


def parse_user_input(sequence_str):
    """Превращает строку в список Item, value = позиция."""
    items = []
    for idx, ch in enumerate(sequence_str):
        if ch not in ('К', 'З', 'С'):
            extra_error_msg = ColorSort.check_symbol_for_similar_latin(ch)
            raise ValueError(f"Недопустимый символ '{ch}'{extra_error_msg}. Допустимы: К, З, С")
        items.append(Item(ch, idx))
    return items



def format_output_with_indices(items):
    return ', '.join(f"{item.mark}({item.value})" for item in items)


def format_original_with_indices(sequence_str):
    chars = list(sequence_str)
    parts = [f"{i}:{ch}" for i, ch in enumerate(chars)]
    return ", ".join(parts)


def input_rule():
    """Запрашивает правило, пока не будет введено корректное."""
    while True:
        print("\nВведите правило (например, К<З<С или С>З>К):")
        rule = input().strip()
        if not rule:
            print("Ошибка: правило не может быть пустым. Попробуйте снова.")
            continue
        try:
            ColorSort.parse_rule(rule)  # проверяем синтаксис и допустимость
            return rule
        except ValueError as e:
            print(f"Ошибка в правиле: {e}. Попробуйте снова.")


def input_sequence():
    """Запрашивает последовательность, пока не будет введена корректная."""
    while True:
        print("\nВведите последовательность объектов (только К, З, С, например: КСЗЗКСК):")
        seq_str = input().strip()
        if not seq_str:
            print("Ошибка: последовательность не может быть пустой. Попробуйте снова.")
            continue
        try:
            parse_user_input(seq_str)  # проверяем символы
            return seq_str
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")


def main():
    print("=== Сортировка объектов по правилу (с сохранением порядка внутри групп) ===")

    while True:
        try:
            rule = input_rule()
            seq_str = input_sequence()
            print("\nИсходная последовательность (индекс:метка):")
            print(format_original_with_indices(seq_str))

            objects = parse_user_input(seq_str)
            sorted_objects = ColorSort.reorder(objects, rule)

            print("\nРезультат сортировки (метка(исходный индекс)):")
            print(format_output_with_indices(sorted_objects))

            result_str = ''.join(obj.mark for obj in sorted_objects)
            print(f"\nКратко (только метки): {result_str}")

            print("\nПорядок внутри каждой группы сохраняется – видно по возрастанию индексов.")
            # Спросить, продолжать ли
            print("\nХотите выполнить ещё одну сортировку? (y/n):")
            again = input().strip().lower()
            if again not in ('y', 'yes', 'да', 'д'):
                print("До свидания!")
                break
        except Exception as e:
            print(f"\nНеожиданная ошибка: {e}. Возможно, проблема в логике программы.")
        except KeyboardInterrupt:
            print("Программа прервана пользователем")
            sys.exit(0)



if __name__ == "__main__":
    main()