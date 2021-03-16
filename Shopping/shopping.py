import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    
    with open(filename, 'r') as file:
        column = list(csv.DictReader(file))

        
        evidence = list()
        labels = list()
        integer = ['Administrative','Informational','ProductRelated','OperatingSystems','Browser','Region','TrafficType']
        nfloat = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
        index_month = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']

        for header in column:
            row = list()

            for name in header:
            
                if name != 'Revenue':
                #declare as integer
                    if name in integer:
                        header[name] = int(header[name])
                    
                    #declare as floating number
                    if name in nfloat:
                        header[name] = float(header[name])

                    #declare Month, an index from 0 (January) to 11 (December)
                    if name == 'Month':
                        for index in range(12):
                            if header[name] == index_month[index]:
                                header[name] = index

                    #declare VisitorType, an integer 0 (not returning) or 1 (returning)
                    if name == 'VisitorType':
                        if header[name] == 'Returning_Visitor':
                            header[name] = int(1)
                        else:
                            header[name] = int(0)

                    #declare Weekend, an integer 0 (if false) or 1 (if true)
                    if name == 'Weekend':
                        if header[name] == 'TRUE':
                            header[name] = int(1)
                        elif header[name] == 'FALSE':
                            header[name] = int(0)

                    #label is 1 if Revenue is true, and 0 otherwise.
                    
                    row.append(header[name])
                
                if name == 'Revenue':
                    if header[name] == 'TRUE':
                        header[name] = int(1)
                    elif header[name] == 'FALSE':
                        header[name] = int(0)
                    labels.append(header[name])

            evidence.append(row)
            
        return(evidence,labels)
                


            


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    specificity = float(0)
    sensitivity = float(0)

    for i in range(len(labels)):
            if labels[i] == predictions[i] and predictions[i] == 1:
                true_positive += 1
            if labels[i] == predictions[i] and predictions[i] == 0:
                true_negative += 1
            if labels[i] != predictions[i] and predictions[i] == 1:
                false_positive += 1
            if labels[i] != predictions[i] and predictions[i] == 0:
                false_negative += 1

    sensitivity = true_positive/(true_positive + false_negative)
    specificty = true_negative/(true_negative + false_positive)

    return(sensitivity,specificty)
                

    

if __name__ == "__main__":
    main()
