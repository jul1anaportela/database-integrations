from pprint import pprint
import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:qWzoIQcFvEGUc2B0@cluster0.erbwoyh.mongodb.net/?retryWrites=true&w=majority")

db = client.bank
collection = db.bank_collection
print(db.bank_collection)

# Definição de info para compor o doc
client_account = {
    "name": "roberta",
    "account_type": "Conta Corrente",
    "agency_number": "143212",
    "cpf": "3458276548"
}

# Preparando para submeter as infos
client_accounts = db.client_accounts
client_id = client_accounts.insert_one(client_account).inserted_id

pprint(db.client_accounts.find_one())

# Bulk inserts
new_client_account = [{
        "name": "juliana",
        "account_type": "Conta Corrente",
        "agency_number": "345323",
        "cpf": "3458273348"},
    {
        "name": "raissa",
        "account_type": "Conta Poupança",
        "agency_number": "345233",
        "cpf": "3458987348"
    }]

# Preparando para submeter as infos
result = client_accounts.insert_many(new_client_account)

# recuperando multiplos documentos
print("\n\nRecuperando info da coleção client_account de maneira ordenada")
for result in client_accounts.find({}).sort("date"):
    pprint(result)

print("\nColeções armazenadas no mongoDB")
collections = db.list_collection_names()

for collection in collections:
    pprint(collection)