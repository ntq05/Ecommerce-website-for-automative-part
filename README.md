# Ecommerce Website for Automotive Parts
##Project Overview
This project is an Ecommerce Website for Automotive Parts, built using Django for the back end and React for the front end. It allows users to register, browse products by category, view product details, add products to a cart, and make purchases. The website is secured with authentication and authorization using Django’s token-based system.

## Table of Contents
Features
Tech Stack
Installation and Setup
Database Setup
API Endpoints
Testing
Contributing
License

## Features
User Authentication: Register, login, and secure session management using token-based authentication.
Product Listings: Browse products by category with detailed product pages.
Cart System: Add items to the cart and update quantities.
Order Management: Place orders and view order history.
Admin Management: Manage products and orders through Django's admin panel.
Secure: Permissions implemented to allow only authorized users to access certain features.

## Tech Stack
Backend: Django REST Framework, Django, SQL Server
Frontend: React (if integrated; otherwise, adjust)
Authentication: Token-based authentication using Django's built-in system
Database: SQL Server

## Installation and Setup
1) Clone the repository:
  git clone https://github.com/yourusername/ecommerce-website.git
  cd ecommerce-website
2) Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate   # On Windows, use: venv\Scripts\activate
3) Install the dependencies from requirements.txt:
  pip install -r requirements.txt
4) Set up the SQL Server database:
  Configure your database settings in settings.py.
  Run migrations to set up the schema:
    python manage.py migrate
5) Create a superuser for the admin panel:
   python manage.py createsuperuser
6) Run the development server:
   python manage.py runserver
## Database setup
Ensure your SQL Server is properly configured. Follow these steps to sync the schema
1) Update the DATABASES section in settings.py with your SQL Server credentials.
2) Apply the migrations:
   python manage.py migrate
3) Load initial data or start using the admin panel to add products and categories.

## API Endpoint
### Authentication
Register: /api/register/ (POST)
Login: /api/login/ (POST)
### Categories
List Categories: /api/categories/ (GET)
### Products
List All Products: /api/products/ (GET)
Products by Category: /api/categories/<category_id>/products/ (GET)
Product Detail: /api/products/<product_id>/ (GET)
### Cart
View Cart: /api/cart/ (GET)
Add to Cart: /api/cart/add/ (POST)
### Orders
Purchase Items in Cart: /api/purchase/ (POST)


