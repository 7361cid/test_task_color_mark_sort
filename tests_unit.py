import unittest
import itertools
from sort_by_color_mark import ColorSort, Item


def generate_valid_rules():
    """
    Генерирует все 12 валидных правил:
    - 6 перестановок цветов
    - для каждой перестановки 2 варианта: через '<' (прямой порядок)
      и через '>' (обратный порядок, который после reverse даёт тот же прямой порядок)
    Возвращает список кортежей (rule_str, expected_order)
    пример одного из кортежей ('К<З<С', ['К', 'З', 'С'])
    """
    colors = ['К', 'З', 'С']
    all_permutations = list(itertools.permutations(colors))
    rules = []
    for perm in all_permutations:
        # вариант с '<' - порядок как в перестановке
        rule_less = '<'.join(perm)
        rules.append((rule_less, list(perm)))
        # вариант с '>' - обратный порядок (т.к. A>B>C даёт убывание, после reversed -> возрастание)
        # reversed нужен потому что порядку 'К', 'З', 'С' соответсвует К<З<С и С>З>К
        rule_greater = '>'.join(reversed(perm))
        rules.append((rule_greater, list(perm)))
    return rules


class TestReorderPositive(unittest.TestCase):
    """Позитивные тесты: все валидные правила и корректные последовательности"""

    def setUp(self):
        # Стандартный набор объектов, содержащий все три цвета в хаотичном порядке
        self.objects = [
            Item('К', 1), Item('С', 2), Item('З', 3),
            Item('З', 4), Item('К', 5), Item('С', 6)
        ]

    def test_all_valid_rules(self):
        """TC-UNIT-POS-01: Проверка всех 12 валидных правил (каждое даёт одинаковую сортировку по своему порядку)"""
        for rule_str, expected_order in generate_valid_rules():
            with self.subTest(rule=rule_str):
                result = ColorSort.reorder(self.objects, rule_str)
                # Собираем ожидаемый список объектов: сначала все метки в порядке expected_order
                expected_list = []
                for color in expected_order:
                    expected_list.extend([obj for obj in self.objects if obj.mark == color])
                self.assertEqual(result, expected_list)

    def test_rule_with_spaces_but_valid(self):
        """TC-UNIT-POS-02: Правило с пробелами (валидно, проверяем что не падает)"""
        objects = [Item('К', 1), Item('С', 2), Item('З', 3)]
        result = ColorSort.reorder(objects, " К < З < С ")
        self.assertEqual(result, [Item('К', 1), Item('З', 3), Item('С', 2)])

    def test_empty_sequence(self):
        """TC-UNIT-POS-03: Пустая последовательность"""
        rule = "К<З<С"
        self.assertEqual(ColorSort.reorder([], rule), [])

    def test_missing_some_color(self):
        """TC-UNIT-POS-04: Отсутствует метка 'З' в последовательности"""
        objects = [Item('К', 1), Item('С', 2), Item('К', 3)]
        rule = "К<З<С"
        expected = [Item('К', 1), Item('К', 3), Item('С', 2)]
        self.assertEqual(ColorSort.reorder(objects, rule), expected)

    def test_preserve_order_within_group(self):
        """TC-UNIT-POS-05: Сохранение исходного порядка внутри группы"""
        objects = [Item('К', 2), Item('К', 1), Item('С', 1), Item('К', 3), Item('С', 2)]
        rule = "К<С<З"
        expected = [Item('К', 2), Item('К', 1), Item('К', 3), Item('С', 1), Item('С', 2)]
        self.assertEqual(ColorSort.reorder(objects, rule), expected)

    def test_complex_objects(self):
        """TC-UNIT-POS-06: Объекты с дополнительными полями, и значениями разных типов"""

        class ExtraItem:
            def __init__(self, mark, name, val):
                self.mark = mark
                self.name = name  # допонительное поле
                self.val = val

        obj1 = ExtraItem('К', 'a', 10)
        obj2 = ExtraItem('С', 'b', '20')
        obj3 = ExtraItem('К', 'c', [30])
        objects = [obj1, obj2, obj3]
        rule = "К<З<С"
        result = ColorSort.reorder(objects, rule)
        self.assertEqual(result, [obj1, obj3, obj2])

    def test_string_sort(self):
        """TC-UNIT-POS-07: Сортировка строки"""
        str_data = "КЗКСКЗ"
        rule = "К<С<З"
        expected = "КККСЗЗ"
        self.assertEqual(ColorSort.reorder(str_data, rule), expected)

