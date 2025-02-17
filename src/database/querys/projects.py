from ..config import supabase

def get_one_project(id: int):
    response = supabase.table("projects").select("id").eq("id", id).execute()
    return response.data