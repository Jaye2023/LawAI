import tkinter as tk
from tkinter import ttk

class ROICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("电商ROI与推广盈亏计算器 - 增强版")
        self.create_widgets()

    def create_widgets(self):
        # 输入参数区域
        input_frame = ttk.LabelFrame(self.root, text="输入参数")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        labels = [
            ("销售价格（元）", "sales_price"),
            ("产品成本（元）", "product_cost"),
            ("平台服务费扣点（%）", "platform_fee"),
            ("平均运费（元）", "shipping_cost"),
            ("赠品成本（元）", "gift_cost"),
            ("退款率（%）", "refund_rate"),
            ("其他成本（元）", "other_cost"),
            ("销量（件）", "sales_volume"),  # 新增销量字段
            ("实际花费（元）", "ad_cost")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(labels):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            self.entries[key] = entry

        # 计算按钮
        ttk.Button(self.root, text="计算ROI和盈亏", command=self.calculate).grid(row=1, column=0, pady=10)

        # 结果显示区域
        result_frame = ttk.LabelFrame(self.root, text="计算结果")
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # 修复后的结果标签配置
        result_labels = [
            ("保本ROI", "保本ROI"),
            ("利润率", "利润率"),
            ("实际ROI", "实际ROI"),
            ("推广盈亏", "推广盈亏")
        ]
        
        self.results = {
            "保本ROI": tk.StringVar(),
            "利润率": tk.StringVar(),
            "实际ROI": tk.StringVar(),
            "推广盈亏": tk.StringVar()
        }

        for i, (label_key, display_text) in enumerate(result_labels):
            ttk.Label(result_frame, text=display_text+":").grid(row=i, column=0, padx=5, pady=2, sticky="e")
            ttk.Label(result_frame, textvariable=self.results[label_key]).grid(row=i, column=1, padx=5, pady=2, sticky="w")

    def get_float(self, key, default=0.0):
        try:
            return float(self.entries[key].get())
        except ValueError:
            return default

    def calculate(self):
        # 获取输入值
        sales_price = self.get_float("sales_price")
        product_cost = self.get_float("product_cost")
        platform_fee = self.get_float("platform_fee") / 100  # 转换为小数
        shipping_cost = self.get_float("shipping_cost")
        gift_cost = self.get_float("gift_cost")
        refund_rate = self.get_float("refund_rate") / 100    # 转换为小数
        other_cost = self.get_float("other_cost")
        sales_volume = self.get_float("sales_volume", default=1.0)  # 获取销量
        ad_cost = self.get_float("ad_cost")

        # 核心计算逻辑
        total_cost = (product_cost + shipping_cost + gift_cost + other_cost +
                     sales_price * platform_fee + sales_price * refund_rate)
        
        net_profit = sales_price - total_cost
        profit_margin = (net_profit / sales_price * 100) if sales_price != 0 else 0
        
        # 修正保本ROI公式
        breakeven_roi = total_cost / (net_profit * (1 - refund_rate)) if (net_profit != 0 and refund_rate < 1) else 0
        actual_roi = (net_profit * sales_volume) / ad_cost if ad_cost != 0 else 0
        profit_loss = net_profit * sales_volume - ad_cost

        # 显示结果
        self.results["保本ROI"].set(f"{abs(breakeven_roi):.2f}" if breakeven_roi != 0 else "N/A")
        self.results["利润率"].set(f"{profit_margin:.2f}%")
        self.results["实际ROI"].set(f"{actual_roi:.2f}" if ad_cost != 0 else "需输入推广费用")
        self.results["推广盈亏"].set(f"{profit_loss:.2f}元（{'盈利' if profit_loss >=0 else '亏损'}）")

if __name__ == "__main__":
    root = tk.Tk()
    app = ROICalculator(root)
    root.mainloop()
