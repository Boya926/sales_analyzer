from pathlib import Path
import logging
from app.analyzer import SalesAnalyzer
from app.data_loader import load_sales_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
DEFAULT_CSV_PATH = BASE_DIR/"data"/"sales.csv"
REQUIRED_COLUMN = {"product","price","quantity"}

def main():
    csv_file = DEFAULT_CSV_PATH
    sales_data = load_sales_data(csv_file,REQUIRED_COLUMN)
    if not sales_data:
        logger.warning("没有有效销售数据，程序退出")
        return
    
    analyzer = SalesAnalyzer(sales_data)
    total_rev = analyzer.calculate_total_revenue()
    product_revenue = analyzer.get_product_revenue()

    logger.info(f"总销售额：{total_rev}")
    print("\n商品销售额：")
    for name, val in product_revenue.items():
        print(f"{name}: {val}")

    print("\n===== 商品查询功能 =====")
    query_name = input("请输入商品名称：")
    res = analyzer.query_by_product_name(query_name)
    if res is None:
        print(f"商品名称：{query_name.strip()} 无销售记录")
    else:
        print(f"商品名称：{query_name} 销售数量：{res['total_qty']} 销售额：{res['total_revenue']}")


if   __name__=="__main__":
    main()


    

  

