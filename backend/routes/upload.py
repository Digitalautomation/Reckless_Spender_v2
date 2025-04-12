from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import Dict, List

# Import the OFX parsing service
import sys
from pathlib import Path

# Add backend directory to sys.path if needed (though usually handled by FastAPI structure/running from root)
# This ensures services can be found if running script directly, but might not be needed for standard FastAPI run
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

try:
    from services.ofx_parser import parse_ofx
except ImportError as e:
    print(f"Error importing services: {e}. Check PYTHONPATH or structure.")
    # Handle case where service cannot be imported - maybe raise config error?
    # For now, allow router creation but endpoint will fail if service missing.
    parse_ofx = None 

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

@router.post("/ofx", status_code=status.HTTP_201_CREATED)
async def upload_ofx_file(file: UploadFile = File(...)):
    """Receives an OFX file, parses it, and stores the data."""
    
    if not parse_ofx:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OFX parsing service not available due to import error."
        )

    # Basic validation: Check file extension and content type
    if not file.filename.lower().endswith('.ofx'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .ofx files are accepted."
        )
    # You might want more robust content type validation depending on client behavior
    # print(f"Received file: {file.filename}, content type: {file.content_type}")

    try:
        # Read file content as bytes
        contents = await file.read()
        
        # Call the parsing service
        # Assuming parse_ofx handles potential errors internally and might raise them
        # We pass None for the client, so it uses the default initialized one
        created_accounts, collected_transactions = await parse_ofx(contents, supabase_client=None)
        
        return {
            "filename": file.filename,
            "message": "OFX file processed successfully.",
            "accounts_processed": len(created_accounts),
            "transactions_collected": len(collected_transactions)
        }

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        # Handle errors during file reading or parsing
        # Log the error for debugging purposes
        print(f"Error processing file {file.filename}: {e}") 
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the file: {e}"
        )
    finally:
        # Ensure the file is closed
        await file.close() 