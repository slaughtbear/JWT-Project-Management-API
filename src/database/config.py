from dotenv import load_dotenv
import os
from supabase import create_client, Client


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not all ([SUPABASE_URL, SUPABASE_KEY]):
    raise EnvironmentError("No se ha detectado una o más variables de entorno...")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)