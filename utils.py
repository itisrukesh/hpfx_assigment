# utils.py

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
