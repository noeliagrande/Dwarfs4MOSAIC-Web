
document.addEventListener('DOMContentLoaded', function() {
    // Get the select for observing_run
    const runSelect = document.getElementById('id_obs_run');
    const filterSelect = document.getElementById('id_filters');
    const configSelect = document.getElementById('id_configuration');

    if (!runSelect || !filterSelect || !configSelect) {
        return; // safety check
    }

    function updateInstrumentChoices(runId) {

        // Clean current filter/configuration options
        filterSelect.innerHTML = '<option value="">---------</option>';
        configSelect.innerHTML = '<option value="">---------</option>';

        if (!runId) return; // no run selected

        // Fetch instrument data for this run (use the correct URL!)
        fetch(`/ajax/get-instrument-choices/?observing_run=${runId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Add filters dynamically
                // data = { filters: [...], configuration: [...] }
                if (data.filters && Array.isArray(data.filters)) {
                    data.filters.forEach(f => {
                        const option = document.createElement('option');
                        option.value = f;
                        option.textContent = f;
                        filterSelect.appendChild(option);
                    });
                }

                // Add configurations dynamically
                if (data.configuration && Array.isArray(data.configuration)) {
                    data.configuration.forEach(c => {
                        const option = document.createElement('option');
                        option.value = c;
                        option.textContent = c;
                        configSelect.appendChild(option);
                    });
                }
            })
            .catch(error => console.error("Error fetching instrument data:", error));
    }

    // When the observing_run changes
    runSelect.addEventListener('change', function() {
        const selectedRunId = this.value;
        updateInstrumentChoices(selectedRunId);
    });

});
