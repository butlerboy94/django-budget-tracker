from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Bill, Transaction

# Use Django's active User model for creating test accounts.
User = get_user_model()


class TransactionCrudTests(TestCase):
    # This test class checks that the transaction CRUD pages behave correctly.
    def setUp(self):
        # Create two users so the tests can verify that one user's transaction
        # data never appears in or modifies another user's records.
        self.user = User.objects.create_user(username="student1", password="CapstonePass123!")
        self.other_user = User.objects.create_user(username="student2", password="CapstonePass123!")
        self.client.login(username="student1", password="CapstonePass123!")

    def test_transaction_list_only_shows_current_users_records(self):
        # Seed one transaction for the logged-in user and one for another user.
        Transaction.objects.create(
            user=self.user,
            date="2026-03-01",
            type=Transaction.INCOME,
            category="Paycheck",
            amount="1000.00",
            note="My transaction",
        )
        Transaction.objects.create(
            user=self.other_user,
            date="2026-03-02",
            type=Transaction.EXPENSE,
            category="Rent",
            amount="500.00",
            note="Other user transaction",
        )

        response = self.client.get(reverse("transaction_list"))

        # The page should render successfully and show only the current user's
        # data, proving the filtering logic is working correctly.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My transaction")
        self.assertNotContains(response, "Other user transaction")

    def test_user_can_edit_their_own_transaction(self):
        # Create a transaction owned by the logged-in user.
        transaction = Transaction.objects.create(
            user=self.user,
            date="2026-03-01",
            type=Transaction.EXPENSE,
            category="Food",
            amount="20.00",
            note="Lunch",
        )

        response = self.client.post(
            reverse("edit_transaction", args=[transaction.id]),
            {
                "date": "2026-03-03",
                "type": Transaction.EXPENSE,
                "category": "Groceries",
                "amount": "42.50",
                "note": "Weekly shopping",
            },
            follow=True,
        )

        # Refresh the object from the database to confirm the update was saved.
        transaction.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(transaction.category, "Groceries")
        self.assertEqual(str(transaction.amount), "42.50")
        self.assertContains(response, "Transaction updated.")

    def test_user_cannot_edit_another_users_transaction(self):
        # Create a transaction owned by a different user.
        transaction = Transaction.objects.create(
            user=self.other_user,
            date="2026-03-01",
            type=Transaction.EXPENSE,
            category="Utilities",
            amount="75.00",
        )

        response = self.client.get(reverse("edit_transaction", args=[transaction.id]))

        # A 404 response confirms the object is not exposed to unauthorized
        # users through the edit route.
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_their_own_transaction(self):
        # Create a transaction that the logged-in user is allowed to remove.
        transaction = Transaction.objects.create(
            user=self.user,
            date="2026-03-01",
            type=Transaction.INCOME,
            category="Freelance",
            amount="250.00",
        )

        response = self.client.post(
            reverse("delete_transaction", args=[transaction.id]),
            follow=True,
        )

        # After the POST request, the record should be gone and the success
        # message should be displayed on the redirected page.
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Transaction.objects.filter(id=transaction.id).exists())
        self.assertContains(response, "Transaction deleted.")


class BillCrudTests(TestCase):
    # This test class checks that the bill CRUD pages behave correctly.
    def setUp(self):
        # Create two users so the tests can verify bill ownership rules.
        self.user = User.objects.create_user(username="billuser1", password="CapstonePass123!")
        self.other_user = User.objects.create_user(username="billuser2", password="CapstonePass123!")
        self.client.login(username="billuser1", password="CapstonePass123!")

    def test_bill_list_only_shows_current_users_records(self):
        # Create one bill for the logged-in user and one for another user.
        Bill.objects.create(
            user=self.user,
            name="Electric Bill",
            amount="120.00",
            due_date="2026-03-20",
            paid=False,
            notes="Current user bill",
        )
        Bill.objects.create(
            user=self.other_user,
            name="Internet Bill",
            amount="80.00",
            due_date="2026-03-25",
            paid=False,
            notes="Other user bill",
        )

        response = self.client.get(reverse("bill_list"))

        # The page should only show the current user's bill information.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current user bill")
        self.assertNotContains(response, "Other user bill")

    def test_user_can_edit_their_own_bill(self):
        # Create a bill owned by the logged-in user.
        bill = Bill.objects.create(
            user=self.user,
            name="Phone Bill",
            amount="60.00",
            due_date="2026-03-18",
            paid=False,
            notes="Original note",
        )

        response = self.client.post(
            reverse("edit_bill", args=[bill.id]),
            {
                "name": "Updated Phone Bill",
                "amount": "65.50",
                "due_date": "2026-03-22",
                "paid": "on",
                "notes": "Updated note",
            },
            follow=True,
        )

        # Refresh the bill from the database to confirm the update was saved.
        bill.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bill.name, "Updated Phone Bill")
        self.assertEqual(str(bill.amount), "65.50")
        self.assertTrue(bill.paid)
        self.assertContains(response, "Bill updated.")

    def test_user_cannot_edit_another_users_bill(self):
        # Create a bill owned by a different user.
        bill = Bill.objects.create(
            user=self.other_user,
            name="Rent",
            amount="900.00",
            due_date="2026-03-05",
            paid=False,
        )

        response = self.client.get(reverse("edit_bill", args=[bill.id]))

        # The bill should not be accessible through the edit page.
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_their_own_bill(self):
        # Create a bill the logged-in user is allowed to remove.
        bill = Bill.objects.create(
            user=self.user,
            name="Water Bill",
            amount="45.00",
            due_date="2026-03-28",
            paid=False,
        )

        response = self.client.post(reverse("delete_bill", args=[bill.id]), follow=True)

        # After deletion, the bill should be removed from the database and the
        # success message should appear.
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bill.objects.filter(id=bill.id).exists())
        self.assertContains(response, "Bill deleted.")
