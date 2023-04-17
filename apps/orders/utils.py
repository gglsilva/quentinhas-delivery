def arrange_order(products_list):
    return [item for item in products_list if item != 'on']

def format_product_list(products_list):
    return ''.join(
        f'{item}, ' if item != products_list[-1] else f'{item} '
        for item in products_list
    )