from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np

def generic_random_split(X, y): 
    """ X: features matrix
        y: classes
        Returns: X_train, y_train, X_validation, y_validation, X_test, y_test
    """
    X = np.array(X)
    y = np.array(y)
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, train_size=0.8, random_state=0)
    
    for fold, (train_index, test_index) in enumerate(sss.split(X, y)):
        # get X_train and y_train, as 0.8 of the data
        X_train = X[train_index]
        y_train = y[train_index]
        # 0.2 of the data, to further split into validation and testing
        test_valid = test_index

    # stratified split on the test set
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.5, train_size=0.5, random_state=0)

    for fold, (valid_index, test_index) in enumerate(sss.split(X[test_valid], y[test_valid])):
        X_test = X[test_valid[test_index]]
        y_test = y[test_valid[test_index]]
        X_validation = X[test_valid[valid_index]]
        y_validation = y[test_valid[valid_index]]

    return X_train, y_train, X_validation, y_validation, X_test, y_test


# use:
# import random_split
# X_train, y_train, X_validation, y_validation, X_test, y_test = random_split.generic_random_split(X, y)
# Print(X_train.shape, y_train.shape, X_validation.shape, y_validation.shape, X_test.shape, y_test.shape)
