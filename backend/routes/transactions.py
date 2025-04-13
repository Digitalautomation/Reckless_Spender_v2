from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from decimal import Decimal
from datetime import date

# Use Path for relative imports if needed, though direct should work
import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from models.financials import Transaction, TransactionFilterParams, TransactionUpdate # Import models and Update model
from core.supabase_client import get_supabase_client # Import Supabase client getter
from supabase import Client # Import Client type hint

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

@router.get("/", response_model=List[Transaction]) # Return a list of Transaction models
def get_transactions(
    # Use Depends for Pydantic query model validation
    # params: TransactionFilterParams = Depends(),
    # --- OR Define query params directly for simplicity now ---
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    account_id: Optional[int] = Query(None, description="Filter by account ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    reconciled: Optional[bool] = Query(None, description="Filter by reconciled status"),
    limit: int = Query(100, description="Maximum number of transactions to return", ge=1, le=1000),
    offset: int = Query(0, description="Number of transactions to skip (for pagination)", ge=0),
    # --- End direct query params ---
    supabase: Client = Depends(get_supabase_client) # Dependency inject the client
):
    """Fetches a list of transactions with optional filtering and pagination."""
    try:
        query = supabase.table("transactions").select("*") # Select all columns for now

        # Apply filters based on query parameters
        if start_date:
            query = query.gte('date', start_date.isoformat())
        if end_date:
            query = query.lte('date', end_date.isoformat())
        if account_id is not None:
            query = query.eq('account_id', account_id)
        if category_id is not None:
            query = query.eq('category_id', category_id)
        if reconciled is not None:
            query = query.eq('reconciled', reconciled)

        # Apply pagination
        query = query.range(offset, offset + limit - 1) # Supabase range is inclusive
        
        # Apply sorting (e.g., newest first by default)
        query = query.order('date', desc=True).order('id', desc=True)

        # Execute the query
        response = query.execute()

        # Check for errors (handled by exceptions in v2)
        # if response.error:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(response.error))

        # Pydantic will automatically validate the response data against List[Transaction]
        # Convert Decimal strings back if needed (Pydantic V2 usually handles this)
        # transactions_data = response.data
        # for t in transactions_data:
        #     if isinstance(t.get('amount'), str):
        #         t['amount'] = Decimal(t['amount'])
        
        return response.data

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching transactions: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching transactions: {e}"
        )

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    update_data: TransactionUpdate, # Use the new Pydantic model for the request body
    supabase: Client = Depends(get_supabase_client)
):
    """Updates specific fields of a transaction by its ID."""
    
    # Convert the Pydantic model to a dictionary
    # exclude_unset=True ensures we only update fields that were actually sent
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Check if there is anything to update
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided."
        )

    # TODO: Add validation?
    # - Check if category_id exists in the categories table?
    # - Validate tags format?

    try:
        # Perform the update operation in Supabase
        response = supabase.table("transactions")\
                           .update(update_dict)\
                           .eq('id', transaction_id)\
                           .execute()

        # Check if the update was successful and if any row was updated
        if response.data:
            # Return the updated transaction data (first element in the data list)
            return response.data[0]
        else:
            # Handle cases where the transaction_id doesn't exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with id {transaction_id} not found."
            )
    
    except HTTPException as http_exc:
        # Re-raise HTTPException directly so FastAPI handles it
        raise http_exc
    except Exception as e:
        # Log the error for debugging
        print(f"Error updating transaction {transaction_id}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating transaction {transaction_id}: {e}"
        )

# TODO: Add POST /transactions/split endpoint (optional) 