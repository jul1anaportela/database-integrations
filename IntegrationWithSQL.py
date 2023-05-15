import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy.orm import Session


Base = declarative_base()

class Client(Base):
    __tablename__ = "client_info"
    #atributos
    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    cpf = Column(String(9), nullable=False)
    address = Column(String(9), nullable=False)
    
    account = relationship(
        "BankAccount", back_populates="client"
    )
    
    
    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"


class BankAccount(Base):
    __tablename__ = "bank_account"
    #atributos
    id = Column(Integer, primary_key=True)
    account_type = Column(String, nullable=False)
    agency_number = Column(String, nullable=False)
    account_number = Column(Integer, nullable=False)
    account_balance = Column(Float, nullable=False)
    client_id = Column(Integer, ForeignKey("client_info.id"), nullable=False)
    
    client = relationship(
        "Client", back_populates="account"
    )
    
    
    def __repr__(self):
        return f"BankAcount(id={self.id}, account_type={self.account_type}, account_number={self.account_number},account_balance={self.account_balance}), client_id={self.client_id}"
    

print(Client.__tablename__)   
print(BankAccount.__tablename__)

# Conexao com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investigando o esquema do banco de dados
inspector_engine = inspect(engine)
print("\nVerificando se as tabelas existem:")
print(inspector_engine.has_table("client_info"))
print(inspector_engine.has_table("bank_account"))
print("\nPegando os nomes das tabelas:")
print(inspector_engine.get_table_names())
print("\nPegando o nome default do esquema:")
print(inspector_engine.default_schema_name)


with Session(engine) as session:
    juliana = Client(
        name='juliana',
        cpf='123456789',
        address='rua 5, parque vitoria'
    )
    
    raissa = Client(
        name='raissa',
        cpf='345678912',
        address='rua 9, cidade operaria'
    )
    
    # Enviando para o BD (persistência de dados)
    session.add_all([juliana, raissa])
    
    session.commit()
    
stmt_Client = select(Client).where(Client.name.in_(['juliana', 'raissa']))
print("\nRecuperando usuarios a partir de condição de filtragem:")
for client in session.scalars(stmt_Client):
    print(client)


with Session(engine) as session:
    juliana_account = BankAccount(
        account_type='Conta Corrente',
        agency_number='356743',
        account_number= 1222,
        account_balance= 0,
        client_id=1
    )
    
    raissa_account = BankAccount(
        account_type='Conta Poupança',
        agency_number='351243',
        account_number= 1332,
        account_balance= 300,
        client_id=2
    )
    
    # Enviando para o BD (persistência de dados)
    session.add_all([juliana_account, raissa_account])
    
    session.commit()

stmt_BankAccount = select(BankAccount).where(BankAccount.client_id.in_([1, 2]))
print("\nRecuperando usuarios a partir de condição de filtragem:")
for client in session.scalars(stmt_BankAccount):
    print(client)

stmt_join = select(Client. name, BankAccount.account_type).join_from(BankAccount, Client)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

print("\nMostrando como foi feita a busca:")
print(f"{select(Client. name, BankAccount.account_type).join_from(BankAccount, Client)}")

# Aqui realmente mostra o join
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection:")
for result in results:
    print(result)
