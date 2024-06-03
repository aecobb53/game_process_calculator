Feature: Resource Exceptions
    Scenario: Create Resource without Project
        Given I clear all test data
         Then I create a resource with the name "Test Resource" in the project named "Test Project" should have a status code of "400"

    Scenario: Create duplicate records
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" in the project named "Test Project"
         Then I create a resource with the name "Test Resource" in the project named "Test Project" should have a status code of "409"


# # Feature: Bad Data Resource
# # Feature: Erroring Resource
# Resource imported without project
