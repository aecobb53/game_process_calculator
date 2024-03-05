from copy import deepcopy
from phtml import *

from .base_document import start_base_document


class WorkflowDisplay:
    def __init__(self, workflows_dict: dict = {}, indent_spaces: int=4):
        self.workflow_doc = start_base_document()
        self.workflows_dict = workflows_dict
        self.indent_spaces = indent_spaces

        self.workflow_style = Style(
            style_details={
                'border': '5px solid black',
                'margin': '10px',
                'padding': '10px',
            },
            name='workflow-style')
        self.process_style = Style(
            style_details={
                'border': '3px solid green',
                'margin': '5px',
                'padding': '5px',
            },
            name='process-style')
        self.process_info_style = Style(style_details={
            'padding': '0px 10px',
            'font-size': '110%',
            },
            name='process-info-style')
        self.process_consume_produce_info_style = Style(style_details={
            'padding': '0px',
            'margin': '5px',
            },
            name='process-consume-produce-info-style')

    @property
    def indent(self):
        return " " * self.indent_spaces

    def display_workflow(self):
        workflows_data_div = Div()
        for workflow_dict in self.workflows_dict:
            if workflow_dict['process_type'] == 'LINEAR':
                data_div = self.create_linear_workflow(workflow_dict=workflow_dict)
            workflows_data_div.add_element(data_div)
        self.workflow_doc.add_body_element(workflows_data_div)
        return self.workflow_doc.return_document

    def create_linear_workflow(self, workflow_dict):
        data_div = Div()
        data_div.add_style(style_obj=self.workflow_style)
        data_div.add_element(
            Header(3, f"{workflow_dict['name']}:"),
        )

        process_overview_div = Div().add_style(
            style_obj=Style(style_details={'border': '3px solid red'}))
        detailed_breakdown_div = Div().add_style(
            style_obj=Style(style_details={'border': '3px solid blue'}))

        for process in workflow_dict['processes']:
            process_info_div = Div()
            process_info_style_dict = deepcopy(self.process_style.styles)
            process_info_style_dict['border'] = '3px solid cyan'
            process_info_style = Style(style_details=process_info_style_dict)
            process_info_div.add_style(style_obj=process_info_style)

            time = process['process_time_seconds'] or 0
            time += process['rest_time_seconds'] or 0
            process_info_list = [
                Span(f"Process to craft: {process['name']}"),
                Span(f"Run Time: {time}"),
            ]
            if process['description']:
                process_info_list.append(
                    Span(f"Description: {process['description']}")
                )
            for span in process_info_list:
                span.add_style(style_obj=self.process_info_style)
                process_info_div.add_element(span)


            process_overview_div.add_element(process_info_div)
            detailed_breakdown_div.add_element(process_info_div)


            consume_produce_div = Div().add_style(style_obj=Style(style_details={'display': 'inline-block'}))
            consumes_div = Div()
            consumes_div.add_style(style_obj=self.process_style).add_style(Style({'float': 'left'}))
            if process['consumes_resources']:
                consumes_div.add_element(
                    Paragraph("Consumes:").add_style(
                        style_obj=self.process_consume_produce_info_style).add_style(
                            style_obj=Style(style_details={'font-size': '110%'})
                        )
                )
                for resource in process['consumes_resources']:
                    amount = process['consume_uids'][resource['uid']]
                    consumes_div.add_element(
                        Paragraph(f"{resource['name']}: {amount}").add_style(
                            style_obj=self.process_consume_produce_info_style)
                    )
                consume_produce_div.add_element(consumes_div)

            produces_div = Div()
            produces_div.add_style(style_obj=self.process_style).add_style(Style({'float': 'left'}))
            if process['produces_resources']:
                produces_div.add_element(
                    Paragraph("Produces:").add_style(style_obj=self.process_consume_produce_info_style).add_style(
                            style_obj=Style(style_details={'font-size': '110%'})
                        )
                )
                for resource in process['produces_resources']:
                    amount = process['produce_uids'][resource['uid']]
                    produces_div.add_element(
                        Paragraph(f"{resource['name']}: {amount}").add_style(
                            style_obj=self.process_consume_produce_info_style)
                    )
                consume_produce_div.add_element(produces_div)
            process_overview_div.add_element(consume_produce_div)

        data_div.add_element(process_overview_div)

        detailed_breakdwon_table = Table()

        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print('HERE HERE HRERE HERE')
        import json
        print(json.dumps(workflow_dict, indent=4))
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')
        print('')

        max_consume_resource_count = 0
        max_produce_resource_count = 0
        for process in workflow_dict['processes']:
            max_consume_resource_count = max(max_consume_resource_count, len(process['consumes_resources']))
            max_produce_resource_count = max(max_produce_resource_count, len(process['produces_resources']))

        headers = ['Machine', 'Machine Count']
        [headers.extend([f'Input {i}', 'Units (U/s)']) for i in range(max_consume_resource_count)]
        [headers.extend([f'Output {i}', 'Units (U/s)']) for i in range(max_produce_resource_count)]
        headers.extend(['Time'])
        detailed_breakdwon_table_header_row = TableRow()
        for header in headers:
            detailed_breakdwon_table_header_row.add_element(TableHeader(header))
        detailed_breakdwon_table.add_element(detailed_breakdwon_table_header_row)

        for process in workflow_dict['processes']:
            table_row = TableRow()

            print('')
            print('')
            print('')
            print('')
            print(process)
            print('')
            print('')
            print('')
            print('`')

            # m=Machine
            table_row.add_element(TableData(internal=process['machine_used']))
            table_row.add_element(TableData(internal=process['machine_count']))

            # Input
            for index in range(max_consume_resource_count):
                if len(process['consumes_resources']) <= index:
                    name = '-'
                    units = '-'
                    units_per_second = '-'
                else:
                    name = process['consumes_resources'][index]['name']
                    units = process['consume_uids'][process['consumes_resources'][index]['uid']] * process['machine_count']
                    units_per_second = int(units / time * 100) / 100
                table_row.add_element(TableData(internal=name))
                table_row.add_element(TableData(internal=f"{units} ({units_per_second})"))

            # Output
            for index in range(max_produce_resource_count):
                if len(process['produces_resources']) <= index:
                    name = '-'
                    units = '-'
                else:
                    name = process['produces_resources'][index]['name']
                    units = process['produce_uids'][process['produces_resources'][index]['uid']] * process['machine_count']
                    units_per_second = int(units / time * 100) / 100
                table_row.add_element(TableData(internal=name))
                table_row.add_element(TableData(internal=f"{units} ({units_per_second})"))

            # Time
            time = process['process_time_seconds'] or 0
            time += process['rest_time_seconds'] or 0
            table_row.add_element(TableData(internal=time))

            detailed_breakdwon_table.add_element(table_row)

        detailed_breakdown_div.add_element(detailed_breakdwon_table)
        data_div.add_element(detailed_breakdown_div)

        return data_div

# def start_workflow_display():
#     workflow_display = start_base_document()
#     workflow_display.add_body_element(
#         Header("Workflow Display"),
#     )
#     return workflow_display

# def add_workflow_display(workflow_doc, workflow):
#     # workflow_doc = start_workflow_display()
#     # data_div = workflow_doc.get_body_element_by_tag("div")
#     # data_div.add_element(
#     #     Paragraph("Workflow: " + workflow),
#     # )



#     data_div = Div()
#     data_div.add_element(
#         Paragraph(f"Workflow: {workflow.put()}"),
#     )



#     workflow_doc.add_body_element(data_div)




#     return workflow_doc
