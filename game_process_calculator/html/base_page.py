import os

from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent


service_url = os.environ.get('SERVICE_URL')


def project_base_page():
    page_content = Div().add_style({'display': 'block'})

    # Welcome
    welcome_div = Div(id='welcome-div')
    welcome_div.add_element(Header(level=1, internal=f"Welcome to the Game Process Calculator!").add_style({'margin': '20px'}))
    welcome_div.add_element(Paragraph(internal=f"""
    The Game Process Calculator is a tool for planning bases for games like Factorio, Satisfactory, and others.
    """).add_style({'margin': '20px'}))
    page_content.add_element(welcome_div)

    # Table of Contents
    toc_div = Div(id='toc-div')

    # Projects
    toc_div.add_element(Header(level=2, internal=f"Projects").add_style({'margin': '20px'}))
    toc_projects_url_list = HtmlList(ordered=False).add_style({'margin': '20px', 'background-color': 'white'})
    toc_projects_url_list.add_element(
        HtmlListItem(Link(internal='Create, Update, or Delete Project', href=f'{service_url}/html/project/modify')))
    toc_projects_url_list.add_element(
        HtmlListItem(Link(internal='Projects List', href=f'{service_url}/html/project')))
    toc_div.add_element(toc_projects_url_list)

    # Resources
    toc_div.add_element(Header(level=2, internal=f"Resources").add_style({'margin': '20px'}))
    toc_resources_url_list = HtmlList(ordered=False).add_style({'margin': '20px', 'background-color': 'white'})
    toc_resources_url_list.add_element(
        HtmlListItem(Link(internal='Create, Update, or Delete Resource', href=f'{service_url}/html/modify-resource')))
    toc_resources_url_list.add_element(
        HtmlListItem(Link(internal='Resources List', href=f'{service_url}/html/resources')))
    toc_div.add_element(toc_resources_url_list)

    # Processes
    toc_div.add_element(Header(level=2, internal=f"Processes").add_style({'margin': '20px'}))
    toc_processes_url_list = HtmlList(ordered=False).add_style({'margin': '20px', 'background-color': 'white'})
    toc_processes_url_list.add_element(
        HtmlListItem(Link(internal='Create, Update, or Delete Process', href=f'{service_url}/html/modify-process')))
    toc_processes_url_list.add_element(
        HtmlListItem(Link(internal='Processes List', href=f'{service_url}/html/processes')))
    toc_div.add_element(toc_processes_url_list)

    # Workflows
    toc_div.add_element(Header(level=2, internal=f"Workflows").add_style({'margin': '20px'}))
    toc_workflows_url_list = HtmlList(ordered=False).add_style({'margin': '20px', 'background-color': 'white'})
    toc_workflows_url_list.add_element(
        HtmlListItem(Link(internal='Create, Update, or Delete Workflow', href=f'{service_url}/html/modify-workflow')))
    toc_workflows_url_list.add_element(
        HtmlListItem(Link(internal='Workflows List', href=f'{service_url}/html/workflows')))
    toc_div.add_element(toc_workflows_url_list)

    page_content.add_element(toc_div)

    navigation_content = NavigationContent(webpage_name="Game Process Calculator")
    body_content = BodyContent(body_content=[page_content])
    new_formatted_doc = MyBaseDocument(
        navigation_content=navigation_content,
        body_content=body_content,
    )
    return new_formatted_doc.return_document
