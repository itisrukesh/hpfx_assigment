# rule_engine.py

import json
from typing import List, Dict
from auth import authenticateGmail
from fetchEmail import fetchEmails_from_Db

class RuleLoader:
    """This class responsible for loading rules from a different data sources."""

    @staticmethod
    def loadRules(filepath: str) -> List[Dict]:
        """
        Load and parse rules from the given JSON file.

        Args:
            filepath (str): Path to the rules.json file.

        Returns:
            List[Dict]: List of rule dictionaries.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            ValueError: If loaded data is not a list of rules.
        """
        try:
            with open(filepath, 'r') as f:
                rules = json.load(f)

            if not isinstance(rules, list):
                raise ValueError("Rules file must contain a list of rules.")

            return rules

        except FileNotFoundError:
            raise FileNotFoundError(f"Rules file not found at path: {filepath}")
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in rules file: {str(e)}")


class RuleEvaluator:
    """Class responsible for evaluating if an email matches a rule."""

    SUPPORTED_PREDICATES = {
        'Contains': lambda field, value: value.lower() in (field or '').lower(),
        'Does Not Contain': lambda field, value: value.lower() not in (field or '').lower(),
        'Equals': lambda field, value: (field or '').lower() == value.lower()
    }

    @classmethod
    def matchRule(cls, rule: Dict, email: Dict) -> bool:
        """
        Check if an email matches a rule based on its conditions.

        Args:
            rule (Dict): A single rule dictionary.
            email (Dict): A single email dictionary.

        Returns:
            bool: True if email matches the rule, False otherwise.
        """
        predicate = rule.get('predicate', 'All')
        conditions = rule.get('conditions', [])

        if not conditions:
            return False

        results = []

        for condition in conditions:
            field = condition.get('field')
            condition_predicate = condition.get('predicate')
            value = condition.get('value')

            email_field_value = email.get(field, '')

            if condition_predicate not in cls.SUPPORTED_PREDICATES:
                continue  # Unknown predicate, ignore

            checker = cls.SUPPORTED_PREDICATES[condition_predicate]
            result = checker(email_field_value, value)
            results.append(result)

        if predicate == 'All':
            return all(results)
        elif predicate == 'Any':
            return any(results)
        else:
            return False


class ActionExecutor:
    """Class responsible for executing actions on matched emails."""

    @staticmethod
    def performActions(service, email_id: str, actions: List[str]):
        """
        Perform the specified actions on the email.

        Args:
            service: Authenticated Gmail service.
            email_id (str): ID of the email to act upon.
            actions (List[str]): List of actions to perform.
        """
        for action in actions:
            if action == 'mark_as_read':
                ActionExecutor.markAsRead(service, email_id)
            elif action.startswith('move_to_label:'):
                label = action.split(':', 1)[1]
                ActionExecutor.moveToLabel(service, email_id, label)

    @staticmethod
    def markAsRead(service, email_id: str):
        """Mark the email as read by removing the UNREAD label."""
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    @staticmethod
    def moveToLabel(service, email_id: str, label: str):
        """Move the email to the specified label."""
        # For simplicity assume label already exists
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'addLabelIds': [label]}
        ).execute()


class RuleProcessor:
    """Class responsible for processing emails based on loaded rules."""

    def __init__(self, service, rules: List[Dict]):
        self.service = service
        self.rules = rules

    def processEmails(self, emails: List[Dict]):
        """
        Process a list of emails against all loaded rules.

        Args:
            emails (List[Dict]): List of fetched email dictionaries.
        """
        for email in emails:
            email_id = email.get('id')
            if not email_id:
                continue

            for rule in self.rules:
                if RuleEvaluator.matchRule(rule, email):
                    actions = rule.get('actions', [])
                    ActionExecutor.performActions(self.service, email_id, actions)


if __name__ == '__main__':
    service = authenticateGmail()
    # emails = fetchEmails_from_Db()
    
    