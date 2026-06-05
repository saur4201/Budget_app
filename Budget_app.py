class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        # Appends an object to the ledger list with positive amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # Uses check_funds to verify availability before withdrawing
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        # Calculates current balance by summing up all ledger entries
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        # Transfers funds to another category object if funds exist
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        # Returns True if amount is less than or equal to balance
        return amount <= self.get_balance()

    def __str__(self):
        # Formats the print layout of the category object
        title = f"{self.name}".center(30, "*")
        items = ""
        for item in self.ledger:
            desc = item["description"][:23]
            amt = f"{item['amount']:.2f}"[:7]
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + "\n" + items + total


def create_spend_chart(categories):
    # 1. Calculate withdrawal amounts per category and total withdrawals
    spendings = []
    for cat in categories:
        spent = sum(-item["amount"] for item in cat.ledger if item["amount"] < 0)
        spendings.append(spent)
        
    total_spent = sum(spendings)
    
    # 2. Calculate percentages rounded down to the nearest 10
    percentages = []
    for spent in spendings:
        if total_spent > 0:
            # Floor division trick to round down to nearest 10 percent
            percentages.append((spent / total_spent) * 100 // 10 * 10)
        else:
            percentages.append(0)

    # 3. Build the chart top-down (100 down to 0)
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -1,):
        if i % 10 == 0:
            chart += f"{i:>3}|"
            for pct in percentages:
                if pct >= i:
                    chart += " o "
                else:
                    chart += "   "
            chart += " \n" # Extra spacing at the end of each row

    # 4. Draw horizontal line divider
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # 5. Format category names vertically
    max_len = max(len(cat.name) for cat in categories)
    names = [cat.name.ljust(max_len) for cat in categories]

    for i in range(max_len):
        chart += "    "
        for name in names:
            chart += f" {name[i]} "
        chart += " "
        if i < max_len - 1:
            chart += "\n" # Do not append newline on the final line

    return chart


# 1. Create instances of your categories
food = Category('Food')
clothing = Category('Clothing')
auto = Category('Auto')

# 2. Add some mock transactions
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food")

clothing.deposit(500, "initial deposit")
food.transfer(50, clothing) # Transfer $50 from Food to Clothing
clothing.withdraw(25.50, "t-shirt")

auto.deposit(300, "initial deposit")
auto.withdraw(60.00, "gas")

# 3. Print the receipt layouts (This triggers __str__)
print(food)
print("\n" + "="*30 + "\n") # Visual separator line
print(clothing)

print("\n" + "="*30 + "\n")

# 4. Generate and print the spend chart visualization
chart_output = create_spend_chart([food, clothing, auto])
print(chart_output)

