from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

class NaturalisticStimuli(object):
    """
    Data object to model naturalistic stimuli, like movies

    Parameters
    ----------

    stimulus : list
        A list of text samples describing events within a stimulus

    recall : list
        A list of text samples from from a recall event, such as sentences that
        verbally describe some stimulus

    n_features : int
        Number of text features used in vectorized representation of text
        samples (default: 1000)

    n_topics : int
        Number of topics used to model the text data (default: 100)

    stimulus_overlap : int
        Size of overlap in text samples used to fit topic model of stimulus
        (default: 50)

    recall_overlap : int
        Size of overlap in text samples used to transform recall samples
        (default: 5)

    vectorizer_params : dict
        Dictionary of parameters used to generate the vectorized representation
        of text samples for finer control (optional)

     topic_params : dict
        Dictionary of parameters used to generate topic model of stimulus for
        finer control (optional)
    """

    def __init__(self, stimulus=None, recall=None, n_features=1000, n_topics=100,
                 stimulus_overlap=50, recall_overlap=5, vectorizer_params=None,
                 topic_params=None):

        # initialize default CountVectorizer parameters
        self.v_params = dict(
            max_df=0.95,
            min_df=2,
            max_features=n_features,
            stop_words='english'
        )

        # update CountVectorizer parameters if there are any
        if vectorizer_params is not None:
            self.v_params.update(vectorizer_params)

        # initialize default LatentDirichletAllocation model parameters
        self.t_params = dict(
            n_topics=n_topics,
            max_iter=5,
            learning_method='online',
            learning_offset=50.
        )

        # update LatentDirichletAllocation parameters if there are any
        if topic_params is not None:
            self.t_params.update(topic_params)

    def fit(self):
        """
        Fit the stimulus model
        """

        # initialize vectorizer
        vectorizer = CountVectorizer(**self.v_params)

        # initialize lda
        lda = LatentDirichletAllocation(**self.t_params)

        # create pipeline
        model = Pipeline([('vectorizer', vectorizer), ('lda', lda)])

        # fit the model
        model.fit(self.stimulus)
