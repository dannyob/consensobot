Feature: command line corpus management
    In order that Consenso can learn more about Anarchist texts
    As a CLI user
    I want to be able to control the markov chain corpus

    Scenario: Add a corpus
        Given an empty set of texts in the corpus
        When I type 'consensobot add_text test_data/test_corpus.txt'
        Then the CLI should output 'I have learned test_data/test_corpus.txt'
        And there should be 1 text in the corpus

    Scenario: List a corpus
        Given an empty set of texts in the corpus
        When I type 'consensobot add_text test_data/test_corpus.txt'
        And I type 'consensobot list_text'
        Then the CLI should output 'test_corpus.txt "Anarchism & American Traditions"'

    Scenario: Delete a corpus
        Given an empty set of texts in the corpus
        When I type 'consensobot add_text test_data/test_corpus.txt'
        And I type 'consensobot delete_text test_corpus.txt'
        Then the CLI should output 'I have forgotten test_corpus.txt'
        And there should be 0 text in the corpus


    Scenario: Markov me some sentences
        Given an empty set of texts in the corpus
        When I type 'consensobot add_text test_data/test_corpus.txt'
        When I type 'consensobot markov 1 --start-word Pontefract'
        Then the CLI should output 'Miserabilis'

