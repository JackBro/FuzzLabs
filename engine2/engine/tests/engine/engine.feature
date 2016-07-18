Feature: Engine API Authentication

  Scenario: set up master client
     Given the engine is accessible
      When we attempt to initialize ACL
      Then we get no error

  Scenario: set up master client again
     Given the engine is accessible
      When we attempt to initialize ACL
      Then we get forbidden message

  Scenario: set up API key
     Given the engine is accessible
      When we attempt to set up the API key
      Then the API key is returned

  Scenario: call to set up API key again
     Given the engine is accessible
      When we attempt to set up the API key
      Then we get forbidden message

  Scenario: call to ping
     Given the engine is accessible
      When we attempt a ping request
      Then we get pong response

