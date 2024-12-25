from fastapi import FastAPI, HTTPException
from models import Account, Project, FundProject, Stake, UpdateRewardRate, DistributeTokens, UnlockAccount, Register, Login
from defi_api import DeFiAPI
from db import register_user, authenticate_user, create_db

app = FastAPI()

api = DeFiAPI()


@app.on_event("startup")
async def startup():
    create_db()
@app.get("/accounts")
async def get_accounts():
    try:
        return api.account()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Register a new user
@app.post("/register")
async def register(user: Register):
    address = register_user(user.username, user.password)
    if not address:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"status": "success", "message": "User registered successfully", "address": address}


# Login a user
@app.post("/login")
async def login(user: Login):
    address = authenticate_user(user.username, user.password)
    if not address:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"status": "success", "message": "User logged in successfully", "address": address}

@app.get("/balance/{address}")
async def get_balance(address: str):
    try:
        balance = api.get_balance(address)
        return {"address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stake")
async def stake(stake_info: Stake):
    try:
        api.stake(stake_info.amount, stake_info.duration_days, stake_info.address_from)
        return {"status": "success", "message": "Staked successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/unstake")
async def unstake(position_id: int, address_from: str):
    try:
        api.unstake(position_id, address_from)
        return {"status": "success", "message": "Unstaked successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_project")
async def create_project(project: Project):
    try:
        api.create_project(project.name, project.description, project.address_from)
        return {"status": "success", "message": "Project created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/fund_project")
async def fund_project(fund_info: FundProject):
    try:
        api.fund_project(fund_info.project_id, fund_info.amount, fund_info.address_from)
        return {"status": "success", "message": "Project funded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_user_positions/{address}")
async def get_user_positions(address: str):
    try:
        positions = api.get_user_positions(address)
        return {"address": address, "positions": positions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_user_projects/{address}")
async def get_user_projects(address: str):
    try:
        projects = api.get_user_projects(address)
        return {"address": address, "projects": projects}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_reward_rate")
async def get_reward_rate():
    return {"reward_rate": api.get_reward_rate()}

@app.post("/update_reward_rate")
async def update_reward_rate(update_info: UpdateRewardRate):
    try:
        api.update_reward_rate(update_info.new_rate, update_info.address_from)
        return {"status": "success", "message": "Reward rate updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/distribute_tokens")
async def distribute_tokens(distribute_info: DistributeTokens):
    try:
        api.distribute_tokens(distribute_info.user, distribute_info.amount, distribute_info.address_from)
        return {"status": "success", "message": "Tokens distributed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/unlock_account")
async def unlock_account(unlock_info: UnlockAccount):
    try:
        api.unlock_account(unlock_info.address, unlock_info.password)
        return {"status": "success", "message": "Account unlocked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_new_user")
async def create_new_user(password: str):
    try:
        new_user_address = api.create_new_user(password)
        return {"status": "success", "address": new_user_address}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
