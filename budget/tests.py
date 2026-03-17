from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Transaction

User = get_user_model()


class TransactionCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student1", password="CapstonePass123!")
        self.other_user = User.objects.create_user(username="student2", password="CapstonePass123!")
        self.client.login(username="student1", password="CapstonePass123!")

    def test_transaction_list_only_shows_current_users_records(self):
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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My transaction")
        self.assertNotContains(response, "Other user transaction")

    def test_user_can_edit_their_own_transaction(self):
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

        transaction.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(transaction.category, "Groceries")
        self.assertEqual(str(transaction.amount), "42.50")
        self.assertContains(response, "Transaction updated.")

    def test_user_cannot_edit_another_users_transaction(self):
        transaction = Transaction.objects.create(
            user=self.other_user,
            date="2026-03-01",
            type=Transaction.EXPENSE,
            category="Utilities",
            amount="75.00",
        )

        response = self.client.get(reverse("edit_transaction", args=[transaction.id]))

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_their_own_transaction(self):
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

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Transaction.objects.filter(id=transaction.id).exists())
        self.assertContains(response, "Transaction deleted.")
