import sys

ALLOWED_MARKS = {'К', 'З', 'С'}


class Item:
    def __init__(self, mark, value):
        self.mark = mark
        self.value = value

    def __repr__(self):
        return f"{self.mark}{self.value}"

    def __eq__(self, other):
        return self.mark == other.mark and self.value == other.value


class ColorSort:
    @staticmethod
    def check_symbol_for_similar_latin(symbol):
        if symbol in ['K', 'C']:  # Символы на латинице похожие на кирилицу
            return ' Проверьте раскладку клавиатуры'
        else:
            return ''

    @classmethod
    def parse_rule(cls, rule_str):
        """
        Разбирает строку правила вида "К<З<С" или "С>З>К".

        Требования:
        - правило должно содержать все три метки (К, З, С) ровно по одному разу
        - разделители только '<' или только '>'
        - возвращает список цветов в порядке следования (для '>' порядок обращается)
        """
        if not rule_str:
            raise ValueError("Правило не может быть пустым")

        if '<' in rule_str and '>' in rule_str:
            raise ValueError("Правило не должно содержать одновременно '<' и '>'")

        if '<' in rule_str:
            colors = rule_str.split('<')
        elif '>' in rule_str:
            colors = rule_str.split('>')
            colors.reverse()
        else:
            raise ValueError("Правило должно содержать разделители '<' или '>'")

        # Удаляем пробелы и пустые элементы
        colors = [c.strip() for c in colors if c.strip()]

        # Должно быть ровно 3 метки
        if len(colors) != 3:
            raise ValueError(f"Правило должно содержать ровно 3 метки (К, З, С), получено: {colors}")

        # Проверка допустимых меток
        for color in colors:
            if color not in ALLOWED_MARKS:
                extra_error_info = cls.check_symbol_for_similar_latin(color)
                raise ValueError(f"Недопустимая метка в правиле: '{color}'{extra_error_info}. Допустимы: К, З, С")

        # Проверка на дубликаты
        if len(set(colors)) != 3:
            raise ValueError(f"Правило содержит повторяющиеся метки: {colors}")

        return colors


    @classmethod
    def reorder(cls, objects, rule):
        """
        Переупорядочивает список объектов согласно правилу.
        Все объекты должны иметь метки только из {К, З, С}.
        """
        order = cls.parse_rule(rule)
        groups = {color: [] for color in order}

        for obj in objects:
            mark = obj.mark
            if mark not in ALLOWED_MARKS:
                extra_error_info = cls.check_symbol_for_similar_latin(mark)
                raise ValueError(f"Недопустимая метка у объекта: '{mark}' {extra_error_info}. Допустимы: К, З, С")
            groups[mark].append(obj)

        result = []
        for color in order:
            result.extend(groups[color])
        return result


# Пример использования
if __name__ == "__main__":
    data = [
        Item('К', 1), Item('С', 2), Item('З', 3),
        Item('З', 4), Item('К', 5), Item('С', [6])
    ]
    rule = "К<З<С"
    print(ColorSort.reorder(data, rule))

    rule2 = "С>З>К"
    print(ColorSort.reorder(data, rule2))

    rule3 = " С <  К  \n < \n  З <"
    print(ColorSort.reorder(data, rule3))


