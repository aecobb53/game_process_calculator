Feature: Factorio
    Scenario: Testing
        Given I clear all test data
        # Given I import projects from "Example_Factorio/project_import.json"
        # Given I import resources from "Example_Factorio/resource_import.json"
        # Given I import processes from "Example_Factorio/process_import.json"
        Given I create a project with the name "Factorio"

        Given I create a resource with the name "Iron Plate" in the project named "Factorio"
        Given I create a resource with the name "Copper Plate" in the project named "Factorio"
        Given I create a resource with the name "Iron Gear" in the project named "Factorio"
        Given I create a resource with the name "Copper Cable" in the project named "Factorio"
        Given I create a resource with the name "Electronic circuit" in the project named "Factorio"
        Given I create a resource with the name "Transport Belt" in the project named "Factorio"
        Given I create a resource with the name "Inserter" in the project named "Factorio"
        Given I create a resource with the name "Green Science Pack" in the project named "Factorio"

        Given I create a process with the name "Iron Gear" in the project named "Factorio"
         When I capture the process id for "Iron Gear" and save it to index "next"
         When I modify the process id at index "0" to "consume" resource at index "0" in quantity "2"
         When I modify the process id at index "0" to "produce" resource at index "2" in quantity "1.5"

        Given I create a process with the name "Copper Cable" in the project named "Factorio"
         When I capture the process id for "Copper Cable" and save it to index "next"
         When I modify the process id at index "1" to "consume" resource at index "1" in quantity "1"
         When I modify the process id at index "1" to "produce" resource at index "3" in quantity "2"

        Given I create a process with the name "Electronic circuit" in the project named "Factorio"
         When I capture the process id for "Electronic circuit" and save it to index "next"
         When I modify the process id at index "2" to "consume" resource at index "3" in quantity "3"
         When I modify the process id at index "2" to "consume" resource at index "0" in quantity "1"
         When I modify the process id at index "2" to "produce" resource at index "4" in quantity "1"

        Given I create a process with the name "Transport Belt" in the project named "Factorio"
         When I capture the process id for "Transport Belt" and save it to index "next"
         When I modify the process id at index "3" to "consume" resource at index "2" in quantity "1"
         When I modify the process id at index "3" to "consume" resource at index "0" in quantity "1"
         When I modify the process id at index "3" to "produce" resource at index "5" in quantity "2"
         When I modify the process id at index "3" to have a "process" time of "0.5"

        Given I create a process with the name "Inserter" in the project named "Factorio"
         When I capture the process id for "Inserter" and save it to index "next"
         When I modify the process id at index "4" to "consume" resource at index "4" in quantity "1"
         When I modify the process id at index "4" to "consume" resource at index "2" in quantity "1"
         When I modify the process id at index "4" to "consume" resource at index "0" in quantity "1"
         When I modify the process id at index "4" to "produce" resource at index "6" in quantity "1"
         When I modify the process id at index "4" to have a "process" time of "0.5"

        Given I create a process with the name "Green Science Pack" in the project named "Factorio"
         When I capture the process id for "Green Science Pack" and save it to index "next"
         When I modify the process id at index "5" to "consume" resource at index "6" in quantity "1"
         When I modify the process id at index "5" to "consume" resource at index "5" in quantity "1"
         When I modify the process id at index "5" to "produce" resource at index "7" in quantity "1"
         When I modify the process id at index "5" to have a "process" time of "6"

        Given I create a workflow with the name "Green Science Pack" in the project named "Factorio" with the process_type of "LINEAR"
         When I capture the workflow id for "Green Science Pack" and save it to index "next"
         When I modify the workflow at index "0" "description" to "Does not go down to raw resource level"
         When I modify the workflow at index "0" to add resource at index "7" as a focus resource

         When I modify the workflow id at index "0" to include process at index "3"
         When I modify the workflow id at index "0" to include process at index "4"
         When I modify the workflow id at index "0" to include process at index "5"

        #  Then I want to look at the data
        #  Then I want to look at the data at a balance of "0.6" units per second

         Then I visualize workflow at index "0" with html and a units per second of "10"















        #  Then I verify the projects export "exactly matches" "Example_Factorio/project_export_1.json"
        #  Then I verify the projects export "exactly matches" "example_export_projects_2.json"

        # electronic ircuit 3 cable gives 1 iron yields 1 circuit
        # transport belt 1 gear and 1 iron yields 2 belts
        # inserter 1 circuit and 1 gear and 1 iron yields 1 inserter



    # Scenario: Inserter
    #     Given I clear all test data
    #     Given I create a project with the name "Factorio"

    # Scenario: Transport Belt
    # Scenario: Red Science Pack
    # Scenario: Green Science Pack
    # Scenario: Building out Factorio



#     Scenario: Modify Project
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Project" in the saved projects
#          When I capture the project id for "Test Project" and save it to index "next"
#          When I modify the project at index "0" name to "Test Project 2"
#          Then I verify the project at index "0" has changed

#     Scenario: Delete Project
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Project" in the saved projects
#          When I delete the project at index "0"
#          Then I verify the project at index "0" has been deleted

#     Scenario: Export Project
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I verify the projects export "matches" "example_export_projects_1.json"

#     Scenario: Import Project
#         Given I clear all test data
#         Given I import projects from "example_import_projects.json"
#          Then I verify the projects export "exactly matches" "example_export_projects_2.json"

# # Feature: Bad Data Project
# # Feature: Erroring Project
