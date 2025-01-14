import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class BankDB:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create the bank table if it doesn't exist, with BankID starting at 100
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bank (
                BankID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                DiscordID TEXT NOT NULL,
                Money NUMERIC NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                MessageID Text PRIMARY KEY NOT NULL,
                DiscordID TEXT NOT NULL,
                Value NUMERIC NOT NULL
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS LastMessage (
                DiscordID TEXT PRIMARY KEY NOT NULL,
                Timestamp DATETIME NOT NULL
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Settings (
                Item TEXT PRIMARY KEY NOT NULL,
                Value TEXT NOT NULL)''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Contracts (
                ContractID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Contractor TEXT NOT NULL,
                Contractee TEXT NOT NULL,
                Amount INTEGER NOT NULL,
                Days INTEGER NOT NULL)''')
        self.connection.commit()

    def add_account(self, discord_id, initial_money=0):
        self.cursor.execute('''SELECT * FROM bank''')
        if self.cursor.fetchall() == []:

            self.cursor.execute('''
            INSERT INTO bank (DiscordID, Money) VALUES (?, ?)
        ''', (os.getenv("ServerID"), initial_money))
            self.cursor.execute('''
                UPDATE SQLITE_SEQUENCE SET seq = 68 WHERE name = "Bank"''')
            self.connection.commit()
        self.cursor.execute('''
            INSERT INTO bank (DiscordID, Money) VALUES (?, ?)
        ''', (discord_id, initial_money))
        self.connection.commit()
        return 0

    def tax_rate(self):
        self.cursor.execute('''SELECT Value FROM Settings Where Item = 'Tax' ''')
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result[0]
    
    def set_tax(self, rate):
        self.cursor.execute('''
            INSERT OR REPLACE INTO Settings (Item, Value)
            VALUES ('Tax',?)''', (rate,))
        self.connection.commit()

    def bonus_rate(self):
        self.cursor.execute('''SELECT Value FROM Settings Where Item = 'Bonus' ''')
        result = self.cursor.fetchone()
        if result is None:
            return 0.001
        return result[0]
    
    def set_bonus(self, rate):
        self.cursor.execute('''
            INSERT OR REPLACE INTO Settings (Item, Value)
            VALUES ('Bonus',?)''', (rate,))
        self.connection.commit()

    def get_balance(self, discord_id):
        # Retrieve the balance for a specific DiscordID
        self.cursor.execute('''
            SELECT Money FROM bank WHERE DiscordID = ?
        ''', (discord_id,))
        result = self.cursor.fetchone()
        return result[0] if result else self.add_account(discord_id)

    def update_balance(self, discord_id, new_balance):
        # Update the balance for a specific DiscordID
        self.cursor.execute('''
            UPDATE bank SET Money = ? WHERE DiscordID = ?
        ''', (new_balance, discord_id))
        self.connection.commit()

    def get_messages(self, discord_id):
        self.cursor.execute('''
            SELECT * FROM Messages WHERE DiscordID = ?''', (discord_id,))
        return len(self.cursor.fetchall())
    
    def update_last_message(self, discord_id):
        self.cursor.execute('''
            INSERT OR REPLACE INTO LastMessage (DiscordID, Timestamp)
            VALUES (?, ?)''', (discord_id, datetime.utcnow()))
        self.connection.commit()
    
    def get_last_message(self, discord_id):
        self.cursor.execute('''
            SELECT Timestamp FROM LastMessage WHERE DiscordID = ?''', (discord_id,))
        result = self.cursor.fetchone()
        if result is None:
            result = datetime.utcnow() - timedelta(seconds=10)
        else:
            result = result[0]
        return str(result)
    
    def delete_message(self, message_id):
        self.cursor.execute('SELECT DiscordID, Value FROM Messages WHERE MessageID = ?', (message_id,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute('DELETE FROM Messages WHERE MessageID = ?', (message_id,))
            self.connection.commit()
            balance = self.get_balance(result[0])
            if balance is None:
                self.add_account(result[0], 0)
                balance = 0
                self.connection.commit()
            self.update_balance(result[0], balance-result[1])


    def contract_add(self, contractor, contractee, amount, days):
        now = datetime.utcnow()
        self.cursor.execute('''INSERT INTO Contracts (Contractor, Contractee, Amount, Days) VALUES (?,?,?,?)''', (contractor,contractee,amount,days))
        self.connection.commit()

    def fulfill_contracts(self):
        self.cursor.execute('''SELECT * FROM Contracts''')
        contracts = self.cursor.fetchall()

        for contract in contracts:
            contract_id = contract[0]
            contractor = contract[1]
            contractee = contract[2]
            Amount = contract[3]
            Days = contract[4] - 1
            if 0 > Days:
                self.cursor.execute('''
                    DELETE FROM Contracts
                    WHERE ContractID = ?''', (contract_id,))
                self.connection.commit()
                continue
            if contractor == os.getenv("ServerID"):
                selfbalance = Amount+1
            else:
                selfbalance = self.get_balance(contractor)
            if selfbalance > Amount:
                if contractor != os.getenv("ServerID"):
                    self.update_balance(contractor,selfbalance-Amount)
                otherbalance = self.get_balance(contractee)
                self.update_balance(contractee, otherbalance+Amount)
                if Days > 0:
                    self.cursor.execute('''
                        UPDATE Contracts
                        SET Days = ?
                        WHERE ContractID = ?''', (Days, contract_id))
                else:
                    self.cursor.execute('''
                        DELETE FROM Contracts
                        WHERE ContractID = ?''', (contract_id,))
                self.connection.commit()

    def list_contracts(self, discord_id):
        self.cursor.execute('''SELECT * FROM Contracts WHERE Contractor = ?''', (discord_id,))
        results = self.cursor.fetchall()
        return results
    
    def delete_contract(self, contract_id):
        self.cursor.execute('''
            DELETE FROM Contracts
            WHERE ContractID = ?''', (contract_id,))
        self.connection.commit()

    def add_message(self, discord_id, message_id, coins):
        self.cursor.execute('''
            INSERT INTO Messages (MessageID, DiscordID, Value) VALUES (?,?,?)''', (message_id, discord_id, coins))
        self.connection.commit()
    
    def event_add(self, discord_id, userCoins, Mastercoins, message):
        balance = self.get_balance(discord_id)
        if balance is None:
            self.add_account(discord_id, 0)
            balance = 0
            self.connection.commit()
        self.add_message(discord_id, message.id, userCoins)
        self.update_balance(discord_id, balance+userCoins)
        balance = self.get_balance(message.guild.id)
        self.update_balance(message.guild.id, balance+Mastercoins)
        self.update_last_message(discord_id)


    def close(self):
        # Close the database connection
        self.connection.close()

# Example usage:
# db = BankDB()
# db.add_account("123456789012345678", 100)
# print(db.get_balance("123456789012345678"))
# db.update_balance("123456789012345678", 200)
# db.close()
