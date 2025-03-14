import pytest
from rest_framework.exceptions import ValidationError
from store.products.models import Product
from store.orders.enums import OrderStatusEnums
from store.orders.exceptions import InsufficientStockException
from store.orders.utils.order_processing import (
    fetch_products,
    validate_and_prepare_order_items,
    create_order,
    process_order,
)


@pytest.fixture
def sample_products(db):
    """Create sample products for testing."""
    return [
        Product.objects.create(id=1, name="Product A", price=100, stock=10),
        Product.objects.create(id=2, name="Product B", price=200, stock=5),
        Product.objects.create(
            id=3, name="Product C", price=50, stock=0
        ),  # Out of stock
    ]


@pytest.fixture
def valid_cart():
    """Return a valid cart with existing products and sufficient stock."""
    return [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
    ]


@pytest.fixture
def out_of_stock_cart():
    """Return a cart containing an out-of-stock product."""
    return [
        {"product_id": 3, "quantity": 1},  # Product C is out of stock
    ]


@pytest.fixture
def invalid_cart():
    """Return a cart with a non-existent product."""
    return [
        {"product_id": 999, "quantity": 1},  # Product does not exist
    ]


@pytest.mark.django_db
def test_fetch_products(sample_products):
    """Should return a dictionary of products by ID."""
    product_ids = [1, 2]
    products = fetch_products(product_ids)
    assert isinstance(products, dict)
    assert len(products) == 2
    assert str(1) in products and str(2) in products


@pytest.mark.django_db
def test_fetch_products_with_empty_list():
    """Should return an empty dictionary when no product IDs are given."""
    assert fetch_products([]) == {}


@pytest.mark.django_db
def test_fetch_products_with_non_existent_ids():
    """Should return an empty dictionary when product IDs don't exist."""
    assert fetch_products([999]) == {}


@pytest.mark.django_db
def test_validate_and_prepare_order_items_valid(sample_products, valid_cart):
    """Should return order items and calculate the correct total price."""
    products = fetch_products([1, 2])
    order_items, total_price = validate_and_prepare_order_items(products, valid_cart)

    assert len(order_items) == 2
    assert total_price == (100 * 2 + 200 * 1)  # (Product A * 2) + (Product B * 1)


@pytest.mark.django_db
def test_validate_and_prepare_order_items_product_not_found(
    sample_products, invalid_cart
):
    """Should raise ValidationError when a product is not found."""
    products = fetch_products([1, 2])
    with pytest.raises(ValidationError):
        validate_and_prepare_order_items(products, invalid_cart)


@pytest.mark.django_db
def test_validate_and_prepare_order_items_insufficient_stock(
    sample_products, out_of_stock_cart
):
    """Should raise InsufficientStockException when stock is insufficient."""
    products = fetch_products([1, 2, 3])
    with pytest.raises(InsufficientStockException):
        validate_and_prepare_order_items(products, out_of_stock_cart)


# ✅ TEST create_order
@pytest.mark.django_db
def test_create_order(sample_products, valid_cart):
    """Should create an order and associate order items correctly."""
    products = fetch_products([1, 2])
    order_items, total_price = validate_and_prepare_order_items(products, valid_cart)

    order = create_order(order_items, total_price)
    assert order.total_price == 400
    assert order.status == OrderStatusEnums.COMPLETED.value


# ✅ TEST process_order
@pytest.mark.django_db
def test_process_order_success(sample_products, valid_cart):
    """Should process the order successfully and update stock."""
    initial_stock = {p.id: p.stock for p in Product.objects.all()}

    order = process_order(valid_cart)

    assert order.status == OrderStatusEnums.COMPLETED.value
