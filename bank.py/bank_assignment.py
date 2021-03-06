class Bank():
    def __init__(self, bankId, name, location):
        self.bankId = bankId
        self.name = name
        self.location = location
        self.accounts = {}
        self.customers = {}
        self.tellers = {}
        self.loans = {}
    def __str__(self):
        result ='BankId:  ' + str(self.bankId) + '\n'
        result += 'Name:  ' + self.name + '\n'
        result += 'Location: ' + self.location
        return result

    def add_customer(self, customer, teller):
        if self.is_valid_teller(teller):
            customer_id = self.get_unique_id("customer")
            self.customers.update({customer_id:customer})
            return customer_id
        else:
            raise Exception("Unauthorized access")

    def add_account(self, account, teller):
        if self.is_valid_teller(teller):
            self.accounts.update({account.id : account})
        else:
            raise Exception("Unauthorized access")

    def add_teller(self, teller):
        teller.id = self.get_unique_id("teller")
        teller.bank = self
        self.tellers.update({teller.id : teller})

    def add_loan(self, loan, teller):
        if self.is_valid_teller(teller):
            self.loans.update({loan.id : loan})
        else:
            raise Exception("Unauthorized access")

    def is_valid_teller(self, teller):
        if teller.id in self.tellers:
            return True
        return False

    def get_max_id(self, data):
        return max([int(y[len(self.name.lower().replace(" ", '') + "teller"):]) for y in list(data.keys())])

    def get_unique_id(self, qualifier):
        x = 0
        if qualifier.lower() in ["teller", "customer", "loan", "account"]:
            if qualifier.lower() == "teller":
                if not list(self.tellers.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = self.get_max_id(self.tellers)

            elif qualifier.lower() == "customer":
                if not list(self.customers.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = self.get_max_id(self.customers)

            elif qualifier.lower() == "loan":
                if not list(self.loans.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = self.get_max_id(self.loans)

            elif qualifier.lower() == "account":
                if not list(self.accounts.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = self.get_max_id(self.accounts)

            return self.name.lower().replace(" ", '') + qualifier.lower() + str(x)
        else:
            raise Exception("Invalid Qualifier")

    def get_customer(self, id):
        if id in self.customers:
            return self.customers[id]

    def get_account(self, id):
        if self.is_valid_account(id):
            return self.accounts[id]

    def get_loan(self, id):
        if id in self.loans:
            return self.loans[id]

    def update_account(self, account_id, amount):
        if self.is_valid_account(account_id):
            new_amount = self.accounts[account_id].get_account_balance()  +  amount
            self.accounts[account_id].set_account_balance(new_amount)

    def is_valid_account(self, account_id):
        if not account_id:
            raise Exception("Invalid Account")
        if not account_id in self.accounts:
            raise Exception("Invalid Account")
        return True

    def delete_account(self, account_id):
        if self.is_valid_account(account_id):
            del self.accounts[account_id]


class Teller(Bank):
    def __init__(self, name, bank=None):
        self.id = None
        self.name = name
        self.bank = bank
        if self.bank:
            self.bank.add_teller(self)

    def collect_money(self, account_id, amount, qualifier):
        if qualifier == "deposit":
            self.bank.update_account(account_id, amount)

    def open_account(self, customer, account_type, amount):
        if account_type in ["savings", "checking"]:
            customer_id = None
            if not customer.get_account_id():
                customer_id = self.bank.add_customer(customer, self)

            elif not self.bank.get_customer(customer.get_account_id()):
                raise Exception("Customer already with another bank")

            account_id = self.bank.get_unique_id("account")
            if account_type == "savings":
                account = SavingsAccount(account_id, customer.get_account_id(), amount)
                self.bank.add_account(account, self)

            else:
                account = CheckingAccount(account_id, customer.get_account_id(), amount)
                self.bank.add_account(account, self)

            return {"account_id" : account_id, "customer_id":customer_id}


        else:
            raise Exception("Invalid Account type")

    def close_account(self, account_id):
        self.bank.delete_account(account_id)

    def loan_request(self, customer, loan_type, amount):
        pass

    def provide_info(self, customer):
        pass

    def issue_card(self):
        pass


class Customer(Bank):
    def __init__(self, name, address, phone_no):
        self.id = None
        self.name = name
        self.address = address
        self.phone_no = phone_no
        self.account_id = None
        self.balance = None                            
    def general_inquiry(self, teller):
        pass

    def deposit_money(self, teller, account_id, amount):
        teller.collect_money(account_id, amount, "deposit")
        self.balance += amount
        return self.balance

    def withdraw_money(self, teller, account_id, amount):
        pass

    def open_account(self, teller, account_type, initial_amount):
        data = teller.open_account(self, account_type, initial_amount)
        self.account_id = data["account_id"]
        if data["customer_id"]:
            self.id = data["customer_id"]

    def close_account(self, teller, account_id):
        teller.close_account(self.account_id)
        self.account_id = None

    def apply_for_loan(self, teller, loan_type, amount):
        pass

    def request_card(self):
        pass

    def get_account_id(self):
        return self.account_id

    def get_customer_id(self):
        return self.id

class Account():
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.account_balance = amount

    def set_account_balance(self, amount):
        self.account_balance = amount

    def get_account_balance(self):
        return self.account_balance

class CheckingAccount(Account):
    def __init__(self, id, customer_id, amount):
        super().__init__(id, customer_id, amount)

class SavingsAccount(Account):
    def __init__(self, id, customer_id, amount):
        super().__init__(id, customer_id, amount)

class Loan():
    def __init__(self, id, loan_type, customer_id, amount):
        self.id = id
        self.loan_type = loan_type
        self.amount = amount
        self.customer_id = customer_id


Bank1 = Bank(10011,'KKBank','Kampala')
print(Bank1)
x1 = {'Teller 11':10011,
     'Teller 12':10012,
     'Teller 13':10013}
Bank1.tellers.update(x1)
print(Bank1.tellers)

customersA = {
    'customer1' :{'id':'101','Name':'Ali','Adress':'Nja','PhoneNo':'070','AccoNo':'123'},
    'customer2' :{'id':'102','Name':'Alice','Adress':'Njale','PhoneNo':'07012','AccoNo':'1234'},
    'customer3' :{'id':'103','Name':'Allen','Adress':'kp','PhoneNo':'07045','AccoNo':'12334'},
    'customer4' :{'id':'104','Name':'Ian','Adress':'gulu','PhoneNo':'070786','AccoNo':'12399'},
    'customer5' :{'id':'105','Name':'Derrik','Adress':'Talli','PhoneNo':'0701234','AccoNo':'1234567'},
    'customer6' :{'id':'106','Name':'Joy','Adress':'Bungu','PhoneNo':'070456','AccoNo':'1232678'},
    'customer7' :{'id':'107','Name':'Beck','Adress':'tuk','PhoneNo':'0700457','AccoNo':'123987'},
    'customer8' :{'id':'108','Name':'Jame','Adress':'Ngajo','PhoneNo':'0700067','AccoNo':'123912'},
    'customer9' :{'id':'109','Name':'Phil','Adress':'flapo','PhoneNo':'0703457','AccoNo':'1231598'},
    'customer10' :{'id':'1010','Name':'Paul','Adress':'flat','PhoneNo':'0713457','AccoNo':'1234898'}}
    
    
Bank1.customers.update(customersA)
print(Bank1.customers)

Bank2 = Bank(10012,'MMBank','Gulu')
print(Bank2)

x2 ={'Teller 21':10021,
     'Teller 22':10022,
     'Teller 23':10023}

Bank2.tellers.update(x2)
print(Bank2.tellers)



customersB = {
    'customer1' :{'id':'2101','Name':'Alupo','Adress':'Najera','PhoneNo':'070','AccoNo':'22123'},
    'customer2' :{'id':'2102','Name':'Alago','Adress':'Nabweru','PhoneNo':'07348','AccoNo':'221234'},
    'customer3' :{'id':'2103','Name':'Apio','Adress':'Bwaise','PhoneNo':'070645','AccoNo':'2212334'},
    'customer4' :{'id':'2104','Name':'Ivan','Adress':'Lamwo','PhoneNo':'071785','AccoNo':'2212399'},
    'customer5' :{'id':'2105','Name':'Demilo','Adress':'kyebando','PhoneNo':'0702934','AccoNo':'221234567'},
    'customer6' :{'id':'2106','Name':'Joyce','Adress':'Bunga','PhoneNo':'070276','AccoNo':'221232678'},
    'customer7' :{'id':'2107','Name':'Beckam','Adress':'Kavule','PhoneNo':'0774457','AccoNo':'22123987'},
    'customer8' :{'id':'2108','Name':'James','Adress':'Wandegeya','PhoneNo':'0750068','AccoNo':'22123912'},
    'customer9' :{'id':'2109','Name':'Philimon','Adress':'Bukoto','PhoneNo':'0713448','AccoNo':'221231598'},
    'customer10' :{'id':'21010','Name':'Dan','Adress':'Kikoni','PhoneNo':'0703419','AccoNo':'221231598'}}
    
    
    

Bank2.customers.update(customersB)
print(Bank2.customers)







                 





        
