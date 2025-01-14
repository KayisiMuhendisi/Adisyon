import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod


class Product(ABC):
    """Ürün Sınıfı (Soyut)"""
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    @abstractmethod
    def update_stock(self, new_stock):
        """Stok bilgisini günceller.""" 
        pass

    @abstractmethod
    def reduce_stock(self):
        """Stoktan bir ürün çıkarır."""
        pass

class FoodProduct(Product):
    """Yemek Ürünü Sınıfı"""
    def __init__(self, name, price, stock):
        super()._init_(name, price, stock)

    def update_stock(self, new_stock):
        """Yemek ürününün stok bilgisini günceller."""
        self.stock = new_stock

    def reduce_stock(self):
        """Yemek ürününden bir adet çıkarır."""
        if self.stock > 0:
            self.stock -= 1
            return True
        return False

class DrinkProduct(Product):
    """İçecek Ürünü Sınıfı"""
    def __init__(self, name, price, stock):
        super()._init_(name, price, stock)

    def update_stock(self, new_stock):
        """İçecek ürününün stok bilgisini günceller."""
        self.stock = new_stock

    def reduce_stock(self):
        """İçecek ürününden bir adet çıkarır."""
        if self.stock > 0:
            self.stock -= 1
            return True
        return False

class StockManager:
    def __init__(self):
        # Ürün kategorilerini ve ürün bilgilerini dinamik bir şekilde oluştur
        self.product_categories = {
            "Kahvaltı": [],
            "İçecekler": [],
            "Ana Yemekler": []
        }

    def add_product(self, category, product_name, product_price, stock):
        """Yeni stok ekler."""
        # Stokta var mı kontrol et, eğer yoksa yeni ürün ekle
        if category in self.product_categories:
            product = {"product_name": product_name, "price": product_price, "stock": stock}
            self.product_categories[category].append(product)
        else:
            print(f"{category} kategorisi bulunamadı!")

    def list_products(self, category):
        """Belirtilen kategorideki tüm ürünleri listeler."""
        if category in self.product_categories:
            return self.product_categories[category]
        else:
            return []

    def update_product_stock(self, product_name, new_stock):
        """Ürünün stok bilgisini günceller."""
        for category, products in self.product_categories.items():
            for product in products:
                if product['product_name'] == product_name:
                    product['stock'] = new_stock
                    return
        print(f"{product_name} ürünü bulunamadı!")

class Table:
    """Temel Masa Sınıfı"""
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, product, price):
        self.orders.append((product, price))

    def remove_order(self, product):
        for i, (p, pr) in enumerate(self.orders):
            if p == product:
                self.orders.pop(i)
                break

    def calculate_total(self):
        return sum(price for _, price in self.orders)

    def apply_discount(self, discount_factor):
        self.orders = [(product, round(price * discount_factor, 2)) for product, price in self.orders]


class VIPTable(Table):
    """VIP Masa Sınıfı"""
    def __init__(self, name, service_fee=50):
        super().__init__(name)
        self.service_fee = service_fee

    def calculate_total(self):
        """Toplam tutara servis ücreti eklenir."""
        total = super().calculate_total()
        return total + self.service_fee



