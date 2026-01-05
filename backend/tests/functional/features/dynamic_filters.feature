Feature: Dynamic filters based on actual data
  As a user of the Offer Search extension
  I want to see only relevant filter options based on my scraped jobs
  So that I don't see irrelevant filters like Indeed when I only have LinkedIn jobs

  Background:
    Given the API is running
    And the database is empty

  Scenario: Get available sources when database is empty
    When I request the job stats
    Then the API should respond with status code 200
    And the jobs_by_source should be empty

  Scenario: Get available sources with LinkedIn jobs only
    Given I have submitted 5 job offers from "linkedin"
    When I request the job stats
    Then the API should respond with status code 200
    And the jobs_by_source should contain "linkedin" with count 5
    And the jobs_by_source should not contain "indeed"

  Scenario: Get available sources with multiple sources
    Given I have submitted 3 job offers from "linkedin"
    And I have submitted 2 job offers from "indeed"
    When I request the job stats
    Then the API should respond with status code 200
    And the jobs_by_source should contain "linkedin" with count 3
    And the jobs_by_source should contain "indeed" with count 2
    And the jobs_by_source should not contain "leboncoin"

  Scenario: Source filter options are updated after new scraping
    Given I have submitted 5 job offers from "linkedin"
    When I request the job stats
    Then the jobs_by_source should contain only "linkedin"
    When I submit 3 new job offers from "indeed"
    And I request the job stats again
    Then the jobs_by_source should contain "linkedin" with count 5
    And the jobs_by_source should contain "indeed" with count 3

  Scenario: Stats include total counts for metadata
    Given I have submitted 10 job offers from different companies and locations
    When I request the job stats
    Then the API should respond with status code 200
    And the total_jobs should be 10
    And the total_companies should be greater than 0
    And the total_locations should be greater than 0
    And the jobs_by_source should contain at least one source
