from turtle import onclick
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent



def filter_projects_html_page():
    page_content = Div()
    page_content.add_element(
        Header(level=1, internal='Projects').add_style({'margin': '20px'}))

    page_content.add_element(Button(
        onclick='populateTable()',
        internal='Refresh',
    ))

    # Table
    projects_table_div = Div(id='projects-table-div').add_style({
        'width:': '100%',
        'height': '100%',
        'border': '5px solid black',
    })
    projects_table = Table(id='projects-table').add_style({
        'width': '100%',
        'border': '1px red double',
    })
    projects_table_header = TableRow()
    header_style = Style(style_details={
        'font-weight': 'bold',
        'padding': '5px'})
    projects_table_header.add_element(TableHeader(internal='Name').add_style(header_style))
    projects_table_header.add_element(TableHeader(internal='Resource Count').add_style(header_style))
    projects_table_header.add_element(TableHeader(internal='Process Count').add_style(header_style))
    projects_table_header.add_element(TableHeader(internal='Workflow Count').add_style(header_style))
    projects_table.add_element(projects_table_header)
    projects_table_div.add_element(projects_table)
    page_content.add_element(projects_table_div)

    # Get data scripts
    get_projects_script = Script(internal="""
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
""")
    get_resources_script = Script(internal="""
    """)
    get_processes_script = Script(internal="""
    """)
    get_workflows_script = Script(internal="""
    """)
    populate_table = Script(internal="""
    function populateTable() {
        console.log('Populating table');
        console.log('Celaring table...');

        var table_div = document.getElementById('projects-table-div');
        table_div.innerHTML = '';

        console.log('Populating table header...');
        // var projects_table = document.createElement('table');
        // table_div.appendChild(projects_table);
        var projects_table_header = document.createElement('thead');
        projects_table_header.innerHTML = '<tr><th style="font-weight: bold; padding: 5px;">Name</th><th style="font-weight: bold; padding: 5px;">Resource Count</th><th style="font-weight: bold; padding: 5px;">Process Count</th><th style="font-weight: bold; padding: 5px;">Workflow Count</th></tr>';

        // const newDiv = document.createElement('div');
        // const newContent = document.createTextNode('Hello! How are you?');
        // newDiv.appendChild(newContent);
        // const currentDiv = document.getElementById('div1');
        // document.body.insertBefore(newDiv, currentDiv);
        // document.getElementById('projects-table-div').innerHTML = projects_table_header;
        document.getElementById('projects-table-div').appendChild(projects_table_header);
        //document.getElementById('projects-table-div').innerHTML = '<table id="projects-table" style="width: 100%; border: 1px red double;"><tr><th style="font-weight: bold; padding: 5px;">Name</th><th style="font-weight: bold; padding: 5px;">Resource Count</th><th style="font-weight: bold; padding: 5px;">Process Count</th><th style="font-weight: bold; padding: 5px;">Workflow Count</th></tr></table>';


        var projects_table_body = document.createElement('tbody');
        var projects_table_row = document.createElement('tr');
        projects_table_row.innerHTML = '<td>Project 1</td><td>3</td><td>5</td><td>2</td>';

        projects_table_body.appendChild(projects_table_row);
        table_div.appendChild(projects_table_body);





        // var old_tbody = document.getElementById('projects-table');
        // var new_tbody = document.createElement('tbody');
        // populate
    }
    """)

    page_content.add_element(get_projects_script)
    page_content.add_element(get_resources_script)
    page_content.add_element(get_processes_script)
    page_content.add_element(get_workflows_script)
    page_content.add_element(populate_table)

    navigation_content = NavigationContent(webpage_name="Game Process Calculator")
    body_content = BodyContent(body_content=[page_content])
    footer_content = FooterContent(
        footer_content=[Header(level=3, internal='Game Process Calculator').add_style(
            Style(style_details={'margin': '0', 'padding': '0'}))],)
    new_formated_doc = MyBaseDocument(
        navigation_content=navigation_content,
        body_content=body_content,
        # footer_content=footer_content,
    )

    return new_formated_doc.return_document


# create - Create a new project
# filter - Filter all projects
# find - Get project and associated information
# update - Update a project. List dependencies and show impacts
# delete - Confirm delete a project
