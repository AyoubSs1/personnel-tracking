// ============================================================
// NAVIGATION
// ============================================================

function showSection(sectionId) {

    document
        .querySelectorAll(".section")
        .forEach(section => {

            section.classList.remove("active");

        });


    document
        .getElementById(sectionId)
        .classList.add("active");


    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove("active");

        });


    const buttons =
        document.querySelectorAll(".nav-item");

    const sectionNames = [
        "overview",
        "employees",
        "cameras",
        "history",
        "alerts"
    ];

    const index =
        sectionNames.indexOf(sectionId);

    if (index >= 0) {

        buttons[index]
            .classList.add("active");

    }


    const titles = {

        overview: "Dashboard",
        employees: "Employés",
        cameras: "Caméras",
        history: "Historique",
        alerts: "Alertes"

    };


    document
        .getElementById("page-title")
        .textContent = titles[sectionId];

}


// ============================================================
// API
// ============================================================

async function getData(endpoint) {

    const response =
        await fetch(endpoint);

    if (!response.ok) {

        throw new Error(
            `Erreur API: ${response.status}`
        );

    }

    return response.json();
}


// ============================================================
// STATS
// ============================================================

async function loadStats() {

    const data =
        await getData("/api/stats");


    document
        .getElementById("employees-count")
        .textContent = data.employees;


    document
        .getElementById("cameras-count")
        .textContent = data.cameras;


    document
        .getElementById("detections-count")
        .textContent = data.detections;

}


// ============================================================
// LOCATIONS
// ============================================================

async function loadLocations() {

    const data =
        await getData("/api/locations");


    const table =
        document.getElementById(
            "locations-table"
        );


    table.innerHTML = "";


    data.forEach(employee => {

        const row =
            document.createElement("tr");


        const name =
            `${employee.prenom} ${employee.nom}`;


        row.innerHTML = `

            <td>
                <strong>${name}</strong>
            </td>

            <td>
                ${employee.matricule}
            </td>

            <td>
                ${employee.camera_name || "-"}
            </td>

            <td>
                <span class="location-badge">
                    ${employee.location || "Inconnue"}
                </span>
            </td>

            <td>
                ${employee.date || "-"}
            </td>

            <td>
                ${employee.heure || "-"}
            </td>

        `;


        table.appendChild(row);

    });

}


// ============================================================
// EMPLOYEES
// ============================================================

async function loadEmployees() {

    const data =
        await getData("/api/employees");


    const table =
        document.getElementById(
            "employees-table"
        );


    table.innerHTML = "";


    data.forEach(employee => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                ${employee.id}
            </td>

            <td>
                <strong>
                    ${employee.matricule}
                </strong>
            </td>

            <td>
                ${employee.nom}
            </td>

            <td>
                ${employee.prenom}
            </td>

            <td>
                ${employee.created_at}
            </td>

        `;


        table.appendChild(row);

    });

}


// ============================================================
// CAMERAS
// ============================================================

async function loadCameras() {

    const data =
        await getData("/api/cameras");


    const container =
        document.getElementById(
            "camera-grid"
        );


    container.innerHTML = "";


    data.forEach(camera => {

        const card =
            document.createElement("div");


        card.className =
            "camera-card";


        card.innerHTML = `

            <div class="camera-header">

                <div>

                    <h3>
                        📷 ${camera.camera_name}
                    </h3>

                    <p>
                        ${camera.location}
                    </p>

                </div>

                <span class="camera-status">
                    ● Configurée
                </span>

            </div>


            <p>
                <strong>ID :</strong>
                ${camera.id}
            </p>

            <p>
                <strong>Type :</strong>
                ${camera.source_type}
            </p>

            <p>
                <strong>Source :</strong>
                ${camera.source}
            </p>

        `;


        container.appendChild(card);

    });

}


// ============================================================
// HISTORY
// ============================================================

async function loadHistory() {

    const data =
        await getData("/api/detections");


    const table =
        document.getElementById(
            "history-table"
        );


    table.innerHTML = "";


    data.forEach(detection => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                <strong>
                    ${detection.matricule}
                </strong>
            </td>

            <td>
                ${detection.prenom}
                ${detection.nom}
            </td>

            <td>
                ${detection.camera_name}
            </td>

            <td>
                ${detection.location}
            </td>

            <td>
                ${detection.date}
            </td>

            <td>
                ${detection.heure}
            </td>

        `;


        table.appendChild(row);

    });

}


// ============================================================
// DASHBOARD COMPLET
// ============================================================

async function loadDashboard() {

    try {

        await Promise.all([

            loadStats(),
            loadLocations(),
            loadEmployees(),
            loadCameras(),
            loadHistory()

        ]);


        document
            .getElementById("last-update")
            .textContent =
                "Mis à jour à " +
                new Date()
                    .toLocaleTimeString("fr-FR");


    } catch (error) {

        console.error(
            "Erreur dashboard:",
            error
        );

    }

}


// ============================================================
// INITIALISATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadDashboard();

        // Actualisation automatique
        setInterval(
            loadDashboard,
            5000
        );

    }
);