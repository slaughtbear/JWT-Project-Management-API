# JWT-Project-Management-API
This is a simple but robust backend developed with FastAPI and Supabase to manage projects and related tasks, including JWT authentication and cibersecurity good practices.

## Characteristics
- JWT authentication.
- CRUD operations.
- Supabase integration.

## Tech stack
- Python 3.12.2
- FastAPI 0.115.8
- Supabase 2.13.0

## Previous requirements
- Python 3.12.2 (or superior).
- Supabase account.

## Installation
### 1. Clone the repository
```

https://github.com/slaughtbear/JWT-Project-Management-API.git

```

### 2. Create a virtual environment
```

python -m venv venv

```

### 3. Activate the virtual environment
#### Linux/MacOS
```

source venv/bin/activate

```

#### Windows
```

venv\Scripts\activate

```

### 4. Install the project requirements
```

pip install -r requirements.txt

```

## Supabase
You need to create an account in Supabase if you don´t already have it one. Then you can follow the next steps.
### 1. Supabase project creation
Enter into your dashboard and create a new project, give it a name and password, then click in "Create a new project" button.
### 2. Create the tables
The next step is create the necessary tables for the project, so move your mouse to the left sidebar and click in "Table editor".
#### Users
- **id** = int8 (primary key).
- **created_at** = timestamptz (autogenereted).


## Environment variables configuration
### 1. Create a `.env` file in the root of the aplication



