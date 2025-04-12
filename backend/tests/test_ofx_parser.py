import pytest
import os
import sys
from unittest.mock import patch, AsyncMock, MagicMock, ANY
from decimal import Decimal
from datetime import date

# Ensure the services and models directories are importable by adding the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import after potentially modifying sys.path
from services.ofx_parser import parse_ofx
from models.financials import Account, AccountCreate, TransactionCreate

# Define the paths to the test OFX files relative to the tests directory
TEST_FILES_DIR = os.path.dirname(__file__)
TEST_OFX_FILES = [
    os.path.join(TEST_FILES_DIR, "test1.ofx"),
    os.path.join(TEST_FILES_DIR, "test2.ofx"),
]

# Helper function to create a mock Supabase response object
def create_mock_response(data=None, error=None, count=None):
    mock = MagicMock()
    mock.data = data
    mock.error = error
    mock.count = count
    return mock

@pytest.mark.asyncio
@pytest.mark.parametrize("ofx_file_path", TEST_OFX_FILES)
async def test_parse_ofx_success(ofx_file_path):
    """Tests successful parsing of different OFX files using mocks."""
    # Check if the test file exists before trying to open it
    if not os.path.exists(ofx_file_path):
        pytest.skip(f"Test file not found: {ofx_file_path}")

    # Read the OFX file content as bytes
    with open(ofx_file_path, 'rb') as f:
        ofx_content = f.read()

    # --- Set up Mocks for Supabase Interaction ---
    # Mock the client instance returned by get_supabase_client
    mock_supabase_client = MagicMock() # Use MagicMock for the client itself if its methods aren't directly awaited

    # Mock the chainable methods
    mock_table_method = MagicMock()
    mock_select_method = MagicMock()
    mock_eq_method = MagicMock()
    mock_insert_method = MagicMock()

    # Configure the synchronous chain: client.table().select().eq()
    mock_supabase_client.table.return_value = mock_table_method
    mock_table_method.select.return_value = mock_select_method
    mock_select_method.eq.return_value = mock_eq_method

    # Configure the insert chain: client.table().insert()
    mock_table_method.insert.return_value = mock_insert_method

    # Configure the final .execute() calls to be SYNCHRONOUS mocks
    # because the code in parse_ofx calls them synchronously now
    mock_eq_method.execute = MagicMock(return_value=create_mock_response(data=[]))
    mock_insert_method.execute = MagicMock(
        side_effect=[
            # Response for creating the first (and possibly only) account
            create_mock_response(data=[{'id': 1, 'name': 'Mock Account 1 from OFX', 'type': 'checking'}]),
            # Response for inserting the batch of transactions
            create_mock_response(data=[{'id': 101}, {'id': 102}])
        ]
    )

    # --- Execute Test --- 
    # Pass the mock client directly into the function, no patch needed
    parsed_accounts, parsed_transactions = await parse_ofx(
        ofx_content,
        supabase_client=mock_supabase_client
    )

    # --- Assertions ---
    # Verify that Supabase methods were called as expected
    # Check that we looked up accounts and inserted into accounts/transactions
    mock_supabase_client.table.assert_any_call("accounts")
    mock_supabase_client.table.assert_any_call("transactions")
    mock_eq_method.execute.assert_called() # Check account lookup happened
    mock_insert_method.execute.assert_called() # Check insert happened

    # --- Basic Validation of Parsed Data ---
    # Print results for inspection (useful for debugging)
    print(f"\n--- Test Results for {os.path.basename(ofx_file_path)} ---")
    print(f"Parsed/Created {len(parsed_accounts)} accounts.")
    print(f"Collected {len(parsed_transactions)} transactions for potential insertion.")

    # Check the types of the returned lists
    assert isinstance(parsed_accounts, list)
    assert isinstance(parsed_transactions, list)

    # Validate content if data was parsed/created
    if parsed_accounts:
        # Check that the list contains Account objects (since we get ID back)
        assert all(isinstance(acc, Account) for acc in parsed_accounts)
        # Example check based on mock data (uncomment/adapt if needed)
        # assert parsed_accounts[0].id == 1 # Check the ID from the mock
        # assert parsed_accounts[0].name == 'Mock Account 1 from OFX'
        print(f"First Created Account (Data from Mock): {parsed_accounts[0].model_dump()}")

    if parsed_transactions:
        # Check that the list contains TransactionCreate objects
        assert all(isinstance(trx, TransactionCreate) for trx in parsed_transactions)
        # Check data types within the first transaction
        assert isinstance(parsed_transactions[0].date, date)
        assert isinstance(parsed_transactions[0].amount, Decimal)
        assert isinstance(parsed_transactions[0].account_id, int)
        # Check that the account_id corresponds to a created account (using mock id 1 here)
        assert parsed_transactions[0].account_id == 1
        print(f"First Collected Transaction: {parsed_transactions[0].model_dump()}")

# TODO: Add tests for error handling (e.g., corrupted file, Supabase errors)
# TODO: Add tests where account already exists (mock_eq_method.execute returns data)