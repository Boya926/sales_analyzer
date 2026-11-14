import pytest
from app.analyzer import SalesAnalyzer


def test_calculate_total_revenue_normal_data():
    sales = [
        {"product": "Apple", "price": 10, "quantity": 5},
        {"product": "Banana", "price": 6, "quantity": 8},
    ]
    analyzer = SalesAnalyzer(sales)
    total = analyzer.calculate_total_revenue()
    # 10*5 +6*8 = 50 +48 =98
    assert total == 98,"正常数据总销售额计算错误"

def test_calculate_total_revenue_empty_data():
    # 空数据边界
    sales = []
    analyzer = SalesAnalyzer(sales)
    total = analyzer.calculate_total_revenue()
    assert total == 0, "空数据总销售额应该是0"

def test_calculate_total_quantity_normal():
    sales = [
        {"product": "Apple", "price":10, "quantity":5},
        {"product": "Apple", "price":10, "quantity":3},
    ]
    analyzer = SalesAnalyzer(sales)
    qty = analyzer.calculate_total_quantity()
    assert qty == 8, "总数量计算错误"


def test_product_revenue_duplicate_product():
    # 重复商品，合并销售额
    sales = [
        {"product": "Apple", "price":10, "quantity":5},
        {"product": "Apple", "price":10, "quantity":3},
    ]
    analyzer = SalesAnalyzer(sales)
    product_rev = analyzer.get_product_revenue()
    assert product_rev["Apple"] == 80, "相同商品销售额没有累加"
    assert len(product_rev) == 1

def test_top3_only_one_product():
    # 只有一种商品
    sales = [{"product": "Orange", "price":8, "quantity":4}]
    analyzer = SalesAnalyzer(sales)
    top3 = analyzer.get_top_products()
    assert len(top3) == 1
    assert top3[0][0] == "Orange"
    assert top3[0][1] == 32

def test_top3_multi_product():
    # 多种商品，取前3
    sales = [
        {"product": "Apple", "price":10, "quantity":5},
        {"product": "Banana", "price":6, "quantity":8},
        {"product": "Orange", "price":8, "quantity":4},
        {"product": "Grape", "price":20, "quantity":2},
    ]
    analyzer = SalesAnalyzer(sales)
    top3 = analyzer.get_top_products()
    # 计算：Apple50, Banana48, Orange32, Grape40
    # 排序：Apple(50) > Banana(48) > Grape(40)
    assert top3[0][0] == "Apple"
    assert top3[1][0] == "Banana"
    assert top3[2][0] == "Grape"

test_data = [
    {"product": "Apple", "price": 10, "quantity": 5},
    {"product": "Apple", "price": 10, "quantity": 3},
    {"product": "Banana", "price": 6, "quantity": 8},
]

def test_query_exist_product():
    sa = SalesAnalyzer(test_data)
    ret = sa.query_by_product_name("Apple")
    assert ret["total_qty"] == 8
    assert ret["total_revenue"] == 80

def test_query_not_exist_product():
    sa = SalesAnalyzer(test_data)
    ret = sa.query_by_product_name("Orange")
    assert ret is None

def test_query_empty_name():
    sa = SalesAnalyzer(test_data)
    with pytest.raises(ValueError, match="商品名称不能为空或全空格"):
        sa.query_by_product_name("   ")

def test_query_empty_dataset():
    sa = SalesAnalyzer([])
    ret = sa.query_by_product_name("Apple")
    assert ret is None

