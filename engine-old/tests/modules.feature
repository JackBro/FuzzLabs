Feature: loading engine modules

  Scenario: load the modules
      Given we have root and config
       When we load the modules
       Then we get a list of modules

  Scenario: unload the modules
      Given we have modules loaded
       When we unload the modules
       Then we get an empty list

