from fastapi import FastAPI, status, HTTPException
from model.models import User, UserResponse
from backend.database import get_connection, create_table

create_table()
app = FastAPI()

# -------------------------
# GET all users
# -------------------------

@app.get("/users/")
def read_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, age FROM users")

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "user_id": row[0],
            "name": row[1],
            "age": row[2]
        }
        for row in rows
    ]


# -------------------------
# POST create user
# -------------------------

@app.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create_user(user: User):

    connection =get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "user_id": user_id,
        "name": user.name,
        "age": user.age
    }


# -------------------------
# GET single user
# -------------------------

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, age FROM users WHERE id = ?",
        (user_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": row[0],
        "name": row[1],
        "age": row[2]
    }


# -------------------------
# PUT update user
# -------------------------

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,)
    )

    existing_user = cursor.fetchone()

    if existing_user is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    cursor.execute(
        """
        UPDATE users
        SET name = ?, age = ?
        WHERE id = ?
        """,
        (user.name, user.age, user_id)
    )

    connection.commit()

    connection.close()

    return {
        "user_id": user_id,
        "name": user.name,
        "age": user.age
    }


# -------------------------
# DELETE user
# -------------------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    if deleted_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }


# -------------------------
# Run server
# -------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )