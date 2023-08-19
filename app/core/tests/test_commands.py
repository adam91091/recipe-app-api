"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # mock check method of BaseCommand django class
        patched_check.return_value = True

        # call wait_for_db command
        call_command('wait_for_db')

        # check if patched check was called with the database=['default']
        # parameter
        patched_check.assert_called_once_with(databases=['default'])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # patch time.sleep to avoid real sleeping thread
        # side effect allows for passing different items that get handled
        # differently
        # if we pass an exception, then mocking library knows that it
        # should raise that exception
        # if we pass an boolean, then it return a boolean value

        # Below, we want to have 2 Psycopg2Error for the 1st and 2nd calls
        # For 3rd, 4th, 5th, we want to have OperationalError. For last call,
        # we want to have boolean
        # THIS IS THE SIMULATION OF HOW check method behaves when cannot
        # connect to db as its not ready
        # The numbers can be different, it's just an simulation
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # We just check if the method is called 6 times
        self.assertEqual(patched_check.call_count, 6)
        # check if patched check was called with the database
        patched_check.assert_called_with(databases=['default'])
