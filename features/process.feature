Feature: General Process
    Scenario: Create Process
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource In" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Out" in the project named "Test Project"
        Given I create a process with the name "Test Process" in the project named "Test Project"
         Then I should see "Test Process" in the saved processes
         When I capture the process id for "Test Process" and save it to index "next"
         Then I verify the process at index "0" has not changed

    Scenario: Modify Process
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource In" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Out" in the project named "Test Project"
        Given I create a process with the name "Test Process" in the project named "Test Project"
         Then I should see "Test Process" in the saved processes
         When I capture the process id for "Test Process" and save it to index "next"
         When I modify the process at index "0" name to "Test Process 2"
         Then I verify the process at index "0" has changed
         When I modify the process id at index "0" to "consume" resource at index "0" in quantity "1"
         When I modify the process id at index "0" to "produce" resource at index "1" in quantity "1.5"

    Scenario: Delete Process
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource In" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Out" in the project named "Test Project"
        Given I create a process with the name "Test Process" in the project named "Test Project"
         Then I should see "Test Process" in the saved processes
         When I delete the process at index "0"
         Then I verify the process at index "0" has been deleted

    Scenario: Export Process
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource In" in the project named "Test Project"
        Given I create a resource with the name "Test Resource Out" in the project named "Test Project"
        Given I create a process with the name "Test Process" in the project named "Test Project"
         Then I verify the processes export "matches" "example_export_processes_1.json"

    Scenario: Import Process
        Given I clear all test data
        Given I import processes from "example_import_processes.json"
         Then I verify the processes export "exactly matches" "example_export_processes_2.json"

# # Feature: Bad Data Process
# # Feature: Erroring Process
# Process imported without project
