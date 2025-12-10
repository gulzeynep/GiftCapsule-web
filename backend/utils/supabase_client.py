import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    Initialize and return Supabase client
    """
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')

    if not url or not key:
        raise ValueError('SUPABASE_URL and SUPABASE_KEY must be set in environment variables')

    return create_client(url, key)

# Create a singleton instance
supabase = get_supabase_client()
