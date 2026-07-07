from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthenticationTests(APITestCase):
    
    def setUp(self):
        # This runs before every test. We create a dummy user to test with.
        self.test_user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='SecurePassword123'
        )
        self.login_url = reverse('login') # Uses the 'name' from your urls.py

    def test_successful_login(self):
        """
        Ensure a user can log in and receive JWT tokens.
        """
        data = {
            'username': 'teststudent',
            'password': 'SecurePassword123'
        }
        
        # Simulates hitting 'Send' in Postman
        response = self.client.post(self.login_url, data, format='json')
        
        # Verify the server responded with 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify both tokens are in the response
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_failed_login(self):
        """
        Ensure an incorrect password rejects the login.
        """
        data = {
            'username': 'teststudent',
            'password': 'WrongPassword!'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        # Verify the server correctly blocks the attempt with a 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)