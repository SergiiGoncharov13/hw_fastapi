import unittest

from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Guest, User
from src.shemas import GuestModel
from src.repository.users import (
    get_user_by_email,
    create_guest,
    confirmed_email,
    update_token,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='test@mail.com', db=self.session)
        self.assertIsNone(result)

    async def test_get_user_by_email_found(self):
        user = Guest()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test@mail.com', db=self.session)
        self.assertEqual(result, user)

    async def test_create_guest(self):
        body = GuestModel(name='test', email='test@mail.com', password='12345678')
        result = await create_guest(body=body, db=self.session)
        self.assertEqual(result.name, body.guest_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email_found(self):
        result = await confirmed_email(email='test@mail.com', db=self.session)
        self.assertIsNone(result)

    async def test_update_token_found(self):
        result = await update_token(user=User(), refresh_token='123', db=self.session)
        self.assertIsNone(result)

    async def test_update_avatar_found(self):
        user = Guest()
        self.session.query().filter().first.return_value = user
        result = await update_avatar(email='test@mail.com', url='www.test/name.jpg', db=self.session)
        self.assertEqual(result, user)

