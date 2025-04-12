from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal

class AccountBase(BaseModel):
    name: str
    type: Optional[str] = None # e.g., 'checking', 'savings', 'credit'

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    date: date
    description: Optional[str] = None
    amount: Decimal
    # For OFX specific fields
    transaction_type: Optional[str] = None # e.g., 'DEBIT', 'CREDIT'
    fitid: Optional[str] = None # Financial Institution Transaction ID

class TransactionCreate(TransactionBase):
    account_id: int
    category_id: Optional[int] = None
    reconciled: Optional[bool] = False
    tags: Optional[List[str]] = None
    notes: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    account_id: int
    category_id: Optional[int] = None
    reconciled: bool
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True) 