from datetime import datetime
from db import TableQuery

def BuildEmailRecord(msg_detail):
    """Build a full email record dictionary matching EMAIL_FIELDS."""
    # Make sure to update/Add new field in email_data if our EMAIL SCHEMA got Changed/Modified.
    headers = msg_detail['payload']['headers']

    # Parse required header fields
    header_map = {h['name'].lower(): h['value'] for h in headers}

    email_data = {
        'id': msg_detail['id'],
        'thread_id': msg_detail['threadId'],
        'sender': header_map.get('from', ''),
        'subject': header_map.get('subject', ''),
        'snippet': msg_detail.get('snippet', ''),
        'received_datetime': header_map.get('date', ''),
        'label_ids': ','.join(msg_detail.get('labelIds', []))
    }

    # Final record tuple matching table field order
    record_tuple = tuple(
        email_data.get(field, None) for field in TableQuery.EMAIL_FIELDS
    )

    return record_tuple

def BuildProcessedHistoryRecord(email_id: str, rule_id: str, actions: list, status):
    """Build a full processed history record dictionary matching RULE_HISTORY_FIELDS."""
    # Make sure to update/Add new field in processed_data if our PROCESSED-HISTORY SCHEMA got Changed/Modified.
    processed_data = {
        'email_id': email_id,
        'rule_id': rule_id,
        'actions_taken': ','.join(actions),
        'status': status,
        'processed_at': datetime.now()
    }
    
    record_tuple = tuple(processed_data.get(field, None) for field in TableQuery.RULE_HISTORY_FIELDS)
    
    return record_tuple