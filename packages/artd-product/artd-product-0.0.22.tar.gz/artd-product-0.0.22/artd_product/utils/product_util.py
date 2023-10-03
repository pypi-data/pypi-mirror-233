from artd_product.models import (
    Category,
)


def get_categories_tree(category_id=None):
    if category_id is None:
        categories = Category.objects.filter(parent=None)
    else:
        categories = Category.objects.filter(id__gte=category_id)
    categories_tree = []
    for category in categories:
        category_tree = {
            "id": category.id,
            "text": category.name,
            "state": {
                "opened": True,
                "selected": False,
            },
            "children": get_children(category),
        }
        categories_tree.append(category_tree)
    return categories_tree


def get_children(category):
    children = Category.objects.filter(parent=category)
    children_tree = []
    for child in children:
        child_tree = {
            "id": child.id,
            "text": child.name,
            "state": {
                "opened": True,
                "selected": False,
            },
            "children": get_children(child),
        }
        children_tree.append(child_tree)
    return children_tree


def get_product_categories_tree(
    category_id=None, product_categories=None, disabled=False
):
    if category_id is None:
        categories = Category.objects.filter(parent=None)
    else:
        categories = Category.objects.filter(id__gte=category_id)
    categories_tree = []
    for category in categories:
        selected = False
        if category.id in product_categories:
            selected = True
        category_tree = {
            "id": category.id,
            "name": category.id,
            "text": category.name,
            "state": {
                "opened": True,
                "selected": selected,
                "disabled": disabled,
            },
            "children": get_product_children(
                category, product_categories, disabled=disabled
            ),
        }
        categories_tree.append(category_tree)
    for category in categories_tree:
        category["state"]["selected"] = True
        break
    return categories_tree


def get_product_children(category, product_categories=None, disabled=False):
    children = Category.objects.filter(parent=category)
    children_tree = []
    selected = False
    for child in children:
        if child.id in product_categories:
            selected = True
        child_tree = {
            "id": child.id,
            "text": child.name,
            "state": {
                "opened": True,
                "selected": selected,
                "disabled": disabled,
            },
            "children": get_product_children(
                child, product_categories, disabled=disabled
            ),
        }
        children_tree.append(child_tree)
    return children_tree
