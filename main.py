from ruleEngine import RuleLoader, RuleProcessor
from auth import authenticateGmail
from logger import app_logger as log
from fetchEmail import fetchAndStoreEmails_from_Gmail
from db import createEmailsTable, createHistoriesTable, get_mails_from_db

def main():
    log.info("Starting Application...")
    # Step 1: Load Rules
    rules = RuleLoader.loadRules('rules.json')
    log.debug("Rules Loaded from rules.json")
    # Step 2: Create Tables
    createEmailsTable()
    createHistoriesTable()
    log.debug("Creation of Tables DONE!")
    
    # Step 3: Authenticate Gmail
    log.info("Initiating Authentication - GMAIL-APIs")
    service = authenticateGmail()
    
    # Step 4: Fetch Emails
    log.info("Fetching of Emails Started!")
    fetchAndStoreEmails_from_Gmail(service, max_res=20)  # Limit for safety
    
    # Step 5: Get Emails from database
    log.info("Initiated-Fetching of mails from Database")
    emails = get_mails_from_db()

    # Step 6: Process Emails with Rules
    log.info("Starting RuleProcessor. To process mails")
    processor = RuleProcessor(service, rules)
    processor.processEmails(emails)

    log.info("Rules applied successfully!")
    log.info(">> Application Sucessfully executed! <<")

if __name__ == "__main__":
    # config is implemented in global scope -> act initialize before main
    main() 
