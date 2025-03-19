document.addEventListener("DOMContentLoaded", function () {
    const observingRunField = document.querySelector("#id_obs_run");
    const researchersField = document.querySelector("#id_researchers");

    if (observingRunField && researchersField) {
        observingRunField.addEventListener("change", function () {
            const observingRunId = observingRunField.value;
            if (!observingRunId) {
                researchersField.innerHTML = "";
                return;
            }

            fetch(`/admin/dwarfs4MOSAIC/tbl_observing_block/get_researchers/?observing_run_id=${observingRunId}`)
                .then(response => response.json())
                .then(data => {
                    researchersField.innerHTML = "";
                    data.forEach(researcher => {
                        let option = new Option(researcher.name, researcher.id);
                        researchersField.appendChild(option);
                    });
                })
                .catch(error => console.error("Error fetching researchers:", error));
        });
    }
});
