from collections import defaultdict as dd
import csv
import datetime
import os
from pathlib import Path, PosixPath

from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from common.clients.google_storage_client import (
    get_storage_client,
)
from style.config import style_app_settings
from style.constants import FILE_PATH_BOOK_DS, MODEL_EXPORT_PATH
from style.dataset.reader import (
    Dataset,
    DatasetReader,
)
from style.predict.servable.base import SklearnBasedClassifierServable

storage_client = get_storage_client(style_app_settings.MISC_BUCKET)


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
    pipeline: Pipeline,
    grid_search_params: dict,
    n_jobs: int,
    cv: int = 5,
):

    """This method trains multiple models via GridSearchCV and it creates a servable
    from the best model.

    See https://scikit-learn.org/stable/tutorial/statistical_inference
    /putting_together.html for more details.


    """

    grid_search = GridSearchCV(
        pipeline, grid_search_params, n_jobs=n_jobs, cv=cv
    )
    grid_search.fit(docs_train, y_train)
    y_predicted = grid_search.predict(docs_test)

    report_ = metrics.classification_report(
        y_test, y_predicted, output_dict=False
    )

    report_dict = metrics.classification_report(
        y_test, y_predicted, output_dict=True
    )

    confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)

    return grid_search.best_estimator_, report_, report_dict, confusion_matrix


def report(report_, name, confusion_matrix, export_path: PosixPath):
    with open(export_path / f"{name}-report.txt", "w") as f:
        f.write(report_)
        print(f"The report is saved successfully, under {export_path}")
    with open(export_path / f"{name}-cm.txt", "w") as f:
        f.write(f"{str(confusion_matrix)}\n")
        print(
            f"The confusion matrix is saved successfully, under {export_path}"
        )


def model_comparison_report(export_path, params, results):
    # What will it print?
    """
    Model names and their metric pairs (F1 score by weighted average)
    document length
    cv
    test_percentage

    normalization
    reduction

    Returns:

    """
    # prefix = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    with open(export_path / "model_comparison_report.tsv", "w") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        tsv_writer.writerow(["model_name", "f1-score", "ngram"])
        for model_name, values in results.items():
            tsv_writer.writerow(
                [model_name, values["f1-weighted-avg"], values["best-ngram"]]
            )
        tsv_writer.writerow("")
        params = sorted(params.items())
        for k, v in params:
            tsv_writer.writerow([k, v])

    print(
        f"The model comparison report is saved successfully, under {export_path}"
    )


def export(model, export_path):
    """
        # When the model is ready, initiate it and return at the end.
    # from style.predict.servable.base import SklearnBasedClassifierServable
    # servable = SklearnBasedClassifierServable(model=model).export(export_path)
    Returns:

    """
    SklearnBasedClassifierServable(model=model).export(export_path)


