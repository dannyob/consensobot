@ircserver
Feature: command line IRC management
    In order that Consenso's IRC presence can be controlled easily
    As a CLI user
    I want to be able to ask Consenso to join and leave IRC channels, and announce things

    Scenario: Have mock IRC server
        Given a mock IRC server on localhost:4567
        Then the mock IRC server should output 'Running on port 4567, localhost' within 1 seconds

    Scenario: Go online
        Given a mock IRC server on localhost:4567
        When I type 'consensobot irc_join "irc://localhost:4567/#test"'
        Then the mock IRC server should output 'consensobot joined test' within 1 seconds
        And the mock IRC server should not output 'consensobot left test' within 1 seconds

    Scenario: Go offline
        Given a mock IRC server on localhost:4567
        When I type 'consensobot irc_join "irc://localhost:4567/#test2"'
        When I type 'consensobot irc_leave "irc://localhost:4567/#test2"'
        Then the mock IRC server should output 'consensobot left test2' within 1 seconds

    Scenario: Announce something
        When I type 'consensobot irc_join "irc://localhost:4567/#test"'
        And I type 'consensobot irc_announce "Freedom for the progletariat"'
        Then the mock IRC server should output 'consensobot said Freedom for the progletariat on test' within 1 seconds
