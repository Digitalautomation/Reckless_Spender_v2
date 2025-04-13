from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# Add path for imports if necessary (usually handled by running from root)
import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from models.categories import Category # Import the model
from core.supabase_client import get_supabase_client
from supabase import Client

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get("/", response_model=List[Category])
def get_categories(supabase: Client = Depends(get_supabase_client)):
    """Fetches a list of all available categories."""
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        # Error handling is via exceptions in supabase-py v2
        return response.data
    except Exception as e:
        print(f"Error fetching categories: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching categories: {e}"
        )

# TODO: Add POST /categories endpoint (for creating custom categories)
# TODO: Add PUT /categories/{id} endpoint?
# TODO: Add DELETE /categories/{id} endpoint? 