import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent

service_url = os.environ.get('SERVICE_URL')


# def create_project_html_page():
#     page_content = Div().add_style({'display': 'block'})

#     # Create
#     create_project_div = Div(id='modify-project-div')
#     create_project_div.add_element(Header(level=1, internal=f"Create, Update, or Delete Project").add_style({'margin': '20px'}))

#     # Form
#     filter_projects_form = Form(id='modify-project')
#     filter_projects_form.add_element("New Project Name:")
#     filter_projects_form.add_element(Input(type="text", id='modify-project-name', name="name"))
#     create_project_div.add_element(filter_projects_form)
#     create_project_div.add_element(Button(
#         onclick='createProject()',
#         internal='Create Project',
#     ))

#     # Result
#     create_result_div = Div(id='modify-project-result')
#     create_project_div.add_element(create_result_div)
#     page_content.add_element(create_project_div)


#     # Update
#     update_project_div = Div(id='update-project-div')
#     update_project_div.add_element(Header(level=1, internal=f"Update Project").add_style({'margin': '20px'}))

#     # Form
#     update_projects_form = Form(id='update-project')
#     update_projects_form.add_element("Old Project Name:")
#     update_projects_form.add_element(Input(type="text", id='update-project-old-name', name="old-name"))
#     update_projects_form.add_element("New Project Name:")
#     update_projects_form.add_element(Input(type="text", id='update-project-new-name', name="new-name"))
#     update_project_div.add_element(update_projects_form)
#     update_project_div.add_element(Button(
#         onclick='updateProject()',
#         internal='Update Project',
#     ))

#     # Result
#     update_result_div = Div(id='update-project-result')
#     update_project_div.add_element(update_result_div)
#     page_content.add_element(update_project_div)


#     # Delete
#     delete_project_div = Div(id='delete-project-div')
#     delete_project_div.add_element(Header(level=1, internal=f"Delete Project").add_style({'margin': '20px'}))

#     # Form
#     delete_projects_form = Form(id='delete-project')
#     delete_projects_form.add_element("Project Name:")
#     delete_projects_form.add_element(Input(type="text", id='delete-project-name', name="name"))
#     delete_project_div.add_element(delete_projects_form)
#     delete_project_div.add_element(Button(
#         onclick='deleteProject()',
#         internal='Delete Project',
#     ))

#     # Result
#     delete_result_div = Div(id='delete-project-result')
#     delete_project_div.add_element(delete_result_div)
#     page_content.add_element(delete_project_div)

#     # JS file
#     js_file = []
#     create_update_delete_project_html_js_path = 'html/project/create_update_delete_project_html.js'
#     with open(create_update_delete_project_html_js_path, 'r') as jf:
#         for line in jf.readlines():
#             line = line.replace('SERVICE_URL', service_url)
#             js_file.append(line)

#     create_update_delete_project_html_script = Script(internal=js_file)
#     page_content.add_element(create_update_delete_project_html_script)

#     navigation_content = NavigationContent(webpage_name="Game Process Calculator")
#     body_content = BodyContent(body_content=[page_content])
#     new_formatted_doc = MyBaseDocument(
#         navigation_content=navigation_content,
#         body_content=body_content,
#     )
#     return new_formatted_doc.return_document


