import logging

class SalesAnalyzer:
    def __init__(self, sales):
        # self.sales：实例属性，保存传入的销售数据
        self.sales = sales

    def calculate_total_revenue(self):
        """计算总销售额"""
        total = 0
        for item in self.sales:
            revenue = item["price"] * item["quantity"]
            total += revenue
        return total

    def calculate_total_quantity(self):
        """计算总销售数量"""
        total_qty = 0
        for item in self.sales:
            total_qty += item["quantity"]
        return total_qty

    def get_product_revenue(self):
        """统计每个商品的销售额，返回字典 {商品名:销售额}"""
        product_map = {}
        for item in self.sales:
            name = item["product"]
            rev = item["price"] * item["quantity"]
            if name in product_map:
                product_map[name] += rev
            else:
                product_map[name] = rev
        return product_map

    def get_top_products(self, top_n=3):
        """获取销售额前N的商品，默认前3"""
        product_rev = self.get_product_revenue()
      
               # 按销售额从高到低排序
        sorted_list = sorted(product_rev.items(), key=lambda x: x[1], reverse=True)
        return sorted_list[:top_n]
    
    
    def query_by_product_name(self, clean_name):
        if not clean_name or not clean_name.strip():
            raise ValueError("商品名称不能为空或全空格")
        
    # 2. 清理空格（防止用户输入 " Apple " 查不到）
        clean_name = clean_name.strip()
    # 1. 先检查这个商品在不在你的销售额字典里（加括号）

        
        if clean_name not in self.get_product_revenue():
            return None # 或者打印提示 "查无此商品"

    # 2. 不能从 get_product_revenue 里拿数量，必须遍历原始数据去算
        total_qty = 0
        total_revenue = 0.0
    
    # 遍历你初始化时传入的原始销售数据
        for item in self.sales: 
        # 假设 item 是一个字典，包含 "product", "price", "quantity"
            if item["product"] == clean_name: # 匹配商品名
                total_qty += item["quantity"]  # 累加数量
                total_revenue += item["price"] * item["quantity"] # 累加销售额

    # 3. 组装结果返回
        info = {
            "total_qty": total_qty,
            "total_revenue": total_revenue
        }
        return info


# ========== 测试代码 ==========
if __name__ == "__main__":
    sales = [
        {"product": "Apple", "price": 10, "quantity": 5},
        {"product": "Banana", "price": 6, "quantity": 8},
        {"product": "Apple", "price": 10, "quantity": 3},
        {"product": "Orange", "price": 8, "quantity": 4},
    ]
    # 创建实例（对象），把数据传给它
    analyzer = SalesAnalyzer(sales)

    print("销售数据分析结果 ----------------")
    print(f"总销售额：{analyzer.calculate_total_revenue()}")
    print(f"总销售数量：{analyzer.calculate_total_quantity()}")

    product_revenue = analyzer.get_product_revenue()
    print("\n商品销售额：")
    for name, val in product_revenue.items():
        print(f"{name}: {val}")

    top3 = analyzer.get_top_products(3)
    print("\n销售额排名：")
    for idx, (name, val) in enumerate(top3, start=1):
        print(f"{idx}. {name}")
