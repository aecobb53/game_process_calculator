// Replace Variables
//   SERVICE_URL
var service_url = 'SERVICE_URL'

async function filterResources() {
    console.log('Filtering resources');

    const form = document.getElementById('filter-resources');
    const formData = new FormData(form);

    var resource_name = formData.get('resource-name');
    var project_name = formData.get('project-name');

    const object = {
        'name': resource_name,
    };

    // If Project name provided, get the project_uid
    if(project_name) {
        console.log('Project name provided: ' + project_name);
        const project_data = await filterProjectsByName(project_name);
        console.log('Project data: ');
        console.log(project_data);
        var project_uid = project_data.projects[0].uid;
        console.log('Project UID: ' + project_uid);
        object['project_uid'] = project_uid;
    }

    const params = new URLSearchParams(object);
    console.log('params: ' + params.toString());

    url = service_url + "/resource?" + params;
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
    console.log(data);
    return data;
}

async function filterProjectsByName(name) {
    console.log('Filtering projects by name: ' + name);

    const params = new URLSearchParams({'name': name});
    console.log('params: ' + params.toString());

    url = service_url + "/project?" + params;
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

async function filterProjectsByUID(project_uid) {
    console.log('Filtering projects by project_uid: ' + project_uid);

    const params = new URLSearchParams({'uid': project_uid});
    console.log('params: ' + params.toString());

    url = service_url + "/project?" + params;
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

async function populateTable() {
    console.log('Populating table');

    var tracking_project_name_hashtable = {};

    // DIV
    console.log('Clearing table...');
    var table_div = document.getElementById('resources-table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    table_element.style.width = '100%';
    table_element.style.height = '100%';
    table_element.style.border = '5px solid black';

    // HEADER
    var resources_table_header = document.createElement('thead');
    resources_table_header.style.width = '100%';
    resources_table_header.style.fontWeight = 'bold';
    resources_table_header.style.padding = '5px';
    var header_values = ['Resource', 'Project'];
    var resources_table_row = document.createElement('tr');
    for(var i = 0; i < header_values.length; i++) {
        var resources_table_item = document.createElement('th');
        resources_table_item.innerHTML = header_values[i];
        resources_table_row.appendChild(resources_table_item);
    }
    resources_table_header.appendChild(resources_table_row);
    table_element.appendChild(resources_table_header);

    // BODY
    var resources_table_body = document.createElement('tbody');
    const resources_response = await filterResources();
    const resources_array = resources_response.resources;
    for(var i = 0; i < resources_array.length; i++) {
        // ROW
        var resources_table_row = document.createElement('tr');
        resources_table_row.style.padding = '5px';
        resources_table_row.style.border = '1px red double'

        // Resource Name
        var resource_hyperlink = document.createElement("a");
        resource_hyperlink.href = service_url + '/html/resource/' + resources_array[i].uid;
        resource_hyperlink.innerHTML = resources_array[i].name;

        var resources_table_item = document.createElement('td');
        resources_table_item.style.padding = '1px 25px';
        resources_table_item.appendChild(resource_hyperlink);
        resources_table_row.appendChild(resources_table_item);

        if (resources_array[i].project_uid in tracking_project_name_hashtable) {
            var resources_table_item = document.createElement('td');
            resources_table_item.style.padding = '1px 25px';
            resources_table_item.innerHTML = tracking_project_name_hashtable[resources_array[i].project_uid];
            resources_table_row.appendChild(resources_table_item);
        } else {
            const project_response = await filterProjectsByUID(project_uid=resources_array[i].project_uid);
            var resources_table_item = document.createElement('td');
            resources_table_item.style.padding = '1px 25px';
            resources_table_item.innerHTML = project_response.projects[0].name;
            resources_table_row.appendChild(resources_table_item);
            tracking_project_name_hashtable[resources_array[i].project_uid] = project_response.projects[0].name;
        }

        // Additional Formatting
        if(i % 2 == 0) {
            resources_table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            resources_table_row.style.backgroundColor = '#35363b';
        }
        resources_table_body.appendChild(resources_table_row);
    }

    table_element.appendChild(resources_table_body);
    table_div.appendChild(table_element);

    table_element.appendChild(resources_table_body);
    table_div.appendChild(table_element);
}
window.onload = populateTable;
