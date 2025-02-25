from ..config import supabase

def get_all_users_bd():
    response = supabase.table("users").select("*").execute()
    return response.data


def get_one_user_bd(id: int):
    response = supabase.table("users").select("*").eq("id", id).execute()
    return None if not response.data else response.data[0]


def get_one_user_by_username_bd(username: str):
    response = supabase.table("users").select("*").eq("username", username).execute()
    return None if not response.data else response.data[0]


def create_user_bd(user_data):
    response = supabase.table("users").insert(user_data.model_dump()).execute()
    return response.data[0]

    
def update_user_bd(user_data, id):
    response = supabase.table("users").update(user_data.model_dump()).eq("id", id).execute()
    return response.data[0]


def delete_user_bd(id):
    response = supabase.table('users').delete().eq('id', id).execute()
    return response.data
