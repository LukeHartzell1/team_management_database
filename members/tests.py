from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import TeamMember

class TeamMemberModelTest(TestCase):
    def test_str_method(self):
        member = TeamMember.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john.doe@example.com",
            role="regular"
        )
        self.assertEqual(str(member), "John Doe")

class TeamMemberAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Base URL for the team member API endpoints.
        # Adjust this if your URL configuration changes.
        self.list_url = '/members/api/team-members/'
        # Create an initial team member.
        self.member = TeamMember.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone="0987654321",
            email="jane.doe@example.com",
            role="admin"
        )

    def test_get_team_members(self):
        """Test retrieving the list of team members."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "Jane")

    def test_create_team_member_success(self):
        """Test successful creation of a team member."""
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "phone": "1112223333",
            "email": "alice.smith@example.com",
            "role": "regular"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamMember.objects.count(), 2)
        new_member = TeamMember.objects.get(email="alice.smith@example.com")
        self.assertEqual(new_member.role, "regular")

    def test_create_team_member_duplicate_email(self):
        """Test that creating a member with a duplicate email fails."""
        data = {
            "first_name": "Bob",
            "last_name": "Jones",
            "phone": "2223334444",
            "email": "jane.doe@example.com",  # Duplicate email
            "role": "regular"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_team_member_invalid_email(self):
        """Test that creating a member with an invalid email fails."""
        data = {
            "first_name": "David",
            "last_name": "Green",
            "phone": "1234567890",
            "email": "notanemail",  # Invalid email format
            "role": "regular"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_phone_number_validation(self):
        """
        Test that creating a team member with a phone number containing
        non-digit characters returns a validation error.
        This assumes your serializer/model enforces a digits-only phone number.
        """
        data = {
            "first_name": "Charlie",
            "last_name": "Brown",
            "phone": "123-456-7890",  # Invalid: contains dashes
            "email": "charlie.brown@example.com",
            "role": "regular"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)

    def test_update_team_member(self):
        """Test updating a team member's details via PUT."""
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "phone": "5556667777",
            "email": "jane.doe@example.com",
            "role": "regular"  # Change role from admin to regular
        }
        detail_url = f'{self.list_url}{self.member.id}/'
        response = self.client.put(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertEqual(self.member.phone, "5556667777")
        self.assertEqual(self.member.role, "regular")

    def test_partial_update_team_member(self):
        """Test partially updating a team member using PATCH."""
        detail_url = f'{self.list_url}{self.member.id}/'
        data = {
            "phone": "9998887777"
        }
        response = self.client.patch(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertEqual(self.member.phone, "9998887777")

    def test_delete_team_member(self):
        """Test deletion of a team member."""
        detail_url = f'{self.list_url}{self.member.id}/'
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TeamMember.objects.count(), 0)

    def test_delete_nonexistent_team_member(self):
        """Test deletion of a non-existent team member returns 404."""
        detail_url = f'{self.list_url}99999/'
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_ordering(self):
        """
        Create additional members and test that the list API returns
        members ordered by ID (or by your default ordering).
        """
        member2 = TeamMember.objects.create(
            first_name="Alice",
            last_name="Smith",
            phone="1112223333",
            email="alice.smith@example.com",
            role="regular"
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect two team members
        self.assertEqual(len(response.data), 2)
        # Check that the returned IDs are in ascending order
        ids = [member['id'] for member in response.data]
        self.assertEqual(ids, sorted(ids))
