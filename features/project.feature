Feature: General Project

    Scenario: Create Project
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Then I should see "Test Project" in the saved projects

    Scenario: Modify Project
        Given I clear all test data
        Given I create a project with the name "Test Project"
         Then I should see "Test Project" in the saved projects
         When I capture the project id for "Test Project" and save it to index "next"
         When I modify the project at index "0" name to "Test Project 2"
    #     #  Then I should see "Test Project 2" in the saved projects



    # # #  Given we have behave installed
    # #   When we implement a test
    # #   Then behave will test it for us!