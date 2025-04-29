from ruleEngine import RuleLoader, RuleProcessor
from auth import authenticateGmail
from fetchEmail import fetchAndStoreEmails_from_Gmail
from db import createEmailsTable, createHistoriesTable, get_mails_from_db
# from config import loadConfigs

def main():
    # Load all needed configurations
    # loadConfigs()
    
    # Step 1: Load Rules
    rules = RuleLoader.loadRules('rules.json')
    
    # Step 2: Create Tables
    createEmailsTable()
    createHistoriesTable()
    
    # Step 3: Authenticate Gmail
    service = authenticateGmail()
    
    # Step 4: Fetch Emails
    fetchAndStoreEmails_from_Gmail(service, max_res=20)  # Limit for safety
    
    # Step 5: Get Emails from database
    emails = get_mails_from_db()

    # Step 6: Process Emails with Rules
    processor = RuleProcessor(service, rules)
    processor.processEmails(emails)

    print(">> Rules applied successfully! <<")

if __name__ == "__main__":
    main()