def create_pipeline(
    clf_name,
    estimator,
    normalize=False,
    reduction=False,
    min_df=3,
):
    steps = [
        (
            "vectorize",
            TfidfVectorizer(
                min_df=min_df,
                max_features=None,
                strip_accents="unicode",
                analyzer="word",
                token_pattern=r"\w{1,}",
                ngram_range=(1, 1),
                use_idf=1,
                smooth_idf=1,
                sublinear_tf=1,
                stop_words="english",
            ),
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
        description="Parameterize data preparation process models."
    )
    # Parameters related with data preparation
    parser.add_argument(
        "--num_books", type=int, help="Number of books for subsetting data"
    )
    parser.add_argument(
        "--document_length",
        type=int,
        default=style_app_settings.DOCUMENT_LENGTH,
        help="Number of words that a document contains",
    )
    parser.add_argument(
        "--test_percentage",
        type=float,
        default=style_app_settings.TEST_PERCENTAGE,
    )

    parser.add_argument(
        "--cross_validation",
        type=int,
        default=style_app_settings.CROSS_VALIDATION,
        help="argument for grid search",
    )
    parser.add_argument(
        "--normalize", action="store_true", help="Normalize text"
    )
    parser.add_argument(
        "--reduction", action="store_true", help="Truncated SVD"
    )

    # Paramaters related with vectorization (tf-idf)
    parser.add_argument(
        "--min_df",
        type=int,
        default=style_app_settings.MIN_DF,
        help="means ignore terms that appear in less than 5 documents or ignore terms "
        "that appear in less than 1% of the documents",
    )

    parser.add_argument(
        "--ngram_min", default=style_app_settings.NGRAM_MIN, type=int
    )

    parser.add_argument(
        "--ngram_max", default=style_app_settings.NGRAM_MAX, type=int
    )

    parser.add_argument(
        "--num_doc",
        default=style_app_settings.NUM_DOC,
        type=int,
        help="It is a Resample_balanced method parameter. It specifies the number of "
        "documents for every author should have.",
    )
    parser.add_argument(
        "--resampling_percentage",
        default=1.0,
        type=float,
        help="Size of resampling",
    )
    parser.add_argument(
        "--n_jobs",
        default=style_app_settings.N_JOBS,
        type=int,
        help="It is an integer, specifying the maximum number of concurrently running workers.",
    )

    args = parser.parse_args()
    print(args)

    # argparse
    # dataset
    num_books = args.num_books
    document_length = args.document_length

    # train model
    cross_validation = args.cross_validation
    num_job = args.n_jobs
    # split dataset
    test_percentage = args.test_percentage
    # under pipeline
    min_df = args.min_df
    normalize = args.normalize
    reduction = args.reduction
    num_doc = args.num_doc

    ngram_min = args.ngram_min
    ngram_max = args.ngram_max

    classifiers = [
        ("clf_svc", LinearSVC),
        ("clf_nb", MultinomialNB),
        ("clf_sgd", SGDClassifier),
    ]

    ngram_range = (ngram_min, ngram_max)

    parameters = [
        {
            "vectorize__ngram_range": [ngram_range],
            "clf_svc__C": [0.01, 0.1, 1, 10],
        },
        {
            "vectorize__ngram_range": [ngram_range],
            "clf_nb__alpha": [0.1, 0.3, 0.5, 0.8, 1],
        },
        {
            "vectorize__ngram_range": [ngram_range],
            "clf_sgd__loss": [
                "hinge",
                "squared_hinge",
            ],
            "clf_sgd__penalty": ["l2", "l1"],
        },
    ]

    dataset = DatasetReader.load_files(
        FILE_PATH_BOOK_DS, n=document_length, num_of_books=num_books
    )

    resampled_dataset = dataset.resample_balanced(num_doc=num_doc)

    exp_name = (
        f"experiment-date-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    )
    experiment_dir_name = Path(exp_name)

    print(
        f"The total data size: {len(resampled_dataset)}. Experiment name: {exp_name}"
    )

    docs_train, docs_test, y_train, y_test, dataset_target = split_dataset(
        resampled_dataset, test_percentage=test_percentage
    )

    print(
        f"Size of the training data: {docs_train.shape} and size of the test "
        f"data {docs_test.shape}"
    )

    model_comparison_results = dd(dict)

    for (name, clf), params in list(zip(classifiers, parameters)):
        print(f"Parameter Search started for {name} with {params}")
        model_export_path = MODEL_EXPORT_PATH / (name + ".model")

        pipeline = create_pipeline(
            name, clf(), min_df=min_df, normalize=normalize, reduction=reduction
        )
        model, report_, report_dict, cm = train_sklearn_classification_model(
            docs_train,
            docs_test,
            y_train,
            y_test,
            pipeline,
            params,
            n_jobs=num_job,
            cv=cross_validation,
        )

        print(f"Parameter Search finished for {name} with {params}")
        export(model, model_export_path)

        storage_client.upload(
            model_export_path,
            "style-resources" / experiment_dir_name / model_export_path.name,
        )

        model_comparison_results[name]["f1-weighted-avg"] = report_dict[
            "weighted avg"
        ]["f1-score"]
        model_comparison_results[name]["best-ngram"] = model.get_params()[
            "vectorize__ngram_range"
        ]
        print(f"The best model is written for {name} {model_export_path}")

        report(report_, name, cm, MODEL_EXPORT_PATH)

        report_output_path = (
            "style-resources" / experiment_dir_name / f"{name}-report.txt"
        )
        storage_client.upload(
            MODEL_EXPORT_PATH / f"{name}-report.txt", report_output_path
        )
        print(f"Report is written to {report_output_path}")

        confusion_matrix_output_path = (
            "style-resources" / experiment_dir_name / f"{name}-cm.txt"
        )
        storage_client.upload(
            MODEL_EXPORT_PATH / f"{name}-cm.txt", confusion_matrix_output_path
        )
        print(f"Confusion matrix is written to {confusion_matrix_output_path}")

    model_comparison_report(
        MODEL_EXPORT_PATH, args.__dict__, model_comparison_results
    )

    model_comparison_report_path = (
        "style-resources" / experiment_dir_name / "model_comparison_report.tsv"
    )

    storage_client.upload(
        MODEL_EXPORT_PATH / "model_comparison_report.tsv",
        model_comparison_report_path,
    )

    print(f"Model Comparison is written to {model_comparison_report_path}")
    print("Training & grid search & finding the best model is done.")


if __name__ == "__main__":
    run()
