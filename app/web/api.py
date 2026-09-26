from flask import Blueprint, jsonify

from app.database.connection import get_connection


api = Blueprint(
    "api",
    __name__
)


# ============================================================
# STATISTIQUES
# ============================================================

@api.route("/stats")
def stats():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT COUNT(*) AS count FROM employees"
        )

        employees = cursor.fetchone()["count"]

        cursor.execute(
            "SELECT COUNT(*) AS count FROM cameras"
        )

        cameras = cursor.fetchone()["count"]

        cursor.execute(
            "SELECT COUNT(*) AS count FROM detections"
        )

        detections = cursor.fetchone()["count"]

        return jsonify({
            "employees": employees,
            "cameras": cameras,
            "detections": detections
        })

    finally:

        conn.close()


# ============================================================
# EMPLOYES
# ============================================================

@api.route("/employees")
def employees():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                matricule,
                nom,
                prenom,
                created_at
            FROM employees
            ORDER BY nom, prenom
            """
        )

        rows = cursor.fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:

        conn.close()


# ============================================================
# DERNIERE LOCALISATION DE CHAQUE EMPLOYE
# ============================================================

@api.route("/locations")
def locations():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                e.id AS employee_id,
                e.matricule,
                e.nom,
                e.prenom,
                c.id AS camera_id,
                c.camera_name,
                c.location,
                d.date,
                d.heure

            FROM employees e

            LEFT JOIN detections d
                ON d.id = (
                    SELECT d2.id
                    FROM detections d2
                    WHERE d2.employee_id = e.id
                    ORDER BY d2.date DESC, d2.heure DESC
                    LIMIT 1
                )

            LEFT JOIN cameras c
                ON c.id = d.camera_id

            ORDER BY e.nom, e.prenom
            """
        )

        rows = cursor.fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:

        conn.close()


# ============================================================
# CAMERAS
# ============================================================

@api.route("/cameras")
def cameras():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                camera_name,
                location,
                source,
                source_type
            FROM cameras
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:

        conn.close()


# ============================================================
# HISTORIQUE DES DETECTIONS
# ============================================================

@api.route("/detections")
def detections():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                e.matricule,
                e.nom,
                e.prenom,
                c.camera_name,
                c.location,
                d.date,
                d.heure

            FROM detections d

            JOIN employees e
                ON e.id = d.employee_id

            JOIN cameras c
                ON c.id = d.camera_id

            ORDER BY d.date DESC, d.heure DESC

            LIMIT 50
            """
        )

        rows = cursor.fetchall()

        return jsonify([
            dict(row)
            for row in rows
        ])

    finally:

        conn.close()