# Gift Haven

## Phase 3 Python Project

#### Date: 2024/06/12

#### By *Sharon Byegon*

## Overview
Welcome to Gift Haven! This project is a Command Line Interface (CLI) application designed to manage a gift shop's operations including managing users, customers, gifts, orders, and order items. 

### Table of Contents
1. Introduction
2. Features
3. Installation
4. Usage
5. Dependencies
6. Technology used
7. Contributing
8. Contact
9. License
10. Feedback

## Introduction
Gift Haven is a Python-based CLI application that allows users to perform various operations related to managing a gift shop. It provides functionalities such as adding users, customers, gifts, creating orders, and managing order items.
<br> 
<br>
The application uses Python's standard library for database interactions, ensuring flexibility and simplicity.

## Features
1. **User Management:** 
- Add, update, delete users.
- Find users by username or ID.
- List all users.

2. **Customer Management:** 
- Add, update, delete customers.
- Find users by contact or ID.
- List all customers.

3.  **Gift Management:** 
- Add, update, delete gifts.
- Find gifts by name or ID.
- List all gifts.

4.  **Order Management:** 
- Create orders with specified customer and user IDs.
- Update order details including customer and user IDs.
- Delete orders.
- Find orders by ID.
- List all orders.

5.  **Order Item Management:** 
- Add, update, delete order items.
- Find order items by ID or associated order ID.
- List order items for a specific order.

6.  **CLI Interface:** 
- Easy-to-use command line interface with a menu-driven system for seamless navigation.

## Project Strucure
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
    ├── cli.py
    ├── db
    │   ├── models.py
    │   ├── seed.py
    ├── debug.py
    ├── helpers.py
    ├── models
    │   ├── __init__.py
    │   ├── customer.py
    │   ├── gift.py
    │   ├── order_items.py
    │   ├── order.py
    │   └── user.py
    ├── company.db  # Database file
    ├── seed.py     # Script to seed the database
    └── helpers.py  # Utility functions

## Installation
To run Gift Haven on your local machine, follow these steps:

1. Clone the repository to your local machine:
    ```
    git clone https://github.com/B-Sharon/Gift-Haven-
    ```

2. Navigate to the project directory in your terminal.

3. Install the dependencies:
    - Gift Haven uses Python Standard Libraries. No additional dependecies required.

4. Set up the database:
    - Ensure you have a compatible database (e.g., SQLite, PostgreSQL).
    - Update the database configuration in the application code (models.py or similar) as per your database setup.

5. Running the application:
    - Activate the virtual environment:
        ```
        pipenv shell
        ```
    - Seed the database with some initial data:
        ```
        python lib/seed.py
        ```
    - Run the CLI application:
        ```
        python lib/cli.py
        ```

## Usage
Follow the on-screen menu to navigate through different options such as managing users, customers, gifts, orders, and order items. Each option provides sub-options for adding, updating, deleting, finding, and listing relevant entities.

Below is an illustration of the ouptut displayed for the main menu:

    
         Welcome to Gift Haven!
            1. User
            2. Customer
            3. Gift
            4. Order
            5. Order Items
            6. Exit
        
        Enter your choice: 
    
        If choice 3 is picked and the option to list all gifts is chosen, this will be the diplay:

            Enter your choice: 3

            Gift Menu:
            1. List all gifts
            2. Add gift
            3. Find gift by name
            4. Find gift by ID
            5. Update gift
            6. Delete gift
            7. Back to main menu
            
            Enter your choice: 1
            <Gift 1: Teddy Bear, 25.0>
            <Gift 2: Flower Bouquet, 40.0>
            <Gift 3: Chocolate Box, 15.0>
            <Gift 4: Shoes, 400.0>
            <Gift 5: Watch, 100.0>
    

## Dependency
- **Python Standard Libraries:** Used for CLI interface, datetime handling, and basic input/output operations.


## Technologies Used
- **Python:** The app is built using the Python library.

## Contributing
Contributions to Gift Haven are welcome! If you'd like to contribute:

- Fork the repository.
- Create your feature branch (`git checkout -b feature/YourFeature`)
- Commit your changes (`git commit -am 'Add some feature'`).
- Push to the branch (`git push origin feature/YourFeature`).
- Create a new Pull Request.

Please ensure your code follows the project's coding style and includes appropriate documentation.


## Contact
For any support or inquiries, please contact **Sharon Byegon** at byegon.sharon@gmail.com


## License
This project is licensed under the MIT License.

## Feedback
If you have any feedback or suggestions for improvement, please feel free to contact me. I'd love to hear from you!
