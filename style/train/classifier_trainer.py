import json
from pathlib import PosixPath

from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from style.constants import FILE_PATH_BOOK_DS, MODEL_EXPORT_PATH
from style.dataset.reader import Dataset, DatasetReader
from style.predict.servable.base import SklearnBasedClassifierServable


class TextNormalizer:
    pass


def split_dataset(
    dataset: Dataset,
    test_percentage: float = 0.2,
    random_state: int = 42,
):
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=test_percentage,
        random_state=random_state,
    )
    return docs_train, docs_test, y_train, y_test, dataset.target


def train_sklearn_classification_model(
    docs_train,
    docs_test,
    y_train,
    y_test,
    dataset_target,
    pipeline: Pipeline,
    grid_search_params: dict,
    cv: int = 5,
):
    """This method trains multiple models via GridSearchCV and it creates a servable
    from the best model.

    See https://scikit-learn.org/stable/tutorial/statistical_inference
    /putting_together.html for more details.


    """

    grid_search = GridSearchCV(
        pipeline, grid_search_params, scoring="f1_weighted", n_jobs=-1, cv=cv
    )
    grid_search.fit(docs_train, y_train)
    y_predicted = grid_search.predict(docs_test)

    report = metrics.classification_report(
        y_test, y_predicted, target_names=set(dataset_target), output_dict=True
    )
    confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)

    return (
        grid_search,
        report["weighted avg"]["f1-score"],
        report,
        confusion_matrix,
    )


# Q: burayi a yapmayinca eklemiyor. w ile sadece ustunu yazip eziyor.


def write_report_and_cm(
    report, model_name, confusion_matrix, export_path: PosixPath
):
    report_fn = export_path / f"{model_name}-report.txt"
    with open(report_fn, "wt") as f:
        f.write(json.dumps(report))
        print(f"The report is saved successfully at {report_fn}")

    conf_matrix_fn = export_path / f"{model_name}-cm.txt"
    with open(conf_matrix_fn, "wt") as f:
        f.write(f"{str(confusion_matrix)}\n")
        print(f"The confusion matrix is saved successfully at {conf_matrix_fn}")


def export(model, export_path):
    """
        # When the model is ready, initiate it and return at the end.
    # from style.predict.servable.base import SklearnBasedClassifierServable
    # servable = SklearnBasedClassifierServable(model=model).export(export_path)
    Returns:

    """
    SklearnBasedClassifierServable(model=model).export(export_path)


def create_pipeline(clf_name, estimator, normalize=False, reduction=False):
    steps = [
        (
            "vectorize",
            TfidfVectorizer(analyzer="word", use_idf=True, lowercase=True),
        )
    ]

    if normalize:
        steps.insert(0, ("normalize", TextNormalizer()))

    if reduction:
        steps.append(("reduction", TruncatedSVD(n_components=10000)))

    # Add the estimator
    steps.append((clf_name, estimator))
    return Pipeline(steps)


def run():
    import argparse

    parser = argparse.ArgumentParser(
        description="Train Classifier for Style Project"
    )
    parser.add_argument(
        "--model-name", type=str, help="Model name to export", required=True
    )
    parser.add_argument(
        "--train-data-size",
        type=int,
        help="Training data max size",
        default=-1,
        required=False,
    )

    args = parser.parse_args()
    model_name = args.model_name
    train_data_size = args.train_data_size

    model_export_path = MODEL_EXPORT_PATH / model_name
    classifiers = [
        ("clf_svc", LinearSVC),
        ("clf_lg", LogisticRegression),
        ("clf_sgd", SGDClassifier),
    ]

    parameters = [
        {
            "vectorize__ngram_range": [(2, 3), (2, 4)],
            "clf_svc__C": [0.01, 0.1, 1, 10],
        },
        {"vectorize__ngram_range": [(2, 3), (2, 4)]},
        {"vectorize__ngram_range": [(2, 3), (2, 4)]},
    ]

    dataset = DatasetReader.load_files(FILE_PATH_BOOK_DS)
    print(f"Dataset size is {len(dataset)}")
    if train_data_size != -1:
        dataset = dataset[:train_data_size]
        print(f"Dataset size is going to be {len(dataset)}")

    dataset.shuffle()
    docs_train, docs_test, y_train, y_test, dataset_target = split_dataset(
        dataset
    )

    best_model = None
    best_model_score = -1
    best_model_report = None
    best_model_cm = None
    # TODO remove the
    for (name, clf), params in list(zip(classifiers, parameters))[1:2]:
        pipeline = create_pipeline(name, clf())
        grid_search, f1_score, report, cm = train_sklearn_classification_model(
            docs_train,
            docs_test,
            y_train,
            y_test,
            dataset_target,
            pipeline,
            params,
            cv=3,
        )

        if best_model_score <= f1_score:
            best_model = grid_search.best_estimator_
            best_model_score = f1_score
            best_model_report = report
            best_model_cm = cm
            print(
                f"Best Estimator score now is {best_model_score} and the model is "
                f"{best_model}"
            )

    print(
        f"Best model is {best_model} with score of: {best_model_score} with params of "
        f"{best_model.get_params()}"
    )
    print("Training the best model with the whole data")
    best_model.fit(X=dataset.data, y=dataset.target)
    export(best_model, model_export_path)
    print(f"The best model is written to {model_export_path}")
    # Provide print for the best model details and
    write_report_and_cm(
        best_model_report, model_name, best_model_cm, MODEL_EXPORT_PATH
    )


if __name__ == "__main__":
    run()
