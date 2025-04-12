import asyncio
import os
import sys
from pathlib import Path

# --- Path Setup ---
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).resolve().parent
# Get the project root directory (one level up from script dir)
PROJECT_ROOT = SCRIPT_DIR.parent
# Get the path to the backend directory
BACKEND_DIR = PROJECT_ROOT / "backend"

# Add backend directory to sys.path to allow imports
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR)) # Insert at beginning to prioritize

# --- Imports (after path setup) ---
# Import the parser function (this will also initialize the real Supabase client)
try:
    # Now imports should work relative to the backend directory
    from services.ofx_parser import parse_ofx
except Exception as e:
    print(f"Error importing parse_ofx. Ensure Supabase client initialized correctly.")
    print(f"Check if backend/.env file exists and has credentials.")
    print(f"Import Error: {e}")
    sys.exit(1)

# --- Configuration ---
# Choose which test file to use for the real upload test
TEST_FILE_NAME = "test2.ofx"
# Path is now relative to BACKEND_DIR/tests
TEST_FILE_PATH = BACKEND_DIR / "tests" / TEST_FILE_NAME
# --- End Configuration ---

async def main():
    """Reads an OFX file and processes it using the real service and Supabase client."""
    print(f"--- Starting Real OFX Processing Test --- ")
    print(f"Attempting to process file: {TEST_FILE_PATH}")

    if not TEST_FILE_PATH.is_file():
        print(f"Error: Test file not found at {TEST_FILE_PATH}")
        return

    try:
        # Read file content as bytes
        print("Reading OFX file content...")
        file_content = TEST_FILE_PATH.read_bytes()
        print(f"Read {len(file_content)} bytes.")

        # Call the parser function (uses the real Supabase client)
        print("Calling parse_ofx service...")
        # parse_ofx is declared async, so we need to await it here
        created_accounts, collected_transactions = await parse_ofx(file_content)

        print("--- Results --- ")
        print(f"Service reported {len(created_accounts)} accounts created/found.")
        if created_accounts:
            print(f"First created/found account details: {created_accounts[0]}")

        print(f"Service collected {len(collected_transactions)} transactions for insertion.")
        if collected_transactions:
            print(f"First collected transaction details: {collected_transactions[0]}")

        print("\nSUCCESS: Processing finished.")
        print("Please check your Supabase dashboard (Table Editor -> accounts, transactions) to verify the data.")

    except ImportError as e:
        print(f"Import Error during execution: {e}")
        print("This might happen if the script is run from the wrong directory or venv isn't active.")
    except Exception as e:
        print(f"\nERROR: An error occurred during processing: {e}")
        import traceback
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    # Check if parse_ofx was imported correctly before running
    if 'parse_ofx' in locals() or 'parse_ofx' in globals():
        print("Running asyncio main function...")
        # Need asyncio.run() because main() is async (as it calls await parse_ofx)
        asyncio.run(main())
    else:
        print("Could not run main function due to import errors.") 