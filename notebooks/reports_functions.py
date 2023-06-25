import matplotlib.pyplot as plt
import numpy as np
import time
import itertools
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 
          'jazz', 'metal', 'pop', 'reggae', 'rock']

def plot_confusion_matrix(y_test, y_pred, save_as:str, title:str='Confusion Matrix'):
    # create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    if not isinstance(save_as, str):
        save_as = f'conf_matrix_{time.time()}.png'

    accuracy = np.trace(cm) / np.sum(cm).astype('float')
    misclass = 1 - accuracy

    cmap = plt.get_cmap('Blues')

    # plot confusion matrix
    plt.figure(figsize=(8,6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(GENRES))
    plt.xticks(tick_marks, GENRES, rotation=45)
    plt.yticks(tick_marks, GENRES)

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "{:,}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > (cm.max() / 2) else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.savefig(save_as)

def cross_validation_accuracy(model, X, y, n_splits=30,  save_as:str=None, title:str='Cross-Validation Scores'):
    
    if not isinstance(save_as, str):
        save_as = f'cross_val_score_{time.time()}.png'

    strKfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=0)
 
    scores = cross_val_score(model,X, y, cv=strKfold)

    print('scores: ', scores)
    print('mean: ', scores.mean())

    plt.figure(figsize=(8,6))
    plt.title(title)
    plt.xlabel('Fold')
    plt.ylabel('Score')
    ax = plt.gca()
    ax.set_xlim(1, n_splits+0.1)
    ax.set_ylim(0, 1.005)
    plt.grid()
    plt.plot(range(1,n_splits+1), scores, 'o-', color='blue', lw=2)
    plt.plot(range(1,n_splits+1), [scores.mean()]*5, linestyle="-.", color='k')
    plt.annotate("%0.4f" % scores.mean(), (3, scores.mean() + 0.005))
    plt.legend(['accuracy','mean acc'],loc="best")
    plt.savefig(save_as)