class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Adisyon Hesabı")
        self.root.geometry("1000x600")

        self.tables = {f"Masa {i}": Table(f"Masa {i}") for i in range(1, 6)}
        self.vip_tables = {f"VIP Masa {i}": VIPTable(f"VIP Masa {i}") for i in range(1, 4)}
        self.daily_cash_total = 0
        self.daily_card_total = 0
        self.current_table = None
        self.is_vip = False

        self.stock_manager = StockManager()
        

        # Ürünleri ve stokları başlat
        self.initialize_products()

        self.create_widgets()

    def initialize_products(self):
        """Başlangıç ürünleri ve stoklarını ekler."""
        self.stock_manager.add_product("Kahvaltı", "Tost", 80, 50)
        self.stock_manager.add_product("Kahvaltı", "Yumurta", 30, 50)
        self.stock_manager.add_product("Kahvaltı", "Pancakes", 50, 50)
        self.stock_manager.add_product("Kahvaltı", "Serpme Kahvaltı", 250, 50)
        self.stock_manager.add_product("Kahvaltı", "Tabakta Kahvaltı", 180, 50)

        self.stock_manager.add_product("İçecekler", "Espresso", 55, 50)
        self.stock_manager.add_product("İçecekler", "Cappuccino", 75, 50)
        self.stock_manager.add_product("İçecekler", "Latte", 80, 50)
        self.stock_manager.add_product("İçecekler", "Çay", 25, 50)
        self.stock_manager.add_product("İçecekler", "Kola", 50, 50)

        self.stock_manager.add_product("Ana Yemekler", "Pizza", 150, 50)
        self.stock_manager.add_product("Ana Yemekler", "Burger", 110, 50)
        self.stock_manager.add_product("Ana Yemekler", "Makarna", 125, 50)
        self.stock_manager.add_product("Ana Yemekler", "Tavuk Sote", 180, 50)
        self.stock_manager.add_product("Ana Yemekler", "Et Sote", 220, 50)

    @staticmethod
    def calculate_total_amount(cash_total, card_total):
     """Nakit ve kredi kartı toplamını hesaplayan statik metod."""
     return cash_total + card_total    
    
    def open_category_stock(self, category_name):
        """Belirli bir kategorinin ürünlerini ve stok bilgilerini gösterir."""
        stock_window = tk.Toplevel(self.root)
        stock_window.title(f"{category_name} Stok Yönetimi")
        stock_window.geometry("600x400")

        # Ürünleri alır
        products = self.stock_manager.list_products(category_name)

        if not products:
            messagebox.showwarning("Uyarı", f"{category_name} kategorisinde ürün bulunmamaktadır.")
            stock_window.destroy()
            return

        # Başlıkları yerleştirir
        tk.Label(stock_window, text="Ürün Adı", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(stock_window, text="Mevcut Stok", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(stock_window, text="Yeni Stok Miktarı", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, pady=10)

        row = 1
        entries = {}

        # Ürünleri ve stokları ekrana yazdırır
        for product in products:
            tk.Label(stock_window, text=product["product_name"], font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(stock_window, text=product["stock"], font=("Arial", 12)).grid(row=row, column=1, padx=10, pady=5)

            # Yeni stok girişi
            entry = tk.Entry(stock_window, width=10, font=("Arial", 12))
            entry.grid(row=row, column=2, padx=10, pady=5)
            entries[product["product_name"]] = entry

            row += 1

        def update_stock():
            """Girilen stok değerlerini günceller."""
            for product_name, entry in entries.items():
                new_stock = entry.get()
                if new_stock.isdigit():
                    self.stock_manager.update_product_stock(product_name, int(new_stock))

            messagebox.showinfo("Başarılı", f"{category_name} stokları güncellendi!")
            stock_window.destroy()  # Pencereyi kapat

        tk.Button(stock_window, text="Stokları Güncelle", command=update_stock, bg="#90ee90", font=("Arial", 12)).grid(row=row, column=0, columnspan=3, pady=20)



    
    def create_widgets(self):
        # Sol Panel: Masalar ve VIP Masalar
        self.table_frame = tk.Frame(self.root, bg="#f0f0f0", width=200)
        self.table_frame.pack(side=tk.LEFT, fill=tk.Y)

        table_label = tk.Label(self.table_frame, text="Masalar", font=("Arial", 16, "bold"), bg="#f0f0f0")
        table_label.pack(pady=10)

        self.table_buttons = {}
        for table_name in self.tables:
            button = tk.Button(self.table_frame, text=table_name, width=15, height=2, bg="green", fg="black",
                            command=lambda t=table_name: self.open_table(t, vip=False))
            button.pack(pady=5)
            self.table_buttons[table_name] = button

        vip_label = tk.Label(self.table_frame, text="VIP Masalar", font=("Arial", 16, "bold"), bg="#f0f0f0")
        vip_label.pack(pady=10)

        for vip_table_name in self.vip_tables:
            button = tk.Button(self.table_frame, text=vip_table_name, width=15, height=2, bg="green", fg="black",
                            command=lambda t=vip_table_name: self.open_table(t, vip=True))
            button.pack(pady=5)
            self.table_buttons[vip_table_name] = button

        # Stok Güncelleme Butonları
        stock_update_label = tk.Label(self.table_frame, text="Stok Güncelleme", font=("Arial", 16, "bold"), bg="#f0f0f0")
        stock_update_label.pack(pady=10)

        stock_buttons = ["Kahvaltı", "İçecekler", "Ana Yemekler"]
        for stock_button in stock_buttons:
            button = tk.Button(self.table_frame, text=stock_button, width=15, height=2, bg="#ffd700", fg="black",
                            command=lambda s=stock_button: self.open_category_stock(s))
            button.pack(pady=5)

        # Günlük Rapor Butonu
        report_button = tk.Button(self.table_frame, text="Günlük Rapor", width=15, height=2,
                                command=self.show_daily_report, bg="#87cefa")
        report_button.pack(pady=10)

        # Sağ Panel: Sipariş Yönetimi
        self.order_frame = tk.Frame(self.root, bg="#fafafa")
        self.order_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.table_indicator_label = tk.Label(self.order_frame, text="Masa Seçilmedi", font=("Arial", 16, "bold"),
                                            bg="#fafafa")
        self.table_indicator_label.pack(pady=10)

        self.selection_display = tk.Listbox(self.order_frame, font=("Arial", 12), bg="#fff",width=30,height=10)
        self.selection_display.pack(pady=10)

        self.button_frame = tk.Frame(self.order_frame, bg="#fafafa")
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Ürün Sil", width=12, height=2, bg="#ff9999",
                command=self.remove_item).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.button_frame, text="Kaydet", width=12, height=2, bg="#90ee90",
                command=self.save_order).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.button_frame, text="Masa Kapat", width=12, height=2, bg="#ff6347",
                command=self.close_table).grid(row=0, column=2, padx=5, pady=5)

        # Kategori Seçim Butonları (Sipariş için)
        tk.Label(self.order_frame, text="Kategoriler", font=("Arial", 14, "bold"), bg="#fafafa").pack(pady=10)

        self.category_frame = tk.Frame(self.order_frame, bg="#fafafa")
        self.category_frame.pack()

        column = 0  # İlk sütun
        for category in self.stock_manager.product_categories:
            tk.Button(self.category_frame, text=category, width=20, height=2,
                    command=lambda c=category: self.select_category(c)).grid(row=0, column=column, padx=5, pady=5)
            column += 1  # Sonraki kategori için sütunu bir artır
        # Ürün Butonları Çerçevesi
        self.product_buttons_frame = tk.Frame(self.order_frame, bg="#fafafa")
        self.product_buttons_frame.pack(pady=10)



    def select_category(self, category_name):
        for widget in self.product_buttons_frame.winfo_children():
            widget.destroy()

        # Burada ürünleri 'self.stock_manager.products' üzerinden alır
        if category_name in self.stock_manager.product_categories:
            products = self.stock_manager.list_products(category_name)
            for product in products:
                tk.Button(self.product_buttons_frame, 
                          text=f"{product['product_name']} ({product['price']} TL) - Stok: {product['stock']}", 
                          width=30, 
                          command=lambda p=product['product_name'], pr=product['price']: self.add_product(p, pr)).pack(pady=5)

    def check_stock(self, product_name):
        """Belirtilen ürünün stok durumunu kontrol eder."""
        for category, items in self.product_categories.items():
                for item in items:
                    if item[0] == product_name:
                        return item[2]  # Stok miktarını döndür
                return 0

    def reduce_stock(self, product_name):
        """Sipariş verildiğinde stok miktarını azaltır."""
        for category, items in self.stock_manager.product_categories.items():
            for item in items:
                if item['product_name'] == product_name:
                    if item['stock'] > 0:
                        item['stock'] -= 1  # Stoktan bir adet düşürür
                        return True
                    else:
                        messagebox.showwarning("Stok Tükenmiş", f"{product_name} stokta kalmadı!")
                        return False
        return False



    def open_table(self, table_name, vip=False):
        self.current_table = table_name
        self.is_vip = vip
        self.table_indicator_label.config(text=f"Aktif Masa: {table_name}")
        self.update_order_display()

    def add_product(self, product_name, product_price):
        # Ürünü ekler
        if not self.reduce_stock(product_name):
            messagebox.showwarning("Stok Tükenmiş", f"{product_name} stokta kalmadı")
            return

        table = self.vip_tables[self.current_table] if self.is_vip else self.tables[self.current_table]
        table.add_order(product_name, product_price)
        self.update_order_display()
        self.update_table_colors()
    def remove_item(self):
        selected_items = self.selection_display.curselection()
        if not selected_items:
             messagebox.showwarning("Uyarı", "Lütfen silmek için bir ürün seçin.")
             return  

        table = self.vip_tables[self.current_table] if self.is_vip else self.tables[self.current_table]
        selected_text = self.selection_display.get(selected_items[0])
    
         # Ürün adını almak için '(' karakterine kadar olan kısmı ayır
        product_name = selected_text.split(" (")[0]
    
         # Ürünü sil
        table.remove_order(product_name)
        self.update_order_display()
        self.update_table_colors()

    def update_order_display(self):
        if not self.current_table:
            return
        table = self.vip_tables[self.current_table] if self.is_vip else self.tables[self.current_table]
        self.selection_display.delete(0, tk.END)
        items_count = {}
        for item, price in table.orders:
            if item in items_count:
                items_count[item]["count"] += 1
            else:
                items_count[item] = {"price": price, "count": 1}
        for item, details in items_count.items():
            count, price = details["count"], details["price"]
            self.selection_display.insert(tk.END, f"{item} ({count}x) - {price * count} TL")

    def save_order(self):
        messagebox.showinfo("Kaydedildi", f"{self.current_table} için sipariş kaydedildi.")

    def apply_discount(self, discount_key):
        if not self.current_table:
            messagebox.showwarning("Uyarı", "Önce bir masa seçin.")
            return
        discount_factor = self.discounts[discount_key]
        table = self.vip_tables[self.current_table] if self.is_vip else self.tables[self.current_table]
        table.apply_discount(discount_factor)
        self.update_order_display()
        messagebox.showinfo("İndirim", f"{discount_key} başarıyla uygulandı.")

    def close_table(self):
        if not self.current_table:
            messagebox.showwarning("Uyarı", "Önce bir masa seçin.")
            return
        table = self.vip_tables[self.current_table] if self.is_vip else self.tables[self.current_table]
        total = table.calculate_total()

        def finalize_payment(payment_type):
            nonlocal total
            if payment_type == "Nakit":
                self.daily_cash_total += total
            else:
                self.daily_card_total += total
            table.orders.clear() 
            self.current_table = None
            self.update_order_display()
            self.table_indicator_label.config(text="Masa Seçilmedi")
            self.update_table_colors()  
            payment_window.destroy()  

       
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Ödeme Türü")
        tk.Label(payment_window, text=f"Toplam Tutar: {total} TL").pack(pady=10)
        tk.Button(payment_window, text="Nakit", command=lambda: finalize_payment("Nakit")).pack(pady=5)
        tk.Button(payment_window, text="Kart", command=lambda: finalize_payment("Kart")).pack(pady=5)

    def update_table_colors(self):
        for table_name, table in {**self.tables, **self.vip_tables}.items():
            button = self.table_buttons[table_name]
            if table.orders:
                button.config(bg="red")
            else:
                button.config(bg="green")

    def show_daily_report(self):
        messagebox.showinfo("Günlük Rapor",
                            f"Nakit Toplam: {self.daily_cash_total} TL\nKart Toplam: {self.daily_card_total} TL\nToplam Tutar: {self.calculate_total_amount(self.daily_card_total,self.daily_cash_total)} TL")

    def run(self):
        self.root.mainloop()


app = RestaurantApp()
app.run()
