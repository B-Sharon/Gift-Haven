from models.__init__ import CURSOR, CONN
from models.user import User
from models.customer import Customer
from models.gift import Gift
from models.order import Order
from models.order_items import OrderItems
from datetime import datetime


def seed_database():
    # Drop existing tables
    User.drop_table()
    Customer.drop_table()
    Gift.drop_table()
    Order.drop_table()
    OrderItems.drop_table()

    # Create new tables
    User.create_table()
    Customer.create_table()
    Gift.create_table()
    Order.create_table()
    OrderItems.create_table()

    # Insert sample data
    # Users
    user1 = User.create(username="Sharon", full_name="Sharon B")
    user2 = User.create(username="jane_smith", full_name="Jane Smith")
    user3 = User.create(username="john_doe", full_name="John Doe")
    user4 = User.create(username="Wangeci", full_name="Lynn Wangeci")


    # Customers
    customer1 = Customer.create(name="Farah", contact="0723456789")
    customer2 = Customer.create(name="Moses", contact="0787654321")


    # Gifts
    gift1 = Gift.create(gift_name="Teddy Bear", gift_price=150)
    gift2 = Gift.create(gift_name="Flower Bouquet", gift_price=600)
    gift3 = Gift.create(gift_name="Chocolate Box", gift_price=250)
    gift4 = Gift.create(gift_name="Shoes", gift_price=1000)
   
    # Orders
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order1 = Order.create(date=current_date, customer_id=customer1.customer_id, user_id=user1.user_id, total_amount=0)
    order2 = Order.create(date=current_date, customer_id=customer1.customer_id, user_id=user2.user_id, total_amount=80)
    order3 = Order.create( date=current_date, customer_id=customer2.customer_id, user_id=user3.user_id, total_amount=40)
    order4 = Order.create( date=current_date, customer_id=customer2.customer_id, user_id=user4.user_id, total_amount=40)

    # Order Items
    OrderItems.create(order_id=order1.order_id, gift_id=gift1.gift_id, quantity=2, price =50)
    OrderItems.create(order_id=order3.order_id, gift_id=gift2.gift_id, quantity=1, price=60)
    OrderItems.create(order_id=order2.order_id, gift_id=gift3.gift_id, quantity=4, price = 90)
    OrderItems.create(order_id=order4.order_id, gift_id=gift1.gift_id, quantity=4, price = 90)

    print("Database seeded successfully.")


seed_database()
print("Seeded database")
