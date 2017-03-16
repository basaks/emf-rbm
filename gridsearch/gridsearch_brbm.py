import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import binarize
from sklearn.neural_network import BernoulliRBM
from emfrbm.rbm_datasets import load_omniglot_iwae, load_mnist_realval

# omniglot data
# X_train, Y_train, _, X_test, Y_test, _ = load_omniglot_iwae()

# mnist realvals
X_train, Y_train, x_valid, targets_valid, X_test, Y_test = \
    load_mnist_realval()


logistic = linear_model.LogisticRegression()


class BRBMTh(BernoulliRBM):
    """ A wrapper class for optimising threshold via GridsearchCV"""

    def __init__(self, n_components=256, learning_rate=0.005, batch_size=100,
                 n_iter=20, verbose=0, random_state=None, threshhold=0.5):
        super(BRBMTh, self).__init__(n_components=n_components,
                                     learning_rate=learning_rate,
                                     batch_size=batch_size,
                                     n_iter=n_iter,
                                     verbose=verbose,
                                     random_state=random_state)
        self.threshhold = threshhold

    def fit(self, X, y=None):
        X_t = binarize(X, threshold=self.threshhold, copy=True)
        return super(BRBMTh, self).fit(X_t, y)

    def transform(self, X):
        X_t = binarize(X, threshold=self.threshhold, copy=True)
        return super(BRBMTh, self).transform(X_t)

emf_rbm = BRBMTh(verbose=True)

classifier = Pipeline(steps=[('rbm', emf_rbm), ('logistic', logistic)])

param_dict = {'rbm__n_iter': [20],
              'rbm__learning_rate': [0.01],
              'rbm__threshhold': [0.4, 0.5, 0.6],
              'logistic__C': [1.0, 1.0e2, 1.0e4]}

estimator = GridSearchCV(classifier,
                         param_dict,
                         n_jobs=6,
                         iid=False,
                         pre_dispatch='2*n_jobs',
                         verbose=True,
                         cv=3)

estimator.fit(X=X_train, y=Y_train)

pd.DataFrame.from_dict(
    estimator.cv_results_).sort_values(by='rank_test_score').to_csv(
    'bernoulli_rbm.csv')