def filter_resources_html_page():
    page_content = Div()
    page_content.add_element(
        Header(level=1, internal='Resources').add_style({'margin': '20px'}))

    # Form
    filter_resources_form = Form(id='filter-resources')
    filter_resources_form.add_element("Resource Name:")
    filter_resources_form.add_element(Input(type="text", id='resource-name', name="resource-name"))
    filter_resources_form.add_element("Project Name:")
    filter_resources_form.add_element(Input(type="text", id='project-name', name="project-name"))
    filter_resources_form.add_element("Acquired from Resource name:")
    filter_resources_form.add_element(Input(type="text", id='acquired-resource-name', name="acquired-resource-name", placeholder='NOT IMPLEMENTED YET'))
    filter_resources_form.add_element("Converted into Resource name:")
    filter_resources_form.add_element(Input(type="text", id='desposal-resource-name', name="desposal-resource-name", placeholder='NOT IMPLEMENTED YET'))
    filter_resources_form.add_element("Relative Value:")
    filter_resources_form.add_element(Input(type="text", id='relative-value-resource-name', name="relative-value-resource-name", placeholder='NOT IMPLEMENTED YET'))
    page_content.add_element(filter_resources_form)
    page_content.add_element(Button(
        onclick='populateTable()',
        internal='Refresh',
    ))

    # Create Resource
    create_resource_div = Div()
    create_resource_div.add_element(Link(href='/html/modify-resource', internal=Button(
        internal='Create, Update or Delete Resource',
    )))
    page_content.add_element(create_resource_div)

    # Table
    resources_table_div = Div(id='resources-table-div').add_style({
        'width:': '100%',
        'height': '100%',
        'border': '5px solid black',
    })
    resources_table = Table(id='resources-table').add_style({
        'width': '100%',
        'border': '1px red double',
    })
    resources_table_div.add_element(resources_table)
    page_content.add_element(resources_table_div)

    # JS file
    js_file = []
    find_resource_html_js_path = 'html/resource/filter_resources_html.js'
    with open(find_resource_html_js_path, 'r') as jf:
        for line in jf.readlines():
            line = line.replace('SERVICE_URL', service_url)
            js_file.append(line)

    find_resource_html_script = Script(internal=js_file)
    page_content.add_element(find_resource_html_script)

    navigation_content = NavigationContent(webpage_name="Game Process Calculator")
    body_content = BodyContent(body_content=[page_content])
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        body_content=body_content,
    )
    return new_formatted_doc.return_document

# def find_project_html_page(project):
#     page_content = Div().add_style({'display': 'block'})
#     page_content.add_element(Header(level=1, internal=f"Project: {project.name}").add_style({'margin': '20px'}))

#     page_tables_div = Div().add_style({'display': 'inline-flex', 'width': '100%'})
#     table_style = {'padding': '20px', 'margin': '5px', 'border': '5px solid black', 'width': '33%'}
#     # table_style = {'padding': '20px', 'margin': '5px', 'border': '5px solid black', 'min-width': '100px', 'max-wdith': '33%'}

#     # Resources
#     resource_div = Div().add_style(table_style)
#     resource_div.add_element(Header(level=2, internal="Resources").add_style({'margin': '20px'}))
#     resource_table_div = Div(id='resources-table-div')
#     resource_table = Table().add_style({
#         'width': '100%',
#         'border': '1px red double',
#     })

#     resource_table_div.add_element(resource_table)
#     resource_div.add_element(resource_table_div)
#     page_tables_div.add_element(resource_div)

#     # Processes
#     process_div = Div().add_style(table_style)
#     process_div.add_element(Header(level=2, internal="Processes").add_style({'margin': '20px'}))
#     process_table_div = Div(id='processes-table-div')
#     process_table = Table().add_style({
#         'width': '100%',
#         'border': '1px red double',
#     })

#     process_table_div.add_element(process_table)
#     process_div.add_element(process_table_div)
#     page_tables_div.add_element(process_div)

#     # Workflows
#     workflow_div = Div().add_style(table_style)
#     workflow_div.add_element(Header(level=2, internal="Workflows").add_style({'margin': '20px'}))
#     workflow_table_div = Div(id='workflows-table-div')
#     workflow_table = Table().add_style({
#         'width': '100%',
#         'border': '1px red double',
#     })

#     workflow_table_div.add_element(workflow_table)
#     workflow_div.add_element(workflow_table_div)
#     page_tables_div.add_element(workflow_div)

#     # JS file
#     js_file = []
#     find_project_html_js_path = 'html/project/find_project_html.js'
#     with open(find_project_html_js_path, 'r') as jf:
#         for line in jf.readlines():
#             line = line.replace('SERVICE_URL', service_url)
#             line = line.replace('PROJECT_UID', project.uid)
#             js_file.append(line)

#     find_project_html_script = Script(internal=js_file)
#     page_tables_div.add_element(find_project_html_script)

#     page_content.add_element(page_tables_div)

#     navigation_content = NavigationContent(webpage_name="Game Process Calculator")
#     body_content = BodyContent(body_content=[page_content])
#     new_formatted_doc = MyBaseDocument(
#         navigation_content=navigation_content,
#         body_content=body_content,
#     )
#     return new_formatted_doc.return_document

# # create - Create a new project
# # filter - Filter all projects
# # find - Get project and associated information
# # update - Update a project. List dependencies and show impacts
# # delete - Confirm delete a project
