import io
from typing import List, Tuple, Dict, Any
from ofxparse import OfxParser
from datetime import datetime, date
from decimal import Decimal

from models.financials import Account, AccountCreate, TransactionCreate
from core.supabase_client import get_supabase_client
from supabase import Client

async def parse_ofx(file_content: bytes, supabase_client: Client = None) -> Tuple[List[Account], List[TransactionCreate]]:
    """Parses OFX file content and returns lists of created Account objects and collected TransactionCreate objects."""
    # Use provided client or get default
    supabase = supabase_client or get_supabase_client()
    
    accounts_data = []
    transactions_data = []
    account_name_to_id_map = {}

    try:
        ofx = OfxParser.parse(io.BytesIO(file_content))

        print(f"Parsed OFX file. Found {len(ofx.accounts)} accounts.")

        for account in ofx.accounts:
            # --- Account Handling ---
            # Construct account name robustly, handling missing institution details
            org_name = "Unknown Institution"
            if account.institution and account.institution.organization:
                org_name = account.institution.organization
            elif account.institution and account.institution.fid:
                org_name = f"Institution FID: {account.institution.fid}" # Use FID if org name is missing

            account_name = f"{org_name} - {account.account_id} ({account.account_type.upper()})"
            print(f"Processing account: {account_name}")

            # Check if account already exists in Supabase by name
            # Note: supabase-py v2 .execute() is not awaited directly
            existing_account_response = supabase.table("accounts").select("id").eq("name", account_name).execute()
            
            account_id = None
            if existing_account_response.data:
                account_id = existing_account_response.data[0]['id']
                print(f"Account '{account_name}' already exists with ID: {account_id}")
            else:
                # Create Account in Supabase if not exists
                # Validate account type before creating
                raw_account_type = account.account_type.lower().strip() if account.account_type else None
                valid_account_types = {'checking', 'savings', 'credit'}
                final_account_type = raw_account_type if raw_account_type in valid_account_types else None # Default to None if invalid/empty
                
                account_to_create = AccountCreate(name=account_name, type=final_account_type)
                print(f"Creating new account: {account_to_create}")
                # Note: supabase-py v2 .execute() is not awaited directly
                created_account_response = supabase.table("accounts").insert(account_to_create.model_dump()).execute()
                
                if created_account_response.data:
                    account_id = created_account_response.data[0]['id']
                    print(f"Successfully created account '{account_name}' with ID: {account_id}")
                    accounts_data.append(Account(**created_account_response.data[0])) # Add to return list
                else:
                    print(f"Error creating account: {account_name}. Response: {created_account_response.error}")
                    # Optionally raise an error or handle differently
                    continue # Skip transactions for this account if creation failed
            
            if account_id:
                account_name_to_id_map[account_name] = account_id

                # --- Transaction Handling --- 
                statement = account.statement
                if statement and statement.transactions:
                    print(f"Processing {len(statement.transactions)} transactions for account ID: {account_id}")
                    for transaction in statement.transactions:
                        # Ensure description exists, use memo if payee is None
                        description = transaction.payee if transaction.payee else transaction.memo
                        if not description:
                            description = "N/A" # Provide a default if both are missing

                        transaction_to_add = TransactionCreate(
                            account_id=account_id,
                            date=transaction.date.date(), # Get date part only
                            description=description,
                            amount=Decimal(str(transaction.amount)), # Convert amount to Decimal
                            transaction_type=transaction.type,
                            fitid=transaction.id,
                            # Initialize other fields as needed, e.g., category_id=None
                        )
                        transactions_data.append(transaction_to_add)
                else:
                    print(f"No transactions found for account ID: {account_id}")
            else:
                print(f"Skipping transactions for account {account_name} due to missing account ID.")

        # --- Persist Transactions --- 
        if transactions_data:
            print(f"Collected {len(transactions_data)} transactions. Checking for existing fitids...")

            # Get all existing fitids for the accounts processed in this file
            account_ids_in_file = list(account_name_to_id_map.values())
            existing_fitids = set()
            if account_ids_in_file:
                fitid_check_response = supabase.table("transactions").select("fitid, account_id").in_("account_id", account_ids_in_file).execute()
                if fitid_check_response.data:
                    for row in fitid_check_response.data:
                        # Create a unique identifier tuple (account_id, fitid)
                        existing_fitids.add((row['account_id'], row['fitid']))
                # Remove the check for .error, as exceptions handle errors
                # elif fitid_check_response.error:
                #    print(f"Warning: Could not check existing fitids - {fitid_check_response.error}")
            
            print(f"Found {len(existing_fitids)} existing transaction fitids for these accounts.")

            # Filter out transactions that already exist
            transactions_to_insert_models = [
                t for t in transactions_data 
                if (t.account_id, t.fitid) not in existing_fitids
            ]

            if not transactions_to_insert_models:
                print("No new transactions to insert after checking for duplicates.")
                # Ensure we return the original collected transactions, even if none are inserted
                return accounts_data, transactions_data 

            print(f"Attempting to insert {len(transactions_to_insert_models)} new transactions...")
            
            # Convert Pydantic models to dictionaries for insertion
            transactions_to_insert_dicts = [t.model_dump() for t in transactions_to_insert_models]
            
            # Convert Decimal and date for JSON serialization 
            for t_dict in transactions_to_insert_dicts:
                t_dict['amount'] = str(t_dict['amount']) 
                if isinstance(t_dict.get('date'), date):
                     t_dict['date'] = t_dict['date'].isoformat()

            # Perform the batch insert for new transactions only
            insert_response = supabase.table("transactions").insert(transactions_to_insert_dicts).execute()
            
            if insert_response.data:
                print(f"Successfully inserted {len(insert_response.data)} transactions.")
            else:
                print(f"Error inserting transactions: {insert_response.error}")
                # Optionally raise an error

        # Return original collected data, regardless of insertion success/filtering
        return accounts_data, transactions_data 

    except Exception as e:
        print(f"Error parsing OFX file: {e}")
        # Log the exception traceback for debugging
        import traceback
        traceback.print_exc()
        raise # Re-raise the exception to be handled by the caller 