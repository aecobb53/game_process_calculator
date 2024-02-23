Feature: General Workflow
    Scenario: Create Workflow
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I should see "Test Workflow" in the saved workflows
         When I capture the workflow id for "Test Workflow" and save it to index "next"
         Then I verify the workflow at index "0" has not changed

    Scenario: Modify Workflow
        Given I clear all test data
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I should see "Test Workflow" in the saved workflows
         When I capture the workflow id for "Test Workflow" and save it to index "next"
         When I modify the workflow at index "0" name to "Test Workflow 2"
         Then I verify the workflow at index "0" has changed

    Scenario: Delete Workflow
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I should see "Test Workflow" in the saved workflows
         When I delete the workflow at index "0"
         Then I verify the workflow at index "0" has been deleted

    Scenario: Export Workflow
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I verify the workflows export "matches" "example_export_workflows_1.json"

    Scenario: Import Workflow
        Given I clear all test data
        Given I import workflows from "example_import_workflows.json"
         Then I verify the workflows export "exactly matches" "example_export_workflows_2.json"

    Scenario: Linear Workflow
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I should see "Test Workflow" in the saved workflows

         When I capture the process id for "Test Process One" and save it to index "next"
         When I capture the process id for "Test Process Two" and save it to index "next"

         When I modify the process id at index "0" to "consume" resource at index "0" in quantity "10"
         When I modify the process id at index "0" to "produce" resource at index "1" in quantity "1.5"
         When I modify the process id at index "1" to "consume" resource at index "1" in quantity "0.125"
         When I modify the process id at index "1" to "produce" resource at index "2" in quantity "1"

         When I capture the workflow id for "Test Workflow" and save it to index "next"
         When I modify the workflow id at index "0" to include process at index "0"
         When I modify the workflow id at index "0" to include process at index "1"

    Scenario: Workflow Google Sheets Export
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource One" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Two" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Three" in the project named "Test Project"
        Given I create a process with the name "Test Process One" in the project named "Test Project"
        Given I create a process with the name "Test Process Two" in the project named "Test Project"
        Given I create a workflow with the name "Test Workflow" in the project named "Test Project" with the process_type of "LINEAR"
         Then I should see "Test Workflow" in the saved workflows

         When I capture the process id for "Test Process One" and save it to index "next"
         When I capture the process id for "Test Process Two" and save it to index "next"

         When I modify the process id at index "0" to "consume" resource at index "0" in quantity "10"
         When I modify the process id at index "0" to "produce" resource at index "1" in quantity "1.5"
         When I modify the process id at index "1" to "consume" resource at index "1" in quantity "0.125"
         When I modify the process id at index "1" to "produce" resource at index "2" in quantity "1"

         When I capture the workflow id for "Test Workflow" and save it to index "next"
         When I modify the workflow id at index "0" to include process at index "0"
         When I modify the workflow id at index "0" to include process at index "1"

         Then I want to look at the data
        #  Then I verify the workflows export "matches" "example_export_workflows_3.json"

        #  Then I verify the workflow at index "0" has not changed

# # # Feature: Bad Data Workflow
# # # Feature: Erroring Workflow
# # Workflow imported without project
