import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_sales_data(file_path: Path, required_cols: set):
    sales = []
    if not file_path.exists():
        logger.error(f"文件不存在：{file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = set(reader.fieldnames)
            if not required_cols.issubset(header):
                logger.error(f"CSV表头缺失必要字段，需要字段：{required_cols}，实际表头：{header}")
                return []

            for row in reader:
                try:
                    product = row["product"].strip()
                    if not product:
                        logger.warning("跳过该行：商品名称为空，行内容：%s", row)
                        continue
                    price = float(row["price"])
                    quantity = int(row["quantity"])
                    if price < 0 or quantity < 0:
                        logger.warning(f"跳过该行：价格或数量为负数，商品：{product}")
                        continue
                    sales.append({"product": product, "price": price, "quantity": quantity})
                except ValueError:
                    logger.warning("跳过该行：数字转换失败，行内容：%s", row)
    except Exception as e:
        logger.exception("读取CSV文件发生异常")
    return sales
