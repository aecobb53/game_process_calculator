// Replace Variables
//   SERVICE_URL
var service_url = 'SERVICE_URL'

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

async function createProject() {
    console.log('Creating Project');

    const form = document.getElementById('modify-project');
    const formData = new FormData(form);

    var object = {};
    formData.forEach((value, key) => object[key] = value);
    var json = JSON.stringify(object);
    console.log('Create Project payload: ' + json);

    url = service_url + "/project";
    console.log('url: ' + url);

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: json,
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);

    // DIV
    console.log('Showing result');
    var create_project_result_div = document.getElementById('modify-project-result');
    create_project_result_div.innerHTML = '';
    var create_project_result_content = document.createElement('p');

    if(status == 201) {
        const message = 'Project "' + data.name + '" Created'
        console.log(message);
        create_project_result_content.innerHTML = message;
        create_project_result_div.appendChild(create_project_result_content);
    }
    else if(status == 409) {
        message = 'Project "' + object.name + '" already exists'
        console.log(message);
        create_project_result_content.innerHTML = message;
        create_project_result_div.appendChild(create_project_result_content);
    }
    else {
        message = 'Failed to create Project "' + json.name + '"'
        console.log(message);
        create_project_result_content.innerHTML = message;
        create_project_result_div.appendChild(create_project_result_content);
    }
    return data;
}

async function updateProject() {
    console.log('Updating project');

    const form = document.getElementById('update-project');
    const formData = new FormData(form);
    var old_name = formData.get('old-name');
    var new_name = formData.get('new-name');
    console.log('Updating "' + old_name + '" to "' + new_name + '"');

    projects = await filterProjectsByName(old_name);
    console.log('Projects found: ');
    console.log(projects);

    // Initial DIV
    // console.log('Showing result if GET failed');
    var update_project_result_div = document.getElementById('update-project-result');
    update_project_result_div.innerHTML = '';
    var update_project_result_content = document.createElement('p');

    if(projects.projects.length < 1) {
        console.log('Project "' + old_name + '" not found');
        update_project_result_content.innerHTML = 'No project found for "' + old_name + '", nothing to update';
        update_project_result_div.appendChild(update_project_result_content);
        return
    }
    else if (projects.projects.length > 1) {
        console.log('Multiple projects found for "' + old_name + '"');
        update_project_result_content.innerHTML = 'Too many projects found for "' + old_name + '", please give a more specific name';
        update_project_result_div.appendChild(update_project_result_content);
        return
    }

    var old_project_uid = projects.projects[0].uid;
    console.log('Project found: ' + old_project_uid);

    var json = projects.projects[0]
    json.name = new_name;
    console.log('Update Project payload: ' + JSON.stringify(json));

    url = service_url + "/project/" + old_project_uid;
    console.log('url: ' + url);

    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(json),
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);

    // DIV
    console.log('Showing result');
    var update_project_result_div = document.getElementById('update-project-result');
    update_project_result_div.innerHTML = '';
    var update_project_result_content = document.createElement('p');

    if(status == 200) {
        const message = 'Project "' + data.name + '" Updated'
        console.log(message);
        update_project_result_content.innerHTML = message;
        update_project_result_div.appendChild(update_project_result_content);
    }
    else if(status == 409) {
        message = 'Project "' + object.name + '" already exists'
        console.log(message);
        update_project_result_content.innerHTML = message;
        update_project_result_div.appendChild(update_project_result_content);
    }
    else {
        message = 'Failed to update Project "' + json.name + '"'
        console.log(message);
        update_project_result_content.innerHTML = message;
        update_project_result_div.appendChild(update_project_result_content);
    }
    return data;
}

async function deleteProject() {
    console.log('Deleting project');

    const form = document.getElementById('delete-project');
    const formData = new FormData(form);
    project_name = formData.get('name');
    console.log('Name of project deleting: ' + project_name);

    projects = await filterProjectsByName(project_name);

    // DIV
    console.log('Showing result');
    var delete_project_result_div = document.getElementById('delete-project-result');
    delete_project_result_div.innerHTML = '';
    var delete_project_result_content = document.createElement('p');

    if(projects.projects.length < 1) {
        console.log('Project "' + project_name + '" not found');
        delete_project_result_content.innerHTML = 'No project found for "' + project_name + '", nothing to delete';
        delete_project_result_div.appendChild(delete_project_result_content);
    }
    else if (projects.projects.length > 1) {
        console.log('Multiple projects found for "' + project_name + '"');
        delete_project_result_content.innerHTML = 'Too many projects found for "' + project_name + '", please filter by a more specific name';
        delete_project_result_div.appendChild(delete_project_result_content);
    }

    var project_uid = projects.projects[0].uid;

    url = service_url + "/project/" + project_uid;
    console.log('url: ' + url);

    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    const status = response.status;
    console.log('Call status: ' + status);
    console.log('Project "' + data.name + '" Successfully Deleted');
    delete_project_result_content.innerHTML = 'Project "' + data.name + '" Successfully Deleted';
    delete_project_result_div.appendChild(delete_project_result_content);
}
