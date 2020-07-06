from sklearn import tree
import matplotlib.pyplot as plt
import datetime
import storage.constants as constants

def plotAndSaveTree8Channels(model, ratioAugSamples):
    tree.plot_tree(model,
                   max_depth=3,
                   class_names=['no augmentation', 'augmentation'],
                   feature_names=['rmsCh1', 'rmsCh2', 'rmsCh3', 'rmsCh4', 'rmsCh5', 'rmsCh6', 'rmsCh7', 'rmsCh8',
                                  'pairw12', 'pairw13', 'pairw14', 'pairw15', 'pairw16', 'pairw17', 'pairw18',
                                  'pairw23', 'pairw24', 'pairw25', 'pairw26', 'pairw27', 'pairw28',
                                  'pairw34', 'pairw35', 'pairw36', 'pairw37', 'pairw38',
                                  'pairw45', 'pairw46', 'pairw47', 'pairw48',
                                  'pairw56', 'pairw57', 'pairw58',
                                  'pairw67', 'pairw68',
                                  'pairw78'],
                   label='all',
                   fontsize=6)

    title = constants.fileNameOfRecording + " (win-sz " + str(constants.windowSize) + ", n-a samples " \
            + str(constants.amtNonAugSamples) \
            + ", a-samp rate " + str(round(ratioAugSamples, 2)) + ")"
    #TODO adjusted for study
    path = constants.savePath + getPlotTitle(constants.fileNameOfRecording)+".png"
    #path = "./plots/decisionTrees/" + getPlotTitle(constants.fileNameOfRecording) + ".png"
    plt.savefig(path)

    #plt.show()

def getPlotTitle(plotTitle):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H.%M.%S_")+plotTitle


