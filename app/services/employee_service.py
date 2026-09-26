from app.database.connection import get_connection
from app.models.employee import Employee


def create_employee(employee: Employee):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees (matricule, nom, prenom, face_embeddings)
        VALUES (?, ?, ?, ?)
    """, (
        employee.matricule,
        employee.nom,
        employee.prenom,
        employee.face_embeddings
    ))

    conn.commit()

    employee_id = cursor.lastrowid

    conn.close()

    return employee_id


def get_employee_by_id(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id = ?
    """, (employee_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def get_employee_by_matricule(matricule: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE matricule = ?
    """, (matricule,))

    row = cursor.fetchone()

    conn.close()

    return row


def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY nom, prenom
    """)

    employees = cursor.fetchall()

    conn.close()

    return employees


def update_employee(
    employee_id: int,
    matricule: str,
    nom: str,
    prenom: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET matricule = ?,
            nom = ?,
            prenom = ?
        WHERE id = ?
    """, (
        matricule,
        nom,
        prenom,
        employee_id
    ))

    conn.commit()

    conn.close()


def delete_employee(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))

    conn.commit()

    conn.close()