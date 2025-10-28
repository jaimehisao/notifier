import unittest
from unittest.mock import patch, MagicMock
import os
import notifier
from click.testing import CliRunner

class TestNotifier(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        # Create a dummy config file for testing
        with open('test_config.yml', 'w') as f:
            f.write("""
channels:
  info:
    - mailto://user:pass@gmail.com
  warnings:
    - tgram://bottoken/chatid
""")
        # Create a dummy invalid config file for testing
        with open('invalid_config.yml', 'w') as f:
            f.write("channels: [")

    def tearDown(self):
        os.remove('test_config.yml')
        os.remove('invalid_config.yml')

    def test_load_config_not_found(self):
        """
        Test that load_config returns None when the config file is not found.
        """
        result = notifier.load_config('non_existent_config.yml')
        self.assertIsNone(result)

    def test_load_config_invalid_yaml(self):
        """
        Test that load_config returns None when the config file is invalid.
        """
        result = notifier.load_config('invalid_config.yml')
        self.assertIsNone(result)

    @patch('notifier.send_notification')
    def test_cli_send_success(self, mock_send_notification):
        """
        Test that the CLI send command calls send_notification with the correct arguments.
        """
        result = self.runner.invoke(notifier.cli, [
            'send',
            '--title', 'Test Title',
            '--body', 'Test Body',
            '--channel', 'info',
            '--config', 'test_config.yml'
        ])
        self.assertEqual(result.exit_code, 0)
        mock_send_notification.assert_called_once_with(
            'Test Title',
            'Test Body',
            ['mailto://user:pass@gmail.com']
        )

    @patch('notifier.send_notification')
    def test_cli_send_channel_not_found(self, mock_send_notification):
        """
        Test that the CLI send command gracefully handles a missing channel.
        """
        result = self.runner.invoke(notifier.cli, [
            'send',
            '--title', 'Test Title',
            '--body', 'Test Body',
            '--channel', 'non_existent_channel',
            '--config', 'test_config.yml'
        ])
        self.assertEqual(result.exit_code, 0)
        mock_send_notification.assert_not_called()

    @patch('apprise.Apprise')
    def test_send_notification_success(self, mock_apprise):
        """
        Test that send_notification returns True on successful notification.
        """
        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = True

        urls = ["mailto://user:pass@gmail.com"]
        result = notifier.send_notification("Test", "Test", urls)
        self.assertTrue(result)
        mock_apprise_instance.add.assert_called_once_with(urls[0])
        mock_apprise_instance.notify.assert_called_once_with(body="Test", title="Test")

    @patch('apprise.Apprise')
    def test_send_notification_failure(self, mock_apprise):
        """
        Test that send_notification returns False on failed notification.
        """
        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = False

        urls = ["mailto://user:pass@gmail.com"]
        result = notifier.send_notification("Test", "Test", urls)
        self.assertFalse(result)
        mock_apprise_instance.add.assert_called_once_with(urls[0])
        mock_apprise_instance.notify.assert_called_once_with(body="Test", title="Test")

if __name__ == '__main__':
    unittest.main()
