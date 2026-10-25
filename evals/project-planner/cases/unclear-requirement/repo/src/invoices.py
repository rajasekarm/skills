def invoices_for(account_id, rows):
    return [row for row in rows if row["account_id"] == account_id]
