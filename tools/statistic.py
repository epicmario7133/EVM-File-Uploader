import sqlite3

conn = sqlite3.connect('api_requests.db')
cursor = conn.cursor()

query = """
    SELECT contract_address, chain_id, COUNT(*) as count
    FROM api_requests
    GROUP BY contract_address, chain_id
    ORDER BY count DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

for result in results:
    contract_address, chain_id, count = result
    print(f"Contract Address: {contract_address}, Chain ID: {chain_id}, Count: {count}")

conn.close()