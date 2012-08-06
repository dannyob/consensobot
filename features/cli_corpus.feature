Feature: command line corpus management
    In order that Consenso can learn more about Anarchist texts
    As a CLI user
    I want to be able to control the markov chain corpus

    Scenario: Add a corpus
        Given an empty set of texts in the corpus
        When I type 'consensobot add_text test_data/test_corpus.txt'
        Then the CLI should output 'I have learned test_data/test_corpus.txt'
        And there should be 1 text in the corpus


