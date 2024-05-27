from turtle import onclick
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent


x=1
doc = Document()
doc.add_body_element(
    Header(1, "HTML Main endpoint function generator"),
)
doc.add_body_element(LineBreak())

major_div_style = Style({'background-color': 'lightblue', 'padding': '10px', 'border': '1px solid black'})

## Projects
projects = Div().add_style(major_div_style)
filter_projects_form = Form(id='filter-projects', action="/projects", method="GET")
filter_projects_form.add_element("Filter")
filter_projects_form.add_element(LineBreak())
filter_projects_form.add_element("Project's Name:")
filter_projects_form.add_element(Input(type="text", id='filter-project-name', name="name"))
projects.add_element(filter_projects_form)
projects.add_element(Button(onclick="filterProjects()", internal="Filter Projects"))
js_filter_script = """
function filterProjects() {
            console.log('Filtering projects');
            url = "http://localhost:8203/projects";

            const form = document.getElementById('filter-projects');
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            console.log(params.toString());

            url = url + "?" + params;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
projects.add_element(Script(internal=js_filter_script))
find_project_form = Form(id='find-project', action="/project", method="GET")
find_project_form.add_element("Find")
find_project_form.add_element(LineBreak())
find_project_form.add_element("Project's UID:")
find_project_form.add_element(Input(type="text", id='find-project-name', name="project-uid"))
projects.add_element(find_project_form)
projects.add_element(Button(onclick="findProject()", internal="Find Project"))
js_find_script = """
function findProject() {
            console.log('Finding project');
            url = "http://localhost:8203/project";

            const form = document.getElementById('find-project');
            const formData = new FormData(form);
            project_uid = formData.get('project-uid');

            url = url + "/" + project_uid;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
projects.add_element(Script(internal=js_find_script))
doc.add_body_element(projects)
doc.add_body_element(LineBreak())


## Resources
resources = Div().add_style(major_div_style)
filter_resources_form = Form(id='filter-resources', action="/resources", method="GET")
filter_resources_form.add_element("Filter")
filter_resources_form.add_element(LineBreak())
filter_resources_form.add_element("Resource's Name:")
filter_resources_form.add_element(Input(type="text", id='filter-resource-name', name="name"))
resources.add_element(filter_resources_form)
resources.add_element(Button(onclick="filterResources()", internal="Filter Resources"))
js_filter_script = """
function filterResources() {
            console.log('Filtering resources');
            url = "http://localhost:8203/resources";

            const form = document.getElementById('filter-resources');
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            console.log(params.toString());

            url = url + "?" + params;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
resources.add_element(Script(internal=js_filter_script))
find_resource_form = Form(id='find-resource', action="/resource", method="GET")
find_resource_form.add_element("Find")
find_resource_form.add_element(LineBreak())
find_resource_form.add_element("Resource's UID:")
find_resource_form.add_element(Input(type="text", id='find-resource-name', name="resource-uid"))
resources.add_element(find_resource_form)
resources.add_element(Button(onclick="findResource()", internal="Find Resource"))
js_find_script = """
function findResource() {
            console.log('Finding resource');
            url = "http://localhost:8203/resource";

            const form = document.getElementById('find-resource');
            const formData = new FormData(form);
            resource_uid = formData.get('resource-uid');

            url = url + "/" + resource_uid;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
resources.add_element(Script(internal=js_find_script))
doc.add_body_element(resources)
doc.add_body_element(LineBreak())


## Processes
processes = Div().add_style(major_div_style)
filter_processes_form = Form(id='filter-processes', action="/processes", method="GET")
filter_processes_form.add_element("Filter")
filter_processes_form.add_element(LineBreak())
filter_processes_form.add_element("Process's Name:")
filter_processes_form.add_element(Input(type="text", id='filter-processe-name', name="name"))
processes.add_element(filter_processes_form)
processes.add_element(Button(onclick="filterProcesses()", internal="Filter Processes"))
js_filter_script = """
function filterProcesses() {
            console.log('Filtering processes');
            url = "http://localhost:8203/processes";

            const form = document.getElementById('filter-processes');
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            console.log(params.toString());

            url = url + "?" + params;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
processes.add_element(Script(internal=js_filter_script))
find_process_form = Form(id='find-process', action="/process", method="GET")
find_process_form.add_element("Find")
find_process_form.add_element(LineBreak())
find_process_form.add_element("Project's UID:")
find_process_form.add_element(Input(type="text", id='find-process-name', name="process-uid"))
processes.add_element(find_process_form)
processes.add_element(Button(onclick="findProcess()", internal="Find Process"))
js_find_script = """
function findProcess() {
            console.log('Finding process');
            url = "http://localhost:8203/process";

            const form = document.getElementById('find-process');
            const formData = new FormData(form);
            process_uid = formData.get('process-uid');

            url = url + "/" + process_uid;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
projects.add_element(Script(internal=js_find_script))
doc.add_body_element(processes)
doc.add_body_element(LineBreak())


## Workflows
workflows = Div().add_style(major_div_style)
filter_workflows_form = Form(id='filter-workflows', action="/workflows", method="GET")
filter_workflows_form.add_element("Filter")
filter_workflows_form.add_element(LineBreak())
filter_workflows_form.add_element("Workflow's Name:")
filter_workflows_form.add_element(Input(type="text", id='filter-workflow-name', name="name"))
workflows.add_element(filter_workflows_form)
workflows.add_element(Button(onclick="filterWorkflows()", internal="Filter Workflows"))
js_filter_script = """
function filterWorkflows() {
            console.log('Filtering workflows');
            url = "http://localhost:8203/workflows";

            const form = document.getElementById('filter-workflows');
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            console.log(params.toString());

            url = url + "?" + params;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
workflows.add_element(Script(internal=js_filter_script))
find_workflow_form = Form(id='find-workflow', action="/workflow", method="GET")
find_workflow_form.add_element("Find")
find_workflow_form.add_element(LineBreak())
find_workflow_form.add_element("Project's UID:")
find_workflow_form.add_element(Input(type="text", id='find-workflow-name', name="workflow-uid"))
workflows.add_element(find_workflow_form)
workflows.add_element(Button(onclick="findWorkflow()", internal="Find Workflow"))
js_find_script = """
function findWorkflow() {
            console.log('Finding workflow');
            url = "http://localhost:8203/workflow";

            const form = document.getElementById('find-workflow');
            const formData = new FormData(form);
            workflow_uid = formData.get('workflow-uid');

            url = url + "/" + workflow_uid;
            console.log(url);

            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => console.log(data));
        }
"""
projects.add_element(Script(internal=js_find_script))
doc.add_body_element(workflows)
doc.add_body_element(LineBreak())

x=1

with open('bin/generate_main_html.html', 'w') as f:
    # f.write(str(new_formated_doc.return_document))
    f.write(str(doc.return_document))

x=1




# workflows_data_div = Div()
# navigation_content = NavigationContent(webpage_name="Game Process Calculator")
# body_content = BodyContent(body_content=[workflows_data_div])
# footer_content = FooterContent(
#     footer_content=[Header(level=3, internal='Game Process Calculator').add_style(
#         Style(style_details={'margin': '0', 'padding': '0'}))],)
# new_formated_doc = MyBaseDocument(
#     navigation_content=navigation_content,
#     body_content=body_content,
#     footer_content=footer_content,
# )



