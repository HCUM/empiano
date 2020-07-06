import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import storage.constants as constants

def plotConfusionMatrix(y_true, y_pred, classes,
                        ratioAugSamples,
                        normalize=False,
                        title=None,
                        cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    titleToSave = title
    title = title + " (win-sz " + str(constants.windowSize) + ", n-a samples " \
            + str(constants.amtNonAugSamples) \
            + ", a-samp rate " + str(round(ratioAugSamples, 2)) + ")"
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    print("Confusion matrix: \n", cm)
    print("real augmentation/augmentation         real augmentation/no augmentation\n")
    print("real no augmentation/augmentation      real no augmentation/no augmentation\n")

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()

    plt.title(title, fontsize= 9)
    path = "./plots/confusionMatrix/"+getPlotTitle(titleToSave) + ".png"
    plt.savefig(path)
    plt.show()

def getPlotTitle(plotTitle):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H.%M.%S_")+plotTitle