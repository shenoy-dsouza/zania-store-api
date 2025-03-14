from django.db import transaction
from rest_framework.exceptions import ValidationError
from store.products.models import Product
from store.orders.models import Order, OrderItem
from store.orders.enums import OrderStatusEnums
from store.orders.exceptions import InsufficientStockException
from typing import Dict, List, Tuple


def fetch_products(product_ids: List[int]) -> Dict[int, Product]:
    """
    Retrieve products in bulk and return a dictionary with product_id as keys.
    """
    return Product.objects.in_bulk(product_ids)


def validate_and_prepare_order_items(
    products: Dict[str, Product], cart_items: List[Dict[str, int]]
) -> Tuple[List[OrderItem], float]:
    """
    Validates stock availability and prepares OrderItem instances.

    Args:
        products (dict): Dictionary of product_id -> Product instance.
        cart_items (list): List of dictionaries containing 'product_id'
        and 'quantity'.

    Returns:
        tuple: (order_items, total_price)
    """
    try:
        order_items = []
        total_price = 0
        for item in cart_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)
            product = products.get(str(product_id))
            if not product:
                raise ValidationError(
                    {"product_id": f"Product with ID {product_id} not found."}
                )

            if product.stock < quantity:
                raise InsufficientStockException()

            # Deduct stock
            product.stock -= quantity
            total_price += product.price * quantity

            order_items.append(OrderItem(product=product, quantity=quantity))
        return order_items, total_price
    except Exception:
        raise


def create_order(order_items: List[OrderItem], total_price: float) -> Order:
    """Creates an order and associates order items."""
    order = Order.objects.create(
        total_price=total_price, status=OrderStatusEnums.PENDING.value
    )

    for item in order_items:
        item.order = order

    OrderItem.objects.bulk_create(order_items)

    order.mark_completed()
    return order


def process_order(cart_items: List[Dict[str, int]]) -> Order:
    """
    Processes an order by validating stock, deducting inventory, and creating
    order records.

    Args:
        cart_items (list): List of dictionaries containing 'product_id' and
        'quantity'.

    Returns:
        Order: The created Order instance.
    """
    product_ids = [item["product_id"] for item in cart_items]

    with transaction.atomic():
        products = fetch_products(product_ids)
        order_items, total_price = validate_and_prepare_order_items(
            products, cart_items
        )

        # Bulk update stock in DB
        Product.objects.bulk_update(products.values(), ["stock"])

        # Create order and save items
        return create_order(order_items, total_price)
