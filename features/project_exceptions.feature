Feature: Project Exceptions
    Scenario: I post duplicate records
        Given I clear all test data
        Given I create a project with the name "Test Project"
         Then I create a project with the name "Test Project" should have a status code of "409"

    Scenario: I cant find a specific project
        Given I clear all test data
        # Given I create a project with the name "Test Project"
        # When I search for a project with the name "Test Project"
        Then I should not find a project with the uid "1b7020bf-8b2e-4b10-ba28-d74de37e5cad"
