// Replace Variables
//   SERVICE_URL
//   PROJECT_UID
var service_url = 'SERVICE_URL'
var project_uid = 'PROJECT_UID'

async function filterResources() {
    console.log('Filtering resources for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/resource?" + params;
    console.log('url' + url);

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);
    return data;
}

async function filterProcesses() {
    console.log('Filtering processes for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/process?" + params;
    console.log('url' + url);

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);
    return data;
}

async function filterWorkflows() {
    console.log('Filtering workflows for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/workflow?" + params;
    console.log('url' + url);

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);
    return data;
}

async function populateResourceTable() {
    console.log('Populating Resource table');

    // DIV
    console.log('Clearing Resource table...');
    var table_div = document.getElementById('resources-table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    table_element.style.width = '100%';
    table_element.style.height = '100%';
    table_element.style.border = '5px solid black';

    // HEADER
    var resources_table_header = document.createElement('thead');
    resources_table_header.innerHTML = '<tr><th>Index</th><th>Name</th></tr>';
    resources_table_header.style.width = '100%';
    resources_table_header.style.fontWeight = 'bold';
    resources_table_header.style.padding = '5px';
    table_element.appendChild(resources_table_header);

    // BODY
    var resources_table_body = document.createElement('tbody');

    const resources_response = await filterResources();
    for(var i = 0; i < resources_response.resources.length; i++) {
        var resources_table_row = document.createElement('tr');

        // Index
        var resources_table_item = document.createElement('td');
        resources_table_item.style.padding = '1px 25px';
        // resources_table_item.style.width = '10px';
        resources_table_item.innerHTML = i;
        resources_table_row.appendChild(resources_table_item);

        // Resource Name
        var resources_table_item = document.createElement('td');
        resources_table_item.style.padding = '1px 25px';
        resources_table_item.innerHTML = resources_response.resources[i].name;
        resources_table_row.appendChild(resources_table_item);

        // Additional Formatting
        if(i % 2 == 0) {
            resources_table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            resources_table_row.style.backgroundColor = '#35363b';
        }

        resources_table_body.appendChild(resources_table_row);
    }
    resources_table_body.appendChild(resources_table_row);

    table_element.appendChild(resources_table_body);
    table_div.appendChild(table_element);

    table_element.appendChild(resources_table_body);
    table_div.appendChild(table_element);
}

async function populateProcessTable() {
    console.log('Populating Process table');

    // DIV
    console.log('Clearing Process table...');
    var table_div = document.getElementById('processes-table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    table_element.style.width = '100%';
    table_element.style.height = '100%';
    table_element.style.border = '5px solid black';

    // HEADER
    var processes_table_header = document.createElement('thead');
    processes_table_header.innerHTML = '<tr><th>Index</th><th>Name</th><th>Consumes</th><th>Produces</th><th>Time</th><th>Machine</th></tr>';

    processes_table_header.style.width = '100%';
    processes_table_header.style.fontWeight = 'bold';
    processes_table_header.style.padding = '5px';
    table_element.appendChild(processes_table_header);

    // BODY
    var processes_table_body = document.createElement('tbody');

    const processes_response = await filterProcesses();
    for(var i = 0; i < processes_response.processes.length; i++) {
        // console.log(processes_response.processes[i])
        var processes_table_row = document.createElement('tr');

        // Index
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = i;
        processes_table_row.appendChild(processes_table_item);

        // Process Name
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = processes_response.processes[i].name;
        processes_table_row.appendChild(processes_table_item);

        // Process Consumes
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = Object.keys(processes_response.processes[i].consume_uids).length;
        processes_table_row.appendChild(processes_table_item);

        // Process Produces
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = Object.keys(processes_response.processes[i].produce_uids).length;
        processes_table_row.appendChild(processes_table_item);

        // Process Time
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = processes_response.processes[i].process_time_seconds;
        processes_table_row.appendChild(processes_table_item);

        // Process Machine
        var processes_table_item = document.createElement('td');
        processes_table_item.style.padding = '1px 25px';
        processes_table_item.innerHTML = processes_response.processes[i].machine_uid;
        processes_table_row.appendChild(processes_table_item);

        // Additional Formatting
        if(i % 2 == 0) {
            processes_table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            processes_table_row.style.backgroundColor = '#35363b';
        }

        processes_table_body.appendChild(processes_table_row);
    }
    processes_table_body.appendChild(processes_table_row);

    table_element.appendChild(processes_table_body);
    table_div.appendChild(table_element);

    table_element.appendChild(processes_table_body);
    table_div.appendChild(table_element);
}

async function populateWorkflowsTable() {
    console.log('Populating Workflow table');

    // DIV
    console.log('Clearing Workflow table...');
    var table_div = document.getElementById('workflows-table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    table_element.style.width = '100%';
    table_element.style.height = '100%';
    table_element.style.border = '5px solid black';

    // HEADER
    var workflows_table_header = document.createElement('thead');
    workflows_table_header.innerHTML = '<tr><th>Index</th><th>Name</th><th>Process Type</th><th>Processes</th></tr>';
    workflows_table_header.style.width = '100%';
    workflows_table_header.style.fontWeight = 'bold';
    workflows_table_header.style.padding = '5px';
    table_element.appendChild(workflows_table_header);

    // BODY
    var workflows_table_body = document.createElement('tbody');

    const workflows_response = await filterWorkflows();
    for(var i = 0; i < workflows_response.workflows.length; i++) {
        var workflows_table_row = document.createElement('tr');

        // Index
        var workflows_table_item = document.createElement('td');
        workflows_table_item.style.padding = '1px 25px';
        workflows_table_item.innerHTML = i;
        workflows_table_row.appendChild(workflows_table_item);

        // Workflow Name
        var workflows_table_item = document.createElement('td');
        workflows_table_item.style.padding = '1px 25px';
        workflows_table_item.innerHTML = workflows_response.workflows[i].name;
        workflows_table_row.appendChild(workflows_table_item);

        // Workflow Process Type
        var workflows_table_item = document.createElement('td');
        workflows_table_item.style.padding = '1px 25px';
        workflows_table_item.innerHTML = workflows_response.workflows[i].process_type;
        workflows_table_row.appendChild(workflows_table_item);

        // Workflow Processes
        var workflows_table_item = document.createElement('td');
        workflows_table_item.style.padding = '1px 25px';
        workflows_table_item.innerHTML = Object.keys(workflows_response.workflows[i].process_uids).length;
        workflows_table_row.appendChild(workflows_table_item);

        // Additional Formatting
        if(i % 2 == 0) {
            workflows_table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            workflows_table_row.style.backgroundColor = '#35363b';
        }

        workflows_table_body.appendChild(workflows_table_row);
    }
    workflows_table_body.appendChild(workflows_table_row);

    table_element.appendChild(workflows_table_body);
    table_div.appendChild(table_element);

    table_element.appendChild(workflows_table_body);
    table_div.appendChild(table_element);
}

async function populateTables() {
    console.log('Populating tables');
    await populateResourceTable();
    await populateProcessTable();
    await populateWorkflowsTable();
}

window.onload = populateTables;
