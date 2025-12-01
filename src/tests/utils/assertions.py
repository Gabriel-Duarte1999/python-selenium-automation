"""
Assertions customizadas para os testes.
"""

def assert_all_items_equal(items: list, expected_value: any, message: str = ""):
    """
    Verifica se todos os itens em uma lista são iguais a um valor esperado.
    """
    for item in items:
        assert item == expected_value, message or f"Item '{item}' não é igual a '{expected_value}'"

def assert_list_not_empty(items: list, message: str = ""):
    """
    Verifica se uma lista não está vazia.
    """
    assert len(items) > 0, message or "A lista não deveria estar vazia"

# Adicionar outras assertions customizadas conforme a necessidade
# Ex: assert_url_contains, assert_element_has_class, etc.