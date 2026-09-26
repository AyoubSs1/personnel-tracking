from app.models.employee import Employee
from app.services.employee_service import (
    create_employee,
    get_all_employees,
    get_employee_by_matricule,
    update_employee,
    delete_employee
)


# CREATE
employee = Employee(
    id=None,
    matricule="EMP003",
    nom="Alaoui",
    prenom="Youssef"
)

employee_id = create_employee(employee)

print("Employé créé :", employee_id)


# READ
employees = get_all_employees()

print("\nListe des employés :")

for employee in employees:
    print(
        employee["id"],
        employee["matricule"],
        employee["nom"],
        employee["prenom"]
    )


# READ BY MATRICULE
employee = get_employee_by_matricule("EMP003")

print("\nEmployé recherché :")

if employee:
    print(
        employee["matricule"],
        employee["nom"],
        employee["prenom"]
    )


# UPDATE
update_employee(
    employee_id,
    "EMP003",
    "Alaoui",
    "Yassine"
)

print("\nEmployé modifié.")


# DELETE
delete_employee(employee_id)

print("Employé supprimé.")