// Replace Variables
//   SERVICE_URL
var service_url = 'SERVICE_URL'

async function filterProjects() {
    console.log('Filtering projects');

    const form = document.getElementById('filter-projects');
    const formData = new FormData(form);
    const params = new URLSearchParams(formData);
    console.log('params: ' + params.toString());

    url = service_url + "/projects?" + params;
    console.log('url: ' + url);

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

async function filterResources(project_uid) {
    console.log('Filtering resources for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/resources?" + params;
    console.log('url: ' + url);

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

async function filterProcesses(project_uid) {
    console.log('Filtering processes for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/processes?" + params;
    console.log('ur;: ' + url);

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

async function filterWorkflows(project_uid) {
    console.log('Filtering workflows for project_uid: ' + project_uid);

    params = new URLSearchParams({project_uid: project_uid});

    url = service_url + "/workflows?" + params;
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

async function populateTable() {
    console.log('Populating table');

    // DIV
    console.log('Clearing table...');
    var table_div = document.getElementById('projects-table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    table_element.style.width = '100%';
    table_element.style.height = '100%';
    table_element.style.border = '5px solid black';

    // HEADER
    var projects_table_header = document.createElement('thead');
    projects_table_header.innerHTML = '<tr><th>Name</th><th>Resource Count</th><th>Process Count</th><th>Workflow Count</th></tr>';
    projects_table_header.style.width = '100%';
    projects_table_header.style.fontWeight = 'bold';
    projects_table_header.style.padding = '5px';
    table_element.appendChild(projects_table_header);

    // BODY
    var projects_table_body = document.createElement('tbody');
    const projects_response = await filterProjects();
    const projects_array = projects_response.projects;
    for(var i = 0; i < projects_array.length; i++) {
        // ROW
        var projects_table_row = document.createElement('tr');
        projects_table_row.style.padding = '5px';
        projects_table_row.style.border = '1px red double'

        console.log('ROW: ' + projects_table_row);

        // Project Name
        var project_hyperlink = document.createElement("a");
        project_hyperlink.href = service_url + '/html/project/' + projects_array[i].uid;
        project_hyperlink.innerHTML = projects_array[i].name;

        var projects_table_item = document.createElement('td');
        projects_table_item.style.padding = '1px 25px';
        projects_table_item.appendChild(project_hyperlink);
        projects_table_row.appendChild(projects_table_item);


        // Resources
        const resources_response = await filterResources(project_id=projects_array[i].uid);
        var projects_table_item = document.createElement('td');
        projects_table_item.style.padding = '1px 25px';
        projects_table_item.innerHTML = resources_response.resources.length;
        projects_table_row.appendChild(projects_table_item);

        // Processes
        const processes_response = await filterProcesses(project_id=projects_array[i].uid);
        var projects_table_item = document.createElement('td');
        projects_table_item.style.padding = '1px 25px';
        projects_table_item.innerHTML = processes_response.processes.length;
        projects_table_row.appendChild(projects_table_item);

        // Workflows
        const workflows_response = await filterWorkflows(project_id=projects_array[i].uid);
        var projects_table_item = document.createElement('td');
        projects_table_item.style.padding = '1px 25px';
        projects_table_item.innerHTML = workflows_response.workflows.length;
        projects_table_row.appendChild(projects_table_item);

        // Additional Formatting
        if(i % 2 == 0) {
            projects_table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            projects_table_row.style.backgroundColor = '#35363b';
        }
        projects_table_body.appendChild(projects_table_row);
    }

    table_element.appendChild(projects_table_body);
    table_div.appendChild(table_element);

    table_element.appendChild(projects_table_body);
    table_div.appendChild(table_element);
}
window.onload = populateTable;
