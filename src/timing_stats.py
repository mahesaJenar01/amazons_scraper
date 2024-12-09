class TimingStats:
    def __init__(self):
        self.brand_time = 0
        self.product_time = 0
        self.rating_time = 0
        self.review_time = 0
        self.sales_info_time = 0
        self.price_time = 0
        self.sustainability_time = 0
        self.total_items = 0
        
    def get_averages(self):
        if self.total_items == 0:
            return {
                "brand": 0, "product": 0, "rating": 0,
                "review": 0, "sales_info": 0, "price": 0, 
                "sustainability": 0
            }
        return {
            "brand": self.brand_time / self.total_items,
            "product": self.product_time / self.total_items,
            "rating": self.rating_time / self.total_items,
            "review": self.review_time / self.total_items,
            "sales_info": self.sales_info_time / self.total_items,
            "price": self.price_time / self.total_items, 
            "sustainability": self.sustainability_time / self.total_items
        }