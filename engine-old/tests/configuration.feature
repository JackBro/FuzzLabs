Feature: loading engine configuration

  Scenario: load the configuration
      Given we have a configuration file
       When we read the configuration
       Then we get a dictionary
