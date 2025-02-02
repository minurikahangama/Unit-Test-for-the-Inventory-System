# Admin login unit test
from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Order, Product
from user.models import Profile

class AdminLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='1234', is_staff=True)

    def test_admin_login(self):
        """Test that admin can log in successfully."""
        response = self.client.post('/', {'username': 'admin', 'password': '1234'})
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after login
        self.assertRedirects(response, '/dashboard/')  # Adjust based on actual redirect URL


# Test cases to verify that an admin can view staff profiles.
class StaffProfileTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='1234', is_staff=True)
        self.client.login(username='admin', password='1234')
        self.staff = User.objects.create_user(username='staff', password='5678', is_staff=False)

    def test_view_staff_profiles(self):
        """Test that admin can view staff profiles."""
        response = self.client.get('/staff/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'staff')
        
# Add, Update, Delete Product
class ProductCRUDTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='1234', is_staff=True)
        self.client.login(username='admin', password='1234')

    def test_add_product(self):
        """Test that a product can be added."""
        response = self.client.post('/product/', {'name': 'New Product', 'category': 'Electronics', 'quantity': 50})
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after adding
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_update_product(self):
        """Test that a product can be updated."""
        product = Product.objects.create(name='Old Product', category='Food', quantity=30)
        response = self.client.post(f'/product/update/{product.id}/', {'name': 'Updated Product', 'category': 'Electronics', 'quantity': 60})
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Product')
        self.assertEqual(product.quantity, 60)

    def test_delete_product(self):
        """Test that a product can be deleted."""
        product = Product.objects.create(name='Product to Delete', category='Food', quantity=10)
        response = self.client.post(f'/product/delete/{product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(name='Product to Delete').exists())
        
# Test cases to verify that orders can be viewed.

class OrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.client.login(username='user', password='1234')
        self.product = Product.objects.create(name='Test Product', category='Food', quantity=100)
        self.order = Order.objects.create(product=self.product, staff=self.user, order_quantity=5)

    def test_view_orders(self):
        """Test that orders can be viewed."""
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        
# View Products (Pie Chart)
class ProductChartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.client.login(username='user', password='1234')
        Product.objects.create(name='Product 1', category='Food', quantity=10)
        Product.objects.create(name='Product 2', category='Electronics', quantity=20)

    def test_view_products_pie_chart(self):
        """Test that products are displayed in a pie chart."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
        
# View Orders (Bar Chart)

class OrderChartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.client.login(username='user', password='1234')
        Product.objects.create(name='Product 1', category='Food', quantity=10)
        Product.objects.create(name='Product 2', category='Electronics', quantity=20)
        Order.objects.create(product=Product.objects.get(name='Product 1'), staff=self.user, order_quantity=5)
        Order.objects.create(product=Product.objects.get(name='Product 2'), staff=self.user, order_quantity=15)

    def test_view_orders_bar_chart(self):
        """Test that orders are displayed in a bar chart."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

# User Registration and Login
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class UserRegistrationAndLoginTests(TestCase):
    def test_user_registration(self):
        """Test that users can register."""
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password1': '1234password',
            'password2': '1234password',
            'email': 'newuser@example.com'  # Adding email field
        })
        if response.status_code != 302:
            print(response.content)  # Print response content to see the error

        self.assertEqual(response.status_code, 302)  # Check for redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())


    def test_user_login(self):
        """Test that users can log in."""
        User.objects.create_user(username='newuser', password='1234password')  # Same password as used in registration
        response = self.client.post('/', {'username': 'newuser', 'password': '1234password'})
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after login

#  Place an Order

class OrderPlacementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.client.login(username='user', password='1234')
        self.product = Product.objects.create(name='Product', category='Food', quantity=100)

    def test_place_order(self):
        """Test that users can place an order."""
        response = self.client.post('/dashboard/', {'product': self.product.id, 'order_quantity': 10})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(product=self.product, staff=self.user, order_quantity=10).exists())





