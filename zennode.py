class Product:
    def __init__(self, n, p):
        self.name = n
        self.price = p
        self.qty = 0
        self.gift = False

def catalog():
    return {
        "A": Product("Product A", 20),
        "B": Product("Product B", 40),
        "C": Product("Product C", 50)
    }

def discount(subtotal, discounts, products):
    max_d = 0
    d_name = "No Discount"

    for d, cond in discounts.items():
        curr_d = cond(subtotal, products)
        if curr_d > max_d:
            d_name, max_d = d, curr_d

    return d_name, max_d

def flat_10(subtotal, _):
    return 10 if subtotal > 200 else 0

def bulk_5(subtotal, products):
    return 0.05 * subtotal if any(p.qty > 10 for p in products.values()) else 0

def bulk_10(subtotal, products):
    return 0.1 * subtotal if sum(p.qty for p in products.values()) > 20 else 0

def tiered_50(subtotal, products):
    t_qty = sum(p.qty for p in products.values())
    max_qty = max(p.qty for p in products.values())
    return 0.5 * products["A"].price * max(0, max_qty - 15) if t_qty > 30 and max_qty > 15 else 0

DISCOUNTS = {
    "flat_10": flat_10,
    "bulk_5": bulk_5,
    "bulk_10": bulk_10,
    "tiered_50": tiered_50
}

def user_input(product):
    product.qty = int(input(f"How many units of {product.name} would you like to buy? "))
    product.gift = input(f"Do you want {product.name} wrapped as a gift? (yes/no): ").lower() == "yes"

products = catalog()

for p in products.values():
    user_input(p)

subtotal = sum(p.qty * p.price for p in products.values())
discount_name, discount_amount = discount(subtotal, DISCOUNTS, products)
shipping_fee = 5 * (subtotal // 10)  # $5 for every 10 units
gift_wrap_fee = sum(p.qty for p in products.values() if p.gift)

print("\nOrder Details:")
for p in products.values():
    print(f"{p.name}: {p.qty} x ${p.price} = ${p.qty * p.price}")

print(f"\nSubtotal: ${subtotal}")
print(f"Discount Applied: {discount_name} (${discount_amount})")
print(f"Shipping Fee: ${shipping_fee}")
print(f"Gift Wrap Fee: ${gift_wrap_fee}")

total = subtotal - discount_amount + shipping_fee + gift_wrap_fee
print(f"\nTotal: ${total}")
