import web3
import json


class DeFiAPI:
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))

    contract_address = web3.Web3.to_checksum_address("0xCEB2d148D4127882b0b0d4bC93a535908F26eDF0")

    with open("abi.txt", "r") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=contract_address, abi=abi)

    def account(self):
        """Returns a list of accounts from the connected web3 provider."""
        return self.w3.eth.accounts

    def get_balance(self, address):
        """Returns the balance in ether for a given address."""
        address = web3.Web3.to_checksum_address(address)
        return web3.Web3.from_wei(self.w3.eth.get_balance(address), "ether")

    def stake(self, amount, duration_days, address_from):
        """Allows a user to stake tokens in the contract."""
        address_from = web3.Web3.to_checksum_address(address_from)
        staking_function = self.contract.functions.stake(amount, duration_days)
        tx = staking_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def unstake(self, position_id, address_from):
        """Allows a user to unstake tokens from a given position."""
        address_from = web3.Web3.to_checksum_address(address_from)
        unstaking_function = self.contract.functions.unstake(position_id)
        tx = unstaking_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def get_user_positions(self, address):
        """Returns a list of staking positions for a given user."""
        address = web3.Web3.to_checksum_address(address)
        return self.contract.functions.getUserPositions(address).call()

    def create_project(self, name, description, address_from):
        """Allows a user to create a new project."""
        address_from = web3.Web3.to_checksum_address(address_from)
        create_project_function = self.contract.functions.createProject(name, description)
        tx = create_project_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def fund_project(self, project_id, amount, address_from):
        """Allows a user to fund a project."""
        address_from = web3.Web3.to_checksum_address(address_from)
        fund_project_function = self.contract.functions.fundProject(project_id, amount)
        tx = fund_project_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def get_user_projects(self, address):
        """Returns a list of projects created by a user."""
        address = web3.Web3.to_checksum_address(address)
        return self.contract.functions.getUserProjects(address).call()

    def get_reward_rate(self):
        """Returns the current reward rate per day."""
        return self.contract.functions.rewardRatePerDay().call()

    def update_reward_rate(self, new_rate, address_from):
        """Allows the admin to update the reward rate."""
        address_from = web3.Web3.to_checksum_address(address_from)
        update_rate_function = self.contract.functions.updateRewardRate(new_rate)
        tx = update_rate_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def distribute_tokens(self, user, amount, address_from):
        """Allows the admin to distribute tokens to a user."""
        address_from = web3.Web3.to_checksum_address(address_from)
        distribute_tokens_function = self.contract.functions.distributeTokens(user, amount)
        tx = distribute_tokens_function.transact({"from": address_from})
        self.w3.eth.wait_for_transaction_receipt(tx)

    def unlock_account(self, address, password):
        """Unlocks a specific account."""
        self.w3.geth.personal.unlock_account(address, password, 0)

    def create_new_user(self, password):
        """Creates a new user account using personal.newAccount."""
        return self.w3.geth.personal.new_account(password)


# Example usage
#api = DeFiAPI()

# Creating a new account with password
#new_address = api.create_new_user("myStrongPassword123")
#print(f"New account created: {new_address}")

# Example usage
#api = DeFiAPI()
#api.unlock_account("0xDC3F826D35fA315799966ee645a0f48bBf6901E6","3612")
# Getting balance of an account
#user0 = api.account()[0]
#balance = api.get_balance(user0)
#print(f"Balance of {user0}: {balance} ETH")
#api.stake(10, 30, user0)  # 1 token for 30 days

# Unstaking tokens
#api.unstake(1, user0)

# Creating a project
#api.create_project("My Project", "Description of the project", user0)

# Funding a project
#api.fund_project(1, 10, user0)  # Fund with 5 ETH

# Get user positions
#print(api.get_user_positions(user0))

# Get user projects
# print(api.get_user_projects(user0))

# Update reward rate
# api.update_reward_rate(200, user0)

# Distribute tokens to a user
# api.distribute_tokens(user0, 1000000000000000000, user0)  # Distribute 1 token