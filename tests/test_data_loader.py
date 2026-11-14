import pytest
from pathlib import Path
from app.data_loader import load_sales_data

REQUIRED_COLS = {"product","price","quantity"}

def test_file_not_exists():
    # 场景1：文件不存在
    fake_path = Path("data/not_exist.csv")
    result = load_sales_data(fake_path, REQUIRED_COLS)
    assert result == []


def test_empty_csv_file(tmp_path):
    # 场景2：空文件（pytest内置tmp_path，自动生成临时文件，用完自动删掉）
    empty_file = tmp_path/"empty.csv"
    empty_file.write_text("")
    result = load_sales_data(empty_file,REQUIRED_COLS)
    assert result ==[]

def test_csv_missing_required_column(tmp_path):
    # 场景3：缺少必要字段，比如没有price
    bad_csv = tmp_path / "bad_header.csv"
    content = """product,quantity
Apple,5
"""
    bad_csv.write_text(content, encoding="utf-8")
    result = load_sales_data(bad_csv, REQUIRED_COLS)
    assert result == []

def test_price_not_number(tmp_path):
    # 场景4：price不是数字，该行会被跳过，其他合法行保留
    bad_csv = tmp_path / "bad_price.csv"
    content = """product,price,quantity
Apple,abc,5
Banana,6,8
"""
    bad_csv.write_text(content, encoding="utf-8")
    result = load_sales_data(bad_csv, REQUIRED_COLS)
    # Apple行跳过，只剩Banana
    assert len(result) == 1
    assert result[0]["product"] == "Banana"

def test_quantity_not_integer(tmp_path):
    # 场景5：quantity不是整数（文本、小数）
    bad_csv = tmp_path / "bad_qty.csv"
    content = """product,price,quantity
Apple,10,three
Orange,8,4.2
Banana,6,8
"""
    bad_csv.write_text(content, encoding="utf-8")
    result = load_sales_data(bad_csv, REQUIRED_COLS)
    assert len(result) == 1
    assert result[0]["product"] == "Banana"

def test_product_name_empty(tmp_path):
    # 场景6：商品名称为空，该行跳过
    bad_csv = tmp_path / "empty_name.csv"
    content = """product,price,quantity
,10,5
Banana,6,8
"""
    bad_csv.write_text(content, encoding="utf-8")
    result = load_sales_data(bad_csv, REQUIRED_COLS)
    assert len(result) == 1
    assert result[0]["product"] == "Banana"

