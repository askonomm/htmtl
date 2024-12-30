from dompa import Dompa


class Htmtl:
    __dom: Dompa
    __attribute_parsers: list
    __expression_modifiers: list

    def __init__(self, template: str, attribute_parsers = None, expression_modifiers = None):
        self.__dom = Dompa(template)
        self.__attribute_parsers = attribute_parsers or []
        self.__expression_modifiers = expression_modifiers or []