class TestReorderNegative(unittest.TestCase):
    """Негативные тесты: ошибочные правила и недопустимые объекты"""

    # ----- Ошибки в правиле -----
    def test_empty_rule(self):
        """TC-UNIT-NEG-01: Пустое правило"""
        with self.assertRaisesRegex(ValueError, "не может быть пустым"):
            ColorSort.reorder([], "")

    def test_no_operator(self):
        """TC-UNIT-NEG-02: Отсутствуют разделители '<' или '>'"""
        with self.assertRaisesRegex(ValueError, "должно содержать разделители"):
            ColorSort.reorder([], "КЗС")

    def test_mixed_operators(self):
        """TC-UNIT-NEG-03: Смешанные разделители в правиле"""
        with self.assertRaisesRegex(ValueError, "Правило не должно содержать одновременно '<' и '>'"):
            ColorSort.reorder([], "К<З>С")

    def test_only_two_colors(self):
        """TC-UNIT-NEG-04: Только две метки в правиле"""
        with self.assertRaisesRegex(ValueError, "Правило должно содержать ровно 3 метки"):
            ColorSort.reorder([], "К<З")

    def test_four_colors(self):
        """TC-UNIT-NEG-05: Четыре метки в правиле"""
        with self.assertRaisesRegex(ValueError, "Правило должно содержать ровно 3 метки"):
            ColorSort.reorder([], "К<З<С<К")

    def test_duplicate_color(self):
        """TC-UNIT-NEG-06: Повторяющаяся метка в правиле"""
        with self.assertRaisesRegex(ValueError, "Правило содержит повторяющиеся метки"):
            ColorSort.reorder([], "К<З<К")

    def test_invalid_color_in_rule(self):
        """TC-UNIT-NEG-07: Недопустимый символ в правиле (не К,З,С)"""
        with self.assertRaisesRegex(ValueError, "Недопустимая метка в правиле: 'Х'"):
            ColorSort.reorder([], "К<З<Х")

    def test_invalid_color_in_rule_latin(self):
        """TC-UNIT-NEG-08: Недопустимый латинский символ в правиле схожий с валидным"""
        with self.assertRaisesRegex(ValueError, "Недопустимая метка в правиле: 'C' Проверьте раскладку клавиатуры."):
            ColorSort.reorder([], "К<З<C")

    # ----- Ошибки в объектах -----
    def test_invalid_mark_in_object(self):
        """TC-UNIT-NEG-09: Объект с недопустимой меткой 'Х'"""
        objects = [Item('К', 1), Item('Х', 2), Item('С', 3)]
        with self.assertRaisesRegex(ValueError, "Недопустимая метка у объекта: 'Х'"):
            ColorSort.reorder(objects, "К<З<С")

    def test_multiple_invalid_marks(self):
        """TC-UNIT-NEG-10: Несколько объектов с недопустимыми метками"""
        objects = [Item('P', 1), Item('Q', 2)]
        with self.assertRaisesRegex(ValueError, "Недопустимая метка у объекта: 'P'"):
            ColorSort.reorder(objects, "К<З<С")

    def test_object_without_mark_attribute(self):
        """TC-UNIT-NEG-11: Объект не имеет атрибута .mark"""

        class BadItem:
            pass

        obj = BadItem()
        with self.assertRaises(ValueError):
            ColorSort.reorder([obj], "К<З<С")


if __name__ == "__main__":
    unittest.main()
