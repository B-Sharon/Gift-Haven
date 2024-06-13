from models.gift import Gift
from models.customer import Customer
from models.user import User
from models.order import Order
from models.order_items import OrderItems


def exit_program():
    print("Goodbye!")
    exit()


# Gift functions
def list_gifts():
    gifts = Gift.get_all()
    for gift in gifts:
        print(gift)


def find_gift_by_name():
    name = input("Enter the gift's name: ")
    gift = Gift.find_by_name(name)
    print(gift) if gift else print(f'Gift {name} not found')


def find_gift_by_id():
    id_ = input("Enter the gift's id: ")
    gift = Gift.find_by_id(id_)
    print(gift) if gift else print(f'Gift {id_} not found')


def create_gift():
    name = input("Enter the gift's name: ")
    price = input("Enter the gift's price: ")
    try:
        gift = Gift.create(name, float(price))
        print(f'Success: {gift}')
    except Exception as exc:
        print("Error creating gift: ", exc)


def update_gift():
    id_ = input("Enter the gift's id: ")
    if gift := Gift.find_by_id(id_):
        try:
            name = input("Enter the gift's new name: ")
            gift.name = name
            price = input("Enter the gift's new price: ")
            gift.price = float(price)
            gift.update()
            print(f'Success: {gift}')
        except Exception as exc:
            print("Error updating gift: ", exc)
    else:
        print(f'Gift {id_} not found')


def delete_gift():
    id_ = input("Enter the gift's id: ")
    if gift := Gift.find_by_id(id_):
        gift.delete()
        print(f'Gift {id_} deleted')
    else:
        print(f'Gift {id_} not found')


# Customer functions
def list_customers():
    customers = Customer.get_all()
    for customer in customers:
        print(customer)


def find_customer_by_contact():
    contact = input("Enter the customer's contact number: ")
    customer = Customer.find_by_contact(contact)
    print(customer) if customer else print(f'Customer {contact} not found')


def find_customer_by_id():
    id_ = input("Enter the customer's id: ")
    customer = Customer.find_by_id(id_)
    print(customer) if customer else print(f'Customer {id_} not found')


def create_customer():
    name = input("Enter the customer's name: ")
    contact_info = input("Enter the customer's contact info: ")
    try:
        customer = Customer.create(name, contact_info)
        print(f'Success: {customer}')
    except Exception as exc:
        print("Error creating customer: ", exc)


def update_customer():
    id_ = input("Enter the customer's id: ")
    if customer := Customer.find_by_id(id_):
        try:
            name = input("Enter the customer's new name: ")
            customer.name = name
            contact_info = input("Enter the customer's new contact info: ")
            customer.contact_info = contact_info
            customer.update()
            print(f'Success: {customer}')
        except Exception as exc:
            print("Error updating customer: ", exc)
    else:
        print(f'Customer {id_} not found')


def delete_customer():
    id_ = input("Enter the customer's id: ")
    if customer := Customer.find_by_id(id_):
        customer.delete()
        print(f'Customer {id_} deleted')
    else:
        print(f'Customer {id_} not found')


# User functions
def list_users():
    users = User.get_all()
    for user in users:
        print(user)


def find_user_by_username():
    username = input("Enter the user's username: ")
    user = User.find_by_username(username)
    print(user) if user else print(f'User {username} not found')


def find_user_by_id():
    id_ = input("Enter the user's id: ")
    user = User.find_by_id(id_)
    print(user) if user else print(f'User {id_} not found')


def create_user():
    username = input("Enter the user's username: ")
    full_name = input("Enter the user's full name: ")
    try:
        user = User.create(username=username, full_name=full_name)
        print(f'Success: {user}')
    except Exception as exc:
        print("Error creating user: ", exc)


def update_user():
    id_ = input("Enter the user's id: ")
    if user := User.find_by_id(id_):
        try:
            username = input("Enter the user's new username: ")
            user.username = username
            full_name = input("Enter the user's new full name: ")
            user.full_name = full_name
            user.update()
            print(f'Success: {user}')
        except Exception as exc:
            print("Error updating user: ", exc)
    else:
        print(f'User {id_} not found')


def delete_user():
    id_ = input("Enter the user's id: ")
    if user := User.find_by_id(id_):
        user.delete()
        print(f'User {id_} deleted')
    else:
        print(f'User {id_} not found')


# Order functions
def list_orders():
    orders = Order.get_all()
    for order in orders:
        print(order)


def find_order_by_id():
    id_ = input("Enter the order's id: ")
    order = Order.find_by_id(id_)
    print(order) if order else print(f'Order {id_} not found')


def create_order():
    date = input("Enter the date (YYYY-MM-DD): ")
    customer_id = input("Enter the customer's id: ")
    user_id = input("Enter the user's id: ")
    total_amount = input("Enter the total amount: ")
    try:
        order = Order.create(date, customer_id, user_id, float(total_amount))
        print(f'Success: {order}')
    except Exception as exc:
        print("Error creating order: ", exc)


def update_order():
    id_ = input("Enter the order's id: ")
    if order := Order.find_by_id(id_):
        try:
            date = input("Enter the new date (YYYY-MM-DD): ")
            customer_id = input("Enter the new customer's id: ")
            user_id = input("Enter the new user's id: ")
            total_amount = input("Enter the new total amount: ")
            order.date = date
            order.customer_id = customer_id
            order.user_id = user_id
            order.total_amount = float(total_amount)
            order.update()
            print(f'Success: {order}')
        except Exception as exc:
            print("Error updating order: ", exc)
    else:
        print(f'Order {id_} not found')


def delete_order():
    id_ = input("Enter the order's id: ")
    if order := Order.find_by_id(id_):
        order.delete()
        print(f'Order {id_} deleted')
    else:
        print(f'Order {id_} not found')


# OrderItems functions
def list_order_items():
    order_id = input("Enter the order id: ")
    items = OrderItems.find_by_order_id(order_id)
    for item in items:
        print(item)


def find_order_item_by_id():
    id_ = input("Enter the order item id: ")
    order_item = OrderItems.find_by_id(id_)
    print(order_item) if order_item else print(f'Order item {id_} not found')


def create_order_item():
    order_id = input("Enter the order id: ")
    gift_id = input("Enter the gift id: ")
    quantity = input("Enter the quantity: ")
    price = input("Enter the price: ")
    try:
        order_item = OrderItems.create(order_id, gift_id, int(quantity), float(price))
        print(f'Success: {order_item}')
    except Exception as exc:
        print("Error creating order item: ", exc)


def update_order_item():
    id_ = input("Enter the order item id: ")
    if order_item := OrderItems.find_by_id(id_):
        try:
            order_id = input("Enter the new order id: ")
            gift_id = input("Enter the new gift id: ")
            quantity = input("Enter the new quantity: ")
            price = input("Enter the new price: ")
            order_item.order_id = order_id
            order_item.gift_id = gift_id
            order_item.quantity = int(quantity)
            order_item.price = float(price)
            order_item.update()
            print(f'Success: {order_item}')
        except Exception as exc:
            print("Error updating order item: ", exc)
    else:
        print(f'Order item {id_} not found')


def delete_order_item():
    id_ = input("Enter the order item id: ")
    if order_item := OrderItems.find_by_id(id_):
        order_item.delete()
        print(f'Order item {id_} deleted')
    else:
        print(f'Order item {id_} not found')
