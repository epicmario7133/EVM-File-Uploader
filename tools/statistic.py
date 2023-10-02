import sqlite3
import matplotlib.pyplot as plt
from qbstyles import mpl_style
import argparse


parser = argparse.ArgumentParser(description='Api for get file from EVM')
parser.add_argument("-g", "--gui", help="Enable gui False/True", type=str, default="True")
args = parser.parse_args()
gui = args.gui


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

contract_addresses = []
chain_ids = []
counts = []

contract_chain_counts = {}

for result in results:
    contract_address, chain_id, count = result
    contract_addresses.append(contract_address)
    chain_ids.append(chain_id)
    counts.append(count)
    print(f"Contract Address: {contract_address}, Chain ID: {chain_id}, Count: {count}")


    if contract_address in contract_chain_counts:
        contract_chain_counts[contract_address][chain_id] = count
    else:
        contract_chain_counts[contract_address] = {chain_id: count}
mpl_style(True)
plt.figure(figsize=(12, 6))
plt.bar(range(len(counts)), counts, tick_label=[f"{addr} - {chain}" for addr, chain in zip(contract_addresses, chain_ids)])
plt.xlabel('Contract Address - Chain ID')
plt.ylabel('Count')
plt.title('Count of API Requests per Contract and Chain ID')
plt.xticks(rotation=90)
plt.tight_layout()

most_used_chains = {}
for contract, chain_count in contract_chain_counts.items():
    most_used_chain = max(chain_count, key=chain_count.get)
    most_used_chains[contract] = (most_used_chain, chain_count[most_used_chain])

chain_counts = {}

for contract, (chain_id, count) in most_used_chains.items():
    if chain_id in chain_counts:
        chain_counts[chain_id] += count
    else:
        chain_counts[chain_id] = count

largest_slice_index = list(chain_counts.values()).index(max(chain_counts.values()))
explode = [0.1 if i == largest_slice_index else 0 for i in range(len(chain_counts))]

plt.figure(figsize=(10, 6))
plt.pie(chain_counts.values(), labels=[f"Chain {chain_id} ({count})" for chain_id, count in chain_counts.items()], autopct='%1.1f%%', startangle=140, explode=explode)
plt.title('Distribution of Chain ID for the Most Used Contracts.')
plt.axis('equal')
if gui == "True":
    plt.show()

conn.close()