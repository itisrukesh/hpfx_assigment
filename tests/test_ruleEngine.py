import unittest
from unittest.mock import MagicMock, patch
from ruleEngine import RuleLoader, RuleEvaluator, ActionExecutor, RuleProcessor
import os
import json

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        # Create a sample rules.json file for RuleLoader
        self.rules_path = 'tests/test_rules.json'
        self.sample_rules = [
            {   
                "rule_id": "TRid001",
                "name": "Test Rule",
                "predicate": "All",
                "conditions": [
                    {"field": "sender", "predicate": "Contains", "value": "example.com"},
                    {"field": "subject", "predicate": "Does Not Contain", "value": "Spam"}
                ],
                "actions": ["mark_as_read", "move_to_label:test"]
            }
        ]
        with open(self.rules_path, 'w') as f:
            json.dump(self.sample_rules, f)

        self.sample_email = {
            "id": "email_1",
            "sender": "admin@example.com",
            "subject": "Welcome!",
            "label_ids": "UNREAD,CATEGORY_UPDATES,INBOX"
        }

    def tearDown(self):
        if os.path.exists(self.rules_path):
            os.remove(self.rules_path)

    def test_rule_loader_success(self):
        rules = RuleLoader.loadRules(self.rules_path)
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['name'], "Test Rule")

    def test_rule_loader_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            RuleLoader.loadRules('dummy.json')

    def test_rule_evaluator_match_all(self):
        rule = self.sample_rules[0]
        result = RuleEvaluator.matchRule(rule, self.sample_email)
        self.assertTrue(result)

    def test_rule_evaluator_fail_condition(self):
        rule = self.sample_rules[0]
        bad_email = {**self.sample_email, "subject": "Spam Offer"}
        self.assertFalse(RuleEvaluator.matchRule(rule, bad_email))

    @patch('ruleEngine.fetchValidLabels')
    def test_action_executor_perform_actions(self, mock_get_labels):
        # Mock label mapping
        mock_get_labels.return_value = {'TEST': 'Label_2634268560439023589'}

        mock_service = MagicMock()
        ActionExecutor.performActions(mock_service, 'email_1', ['mark_as_read', 'move_to_label:test'])

        # Validate Gmail modify call was made
        self.assertTrue(mock_service.users().messages().modify.called)

    @patch('ruleEngine.ActionExecutor.performActions')
    @patch('ruleEngine.RuleEvaluator.matchRule')
    def test_rule_processor_calls_evaluator_and_executor(self, mock_match, mock_perform):
        mock_match.return_value = True  # Force match
        mock_service = MagicMock()

        rules = self.sample_rules
        emails = [self.sample_email]

        processor = RuleProcessor(mock_service, rules)
        processor.processEmails(emails)

        mock_match.assert_called_once()
        mock_perform.assert_called_once()

if __name__ == '__main__':
    unittest.main()
