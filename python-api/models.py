from pydantic import BaseModel

class Account(BaseModel):
    address: str

class Project(BaseModel):
    name: str
    description: str
    address_from: str

class FundProject(BaseModel):
    project_id: int
    amount: int
    address_from: str

class Stake(BaseModel):
    amount: int
    duration_days: int
    address_from: str

class UpdateRewardRate(BaseModel):
    new_rate: int
    address_from: str

class DistributeTokens(BaseModel):
    user: str
    amount: int
    address_from: str

class UnlockAccount(BaseModel):
    address: str
    password: str

class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class MintTokens(BaseModel):
    recipient_address: str
    amount: int
    address_from: str

class ExchangeTokensRequest(BaseModel):
    to: str  # Recipient's address
    amount: int  # Amount of tokens to exchange
    address_from: str