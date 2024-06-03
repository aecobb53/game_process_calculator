from copy import deepcopy
from phtml import *
from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent

from handlers import DataHandler
from utils import Utils



from .base_document import start_base_document


class WorkflowDisplay:
    def __init__(self, workflows_dict: dict = {}, indent_spaces: int=4):
        self.workflow_doc = start_base_document()
        self.workflows_dict = workflows_dict
        self.indent_spaces = indent_spaces
        self.data_handler = DataHandler()

        self.workflow_style = Style(
            style_details={
                'border': '5px solid black',
                'margin': '10px',
                # 'padding': '10px',
                'padding': '0px',
            },
            name='workflow-style')
        self.process_style = Style(
            style_details={
                # 'border': '3px solid green',
                # 'margin': '5px',
                'margin': '0px',
                'padding': '2px 2px 5px',
            },
            name='process-style')
        self.process_info_style = Style(style_details={
            'padding': '0px 10px',
            'font-size': '110%',
            },
            name='process-info-style')
        self.process_consume_produce_info_style = Style(style_details={
            'padding': '0px 5px',
            'margin': '0px',
            },
            name='process-consume-produce-info-style')

        self.table_header_style = Style(style_details={
            'border': '1px solid black',
            'margin': '2px',
            'padding': '2px',
            # 'width': '100%',
            'text-align': 'left',
            },
            name='table-data-style')

        self.table_data_style = Style(style_details={
            'border': '1px solid black',
            'margin': '0px',
            'padding': '0px',
            # 'width': '100%',
            'text-align': 'left',
            },
            name='table-data-style')

        self.utils = Utils()

    @property
    def indent(self):
        return " " * self.indent_spaces

    def display_workflow(self):
        workflows_data_div = Div()
        for workflow_dict in self.workflows_dict:
            if workflow_dict['process_type'] == 'LINEAR':
                data_div = self.create_linear_workflow(workflow_dict=workflow_dict)
            workflows_data_div.add_element(data_div)
        navigation_content = NavigationContent(webpage_name="Game Process Calculator")
        body_content = BodyContent(body_content=[workflows_data_div])
        footer_content = FooterContent(
            footer_content=[Header(level=3, internal='Game Process Calculator').add_style(
                Style(style_details={'margin': '0', 'padding': '0'}))],)
        new_formated_doc = MyBaseDocument(
            navigation_content=navigation_content,
            body_content=body_content,
            footer_content=footer_content,
        )

        return new_formated_doc.return_document

    def create_linear_workflow(self, workflow_dict, precision=3):
        data_div = Div()
        data_div.add_style(style_obj=self.workflow_style)
        data_div.add_element(
            Header(1, f"{workflow_dict['name']}:").add_style(
                Style(style_details={'padding': '10px'})
            ),
        )

        process_overview_div = Div().add_style(
            style_obj=Style(style_details={'padding': '5px'}))
            # style_obj=Style(style_details={'border': '3px solid red'}))
        process_overview_div.add_element(Header(2, "Processes Overview:").add_style(
            Style(style_details={'margin': '0', 'padding': '5px', 'text-decoration': 'underline'})))

        detailed_breakdown_div = Div().add_style(
            style_obj=Style(style_details={'padding': '5px'}))
            # style_obj=Style(style_details={'border': '3px solid blue'}))
        detailed_breakdown_div.add_element(Header(2, "Adjusted Process Overview:").add_style(
            Style(style_details={'margin': '0', 'padding': '5px', 'text-decoration': 'underline'})))

        resource_balance_div = Div().add_style(
            style_obj=Style(style_details={'padding': '5px'}))
            # style_obj=Style(style_details={'border': '3px solid blue'}))
        resource_balance_div.add_element(Header(2, "Resource Balance:").add_style(
            Style(style_details={'margin': '0', 'padding': '5px', 'text-decoration': 'underline'})))

        for process_uid, process_details in workflow_dict['processes_dict'].items():
            # process = process_details['process_metadata']
            process_info_div = Div()
            process_info_style_dict = deepcopy(self.process_style.styles)
            # process_info_style_dict['border'] = '3px solid cyan'
            process_info_style = Style(style_details=process_info_style_dict)
            process_info_div.add_style(style_obj=process_info_style)

            time = process_details['process_time_seconds'] or 0
            process_info_list = [
                Span(f"Process to craft: {process_details['process_metadata']['name']}"),
                Span(f"Run Time: {time}"),
            ]
            if process_details['process_metadata']['description']:
                process_info_list.append(
                    Span(f"Description: {process_details['process_metadata']['description']}")
                )
            for span in process_info_list:
                span.add_style(style_obj=self.process_info_style)
                process_info_div.add_element(span)

            process_overview_div.add_element(process_info_div)
            # detailed_breakdown_div.add_element(process_info_div)

            consume_produce_div = Div().add_style(
                style_obj=Style(style_details={'display': 'inline-block', 'margin': '0', 'padding': '0px 20px 20px'}))
            consumes_div = Div()
            consumes_div.add_style(style_obj=self.process_style).add_style(
                Style({'float': 'left', 'margin': '0', 'padding': '0px 20px'}))
            if process_details['consumes_resources']:
                consumes_div.add_element(
                    Paragraph("Consumes:").add_style(
                        style_obj=self.process_consume_produce_info_style).add_style(
                            style_obj=Style(style_details={'margin': '0', 'padding': '0px', 'font-size': '110%'})
                        )
                )
                for resource_uid, amount in process_details['consumes_resources'].items():
                    resource = self.data_handler.find_resource(resource_uid)
                    consumes_div.add_element(
                        Paragraph(f"{resource.name}: {amount}").add_style(
                            style_obj=self.process_consume_produce_info_style)
                    )
                consume_produce_div.add_element(consumes_div)

            produces_div = Div()
            produces_div.add_style(style_obj=self.process_style).add_style(
                Style({'float': 'left', 'margin': '0', 'padding': '0px 20px'}))
            if process_details['produces_resources']:
                produces_div.add_element(
                    Paragraph("Produces:").add_style(style_obj=self.process_consume_produce_info_style).add_style(
                            style_obj=Style(style_details={'margin': '0', 'padding': '0px', 'font-size': '110%'})
                        )
                )
                for resource_uid, amount in process_details['produces_resources'].items():
                    resource = self.data_handler.find_resource(resource_uid)
                    produces_div.add_element(
                        Paragraph(f"{resource.name}: {amount}").add_style(
                            style_obj=self.process_consume_produce_info_style)
                    )
                consume_produce_div.add_element(produces_div)
            process_overview_div.add_element(consume_produce_div)

        data_div.add_element(process_overview_div)

        detailed_breakdwon_table = Table()

        max_consume_resource_count = 0
        max_produce_resource_count = 0
        for process_uid, process in workflow_dict['processes_dict'].items():
            max_consume_resource_count = max(
                max_consume_resource_count,
                len(process['consumes_resources']))
            max_produce_resource_count = max(
                max_produce_resource_count,
                len(process['produces_resources']))

        headers = ['Machine', 'Machine Count']
        [headers.extend([f'Input {i}', 'Units (U/s)']) for i in range(max_consume_resource_count)]
        [headers.extend([f'Output {i}', 'Units (U/s)']) for i in range(max_produce_resource_count)]
        headers.extend(['Time'])
        detailed_breakdwon_table_header_row = TableRow()
        for header in headers:
            detailed_breakdwon_table_header_row.add_element(TableHeader(header).add_style(style_obj=self.table_header_style))
        detailed_breakdwon_table.add_element(detailed_breakdwon_table_header_row)

        for process_uid, process_details in workflow_dict['processes_dict'].items():
            process = process_details['process_metadata']
            table_row = TableRow()

            # Machine
            machine_used = process_details['machine_used']
            parallel_count = process_details['process_count']
            table_row.add_element(TableData(internal=machine_used))
            table_row.add_element(TableData(internal=parallel_count))

            precision_multiplier = int(f"1{'0'*precision}")

            # Input
            consume_resource_dict = {}
            for index in range(max_consume_resource_count):
                try:
                    key = list(process_details['consumes_resources'].keys())[index]
                    value = process_details['consumes_resources'][key]
                except IndexError:
                    key = index
                    value = None
                consume_resource_dict[key] = value
            for consume_resource_uid, amount in consume_resource_dict.items():
                if amount is not None:
                    resource = self.data_handler.find_resource(consume_resource_uid)
                    name = resource.name
                    units = amount * process_details['process_count']
                    units_per_second = int((units / process_details['process_time_seconds']) * precision_multiplier) / precision_multiplier
                else:
                    name = '-'
                    units = '-'
                    units_per_second = '-'
                table_row.add_element(TableData(internal=name))
                table_row.add_element(TableData(internal=f"{units} ({units_per_second})"))

            # Output
            produce_resource_dict = {}
            for index in range(max_produce_resource_count):
                try:
                    key = list(process_details['produces_resources'].keys())[index]
                    value = process_details['produces_resources'][key]
                except IndexError:
                    key = index
                    value = None
                produce_resource_dict[key] = value
            for produce_resource_uid, amount in produce_resource_dict.items():
                if amount is not None:
                    resource = self.data_handler.find_resource(produce_resource_uid)
                    name = resource.name
                    units = amount * process_details['process_count']
                    units_per_second = int((units / process_details['process_time_seconds']) * precision_multiplier) / precision_multiplier
                else:
                    name = '-'
                    units = '-'
                    units_per_second = '-'
                table_row.add_element(TableData(internal=name))
                table_row.add_element(TableData(internal=f"{units} ({units_per_second})"))

            # Time
            table_row.add_element(TableData(internal=process_details['process_time_seconds']))

            for item in table_row.internal:
                item.add_style(style_obj=self.table_data_style)

            detailed_breakdwon_table.add_element(table_row)

        detailed_breakdown_div.add_element(detailed_breakdwon_table)
        data_div.add_element(detailed_breakdown_div)

        # Resource balance
        resource_balance = Table()
        headers = ['Resource', 'Consumed (U/s)', 'Produced (U/s)', 'NET (U/s)']
        resource_balance_header_row = TableRow()
        for header in headers:
            resource_balance_header_row.add_element(TableHeader(header).add_style(style_obj=self.table_header_style))
        resource_balance.add_element(resource_balance_header_row)

        for resource_uid, resource_balance_dict in workflow_dict['resources_dict'].items():
            resource = self.data_handler.find_resource(resource_uid)
            table_row = TableRow()
            table_row.add_element(TableData(internal=resource.name))
            consumed_per_second = resource_balance_dict['consumed_per_second']
            produced_per_second = resource_balance_dict['produced_per_second']
            net_per_second = produced_per_second - consumed_per_second
            table_row.add_element(TableData(internal=self.utils.round_up(consumed_per_second, decimal_places=3)))
            table_row.add_element(TableData(internal=self.utils.round_up(produced_per_second, decimal_places=3)))
            table_row.add_element(TableData(internal=self.utils.round_up(net_per_second, decimal_places=3)))
            for item in table_row.internal:
                item.add_style(style_obj=self.table_data_style)
            resource_balance.add_element(table_row)
        resource_balance_div.add_element(resource_balance)
        data_div.add_element(resource_balance_div)

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
