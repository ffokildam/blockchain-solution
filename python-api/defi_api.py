import web3
import json


class DeFiAPI:
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))

    contract_address = web3.Web3.to_checksum_address("0xCBe1376958aDA857fdeC4aD03ff99aC372CA6056")

    with open("abi.txt", "r") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=contract_address, abi=abi)

    def account(self):
        return self.w3.eth.accounts

    def get_balance(self, address):
        address = web3.Web3.to_checksum_address(address)
        return web3.Web3.from_wei(self.w3.eth.get_balance(address), "ether")

    def stake(self, amount, duration_days, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        staking_function = self.contract.functions.stake(amount, duration_days)
        tx = staking_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def unstake(self, position_id, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        unstaking_function = self.contract.functions.unstake(position_id)
        tx = unstaking_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def get_user_positions(self, address):
        address = web3.Web3.to_checksum_address(address)
        return self.contract.functions.getUserPositions(address).call()

    def create_project(self, name, description, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        create_project_function = self.contract.functions.createProject(name, description)
        tx = create_project_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def fund_project(self, project_id, amount, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        fund_project_function = self.contract.functions.fundProject(project_id, amount)
        tx = fund_project_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def get_user_projects(self, address):
        address = web3.Web3.to_checksum_address(address)
        return self.contract.functions.getUserProjects(address).call()

    def get_reward_rate(self):
        return self.contract.functions.rewardRatePerDay().call()

    def update_reward_rate(self, new_rate, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        update_rate_function = self.contract.functions.updateRewardRate(new_rate)
        tx = update_rate_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def distribute_tokens(self, user, amount, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)
        distribute_tokens_function = self.contract.functions.distributeTokens(user, amount)
        tx = distribute_tokens_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def unlock_account(self, address, password):
        self.w3.geth.personal.unlock_account(address, password, 0)

    def create_new_user(self, password):
        return self.w3.geth.personal.new_account(password)

    def balance_of(self, address):
        address = web3.Web3.to_checksum_address(address)
        balance = self.contract.functions.balanceOf(address).call()
        return balance

    def mint_tokens(self, to, amount, address_from):
        address_from = web3.Web3.to_checksum_address(address_from)

        admin_address = self.contract.functions.getAdmin().call()
        if address_from != admin_address:
            raise Exception("Only admin can mint tokens.")

        mint_tokens_function = self.contract.functions.mintTokens(to, amount)

        try:
            tx = mint_tokens_function.transact({"from": address_from})
            self.w3.eth.wait_for_transaction_receipt(tx)
            print(f"Minted {amount} tokens to {to}")
        except Exception as e:
            print(f"Error minting tokens: {e}")

# Примеры использования
# api = DeFiAPI()
# print(api.balance_of("0xDC3F826D35fA315799966ee645a0f48bBf6901E6"))
#
# api.mint_tokens("0xDC3F826D35fA315799966ee645a0f48bBf6901E6", 10000, "0xDC3F826D35fA315799966ee645a0f48bBf6901E6")
# new_address = api.create_new_user("myStrongPassword123")
#print(f"New account created: {new_address}")

#api = DeFiAPI()
#api.unlock_account("0xDC3F826D35fA315799966ee645a0f48bBf6901E6","3612")
#user0 = api.account()[0]
#balance = api.get_balance(user0)
#print(f"Balance of {user0}: {balance} ETH")
#api.stake(10, 30, user0)  # 1 token for 30 days

#api.unstake(1, user0)

#api.create_project("My Project", "My Project", user0)

#api.fund_project(1, 10, user0)  # Fund with 5 ETH

#print(api.get_user_positions(user0))

# print(api.get_user_projects(user0))

# api.update_reward_rate(200, user0)

# api.distribute_tokens(user0, 10000, user0)