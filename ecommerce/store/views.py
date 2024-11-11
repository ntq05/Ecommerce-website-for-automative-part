from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer, 
    CartSerializer, CartItemSerializer, OrderSerializer
)

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# User Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

# List all categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# List all products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# List products by category
class ProductListByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category__id=category_id)

# Retrieve and update the user's cart
class CartView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

# Add an item to the cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]  # Make sure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=403)

        # Ensure cart exists or create one
        cart, created = Cart.objects.get_or_create(user=user)

        # Get product ID from the request data
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        
        # Ensure unit_price is set correctly
        unit_price = product.price  # Assuming unit_price should be the product's price

        # Create or get the CartItem, ensuring unit_price is not null
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'unit_price': unit_price}  # Set unit_price if not already set
        )
        
        # If the item was not created but already exists, ensure unit_price is not null
        if not created and cart_item.unit_price is None:
            cart_item.unit_price = unit_price
            cart_item.save()

        return Response({
            "message": "Item added to cart",
            "created": created,
            "cart_item_id": cart_item.id,
            "unit_price": cart_item.unit_price
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# Purchase items in the cart and create an order
class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure cart exists or create it
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if cart has items
        items = cart.items.all()
        if not items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total amount
        total_amount = sum(item.quantity * item.product.price for item in items)

        # Create the order
        order = Order.objects.create(user=request.user, total_amount=total_amount)

        # Create order items and link them to the order
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price
            )

        # Clear the cart after purchase
        items.delete()

        # Return the order data as response
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

