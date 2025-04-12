import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase URL and Key from environment variables
supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")

# Check if environment variables are set
if not supabase_url or not supabase_key:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

# Initialize Supabase client
try:
    supabase: Client = create_client(supabase_url, supabase_key)
    # Removed print statement for production
    # print("Supabase client initialized successfully.") 
except Exception as e:
    print(f"Error initializing Supabase client: {e}") # Print error if initialization fails
    raise

def get_supabase_client() -> Client:
    """Returns the initialized Supabase client."""
    return supabase 