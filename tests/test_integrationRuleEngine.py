import unittest
from unittest.mock import MagicMock, patch
from ruleEngine import RuleLoader, RuleProcessor
import json
import os

class TestRuleEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.rules_path = 'tests/integration_rules.json'

        self.sample_rules = [
            {   
                "ruleid": "TRid003",
                "name": "Integration Test Rule",
                "predicate": "All",
                "conditions": [
                    {"field": "sender", "predicate": "Contains", "value": "example.com"}
                ],
                "actions": ["mark_as_read", "move_to_label:INBOX"]
            }
        ]

        with open(self.rules_path, 'w') as f:
            json.dump(self.sample_rules, f)

        self.sample_email = {
            "id": "email_123",
            "sender": "noreply@example.com",
            "subject": "Test Subject",
            "label_ids": "UNREAD"
        }

    def tearDown(self):
        if os.path.exists(self.rules_path):
            os.remove(self.rules_path)

    @patch('ruleEngine.storeProcessedHistory')
    @patch('ruleEngine.ActionExecutor.performActions')
    def test_rule_engine_end_to_end_flow_with_history(self, mock_perform_actions, mock_store_history):
        # Step 1: Load Rules
        rules = RuleLoader.loadRules(self.rules_path)

        # Step 2: Prepare Mock Gmail Service
        mock_service = MagicMock()

        # Step 3: Process Email
        processor = RuleProcessor(mock_service, rules)
        processor.processEmails([self.sample_email])

        # Step 4: Assert performActions was called
        mock_perform_actions.assert_called_once_with(
            mock_service,
            'email_123',
            ['mark_as_read', 'move_to_label:INBOX']
        )

        # Step 5: Assert storeProcessedHistory was called once with expected record
        mock_store_history.assert_called_once()
        record = mock_store_history.call_args.args[0]  # The single record passed in

        # Now assert values inside the record (assuming it's a tuple or a dataclass)
        print(record)
        email_id, rule_id, actions, status, timestamp = record

        self.assertEqual(email_id, 'email_123')
        self.assertEqual(rule_id, 'TRid003')
        self.assertEqual(actions, "mark_as_read,move_to_label:INBOX")
        self.assertEqual(status, 'Success')


if __name__ == '__main__':
    unittest.main()
