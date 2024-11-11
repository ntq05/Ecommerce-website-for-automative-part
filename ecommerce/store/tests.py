from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from store.models import Category, Product, Cart, CartItem

class EcommerceApiTests(APITestCase):
    
    def setUp(self):
        # Create a user and get their token
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        
        # Create test data (categories, products)
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", price=10.0, category=self.category)
        
    def authenticate(self):
        # Set the authentication token in the headers for the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_product_list(self):
        self.authenticate()  # Authenticate the user
        response = self.client.get('/store/products/')  # Corrected URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_by_category(self):
        self.authenticate()  # Authenticate the user
        response = self.client.get(f'/store/categories/{self.category.id}/products/')  # Corrected URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        self.authenticate()  # Authenticate the user
        response = self.client.post('/store/add-to-cart/', {'product_id': self.product.id})  # Corrected URL
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cart(self):
        self.authenticate()  # Authenticate the user
        response = self.client.get('/store/cart/')  # Corrected URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase(self):
        self.authenticate()  # Authenticate the user
        
        # Ensure the cart has an item before purchase
        cart, created = Cart.objects.get_or_create(user=self.user)
        product = Product.objects.create(name="Test Product", price=100.0, category=self.category)
        
        # Add product to cart
        CartItem.objects.create(cart=cart, product=product, quantity=2, unit_price=product.price)

        # Try to purchase the items in the cart
        response = self.client.post('/purchase/', {})
        
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the total_amount is correctly calculated
        self.assertTrue('total_amount' in response.data)
        self.assertEqual(response.data['total_amount'], 200.0)  # Assuming product price is 100 and quantity is 2

