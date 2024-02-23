Feature: General Resource
    Scenario: Create Resource
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" in the project named "Test Project"
         Then I should see "Test Resource" in the saved resources
         When I capture the resource id for "Test Resource" and save it to index "next"
         Then I verify the resource at index "0" has not changed

    Scenario: Modify Resource
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" in the project named "Test Project"
         Then I should see "Test Resource" in the saved resources
         When I capture the resource id for "Test Resource" and save it to index "next"
         When I modify the resource at index "0" name to "Test Resource 2"
         Then I verify the resource at index "0" has changed

    Scenario: Delete Resource
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" in the project named "Test Project"
         Then I should see "Test Resource" in the saved resources
         When I delete the resource at index "0"
         Then I verify the resource at index "0" has been deleted

    Scenario: Export Resource
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" in the project named "Test Project"
         Then I verify the resources export "matches" "example_export_resources_1.json"

    Scenario: Import Resource
        Given I clear all test data
        Given I import resources from "example_import_resources.json"
         Then I verify the resources export "exactly matches" "example_export_resources_2.json"

# # Feature: Bad Data Resource
# # Feature: Erroring Resource
# Resource imported without project
