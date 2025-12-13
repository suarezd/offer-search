Feature: Submit job offers
  As a LinkedIn scraper extension
  I want to submit scraped job offers to the API
  So that they can be stored and searched later

  Background:
    Given the API is running
    And the database is empty

  Scenario: Submit a single valid job offer
    Given I have scraped 1 job offers from LinkedIn
    When I submit the job offer to the API
    Then the API should respond with status code 200
    And the response should indicate 1 job inserted
    And the response should indicate 0 duplicates

  Scenario: Submit multiple job offers
    Given I have scraped 5 job offers from LinkedIn
    When I submit all job offers to the API
    Then the API should respond with status code 200
    And the response should indicate 5 jobs inserted
    And the response should indicate 0 duplicates

  Scenario: Submit duplicate job offers
    Given I have already submitted a job offer with id "linkedin-123"
    When I submit the same job offer again
    Then the API should respond with status code 200
    And the response should indicate 0 jobs inserted
    And the response should indicate 1 duplicate
    And the duplicate id should be "linkedin-123"

  Scenario: Submit mix of new and duplicate job offers
    Given I have already submitted 2 job offers
    And I have scraped 3 new job offers from LinkedIn
    When I submit all 5 job offers to the API
    Then the API should respond with status code 200
    And the response should indicate 3 jobs inserted
    And the response should indicate 2 duplicates

  Scenario: Submit job offer with missing required field
    Given I have a job offer missing the "title" field
    When I submit the job offer to the API
    Then the API should respond with status code 422
    And the response should indicate a validation error

  Scenario: Submit job offer with invalid field length
    Given I have a job offer with a title longer than 255 characters
    When I submit the job offer to the API
    Then the API should respond with status code 422
    And the response should indicate a validation error
