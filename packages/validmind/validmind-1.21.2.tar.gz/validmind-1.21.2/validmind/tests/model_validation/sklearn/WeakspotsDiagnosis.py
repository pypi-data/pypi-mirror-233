# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from functools import partial
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class WeakspotsDiagnosis(ThresholdTest):
    """
    **Purpose:**
    The weak spots test is designed to evaluate the performance of a machine learning model in specific regions of the
    feature space. This test consists of dividing the feature space into various sections or slices, evaluating the
    model's output within each of these sections, and identifying regions where the model's performance metrics fall
    below specified thresholds. Performance metrics include accuracy, precision, recall, and F1 scores. This diagnostic
    test helps identify areas where the machine learning model may not perform well, potentially exposing its
    limitations and weaknesses.

    **Test Mechanism:**
    The test is performed by slicing the feature space of the training data set into multiple bins. For each bin, the
    model's performance metrics are computed for both the training and test data sets. If any of the model's
    performance metrics fall below the predetermined threshold for a particular bin on the test dataset, it is
    identified as a "weak spot". The results are visually represented in a bar chart for each performance metric,
    marking the bins failing the threshold.

    **Signs of High Risk:**
    High risk or failure in the model's performance is indicated when any of the model's performance metrics fall below
    the set thresholds. If any bin performed significantly worse in the test dataset compared to the training dataset,
    it might indicate overfitting in that region. Further, if a region or slice has low performance metrics, it
    suggests that the model does not handle that type of input data well, which may lead to inaccurate predictions.

    **Strengths:**
    - The weak spots test helps identify specific regions of the feature space where the model's performance is subpar,
    which can guide further refinement of the model.
    - Plotting the performance metrics provides an intuitive way to understand the model's performance across different
    regions.
    - The test can be customizable, allowing users to specify various thresholds for multiple performance metrics based
    on the needs of the specific application.

    **Limitations:**
    - By binning the feature space, the test could potentially oversimplify the model's behavior in each region. The
    granular control of this slicing depends on the bins parameter, and can be coincidentally arbitrary.
    - The test's effectiveness relies upon the chosen thresholds for the performance metrics, which may not be
    universally applicable and subject to the model's specification and the application.
    - The test does not handle datasets with a text column, thus limiting its applicability to only numerical or
    categorical data.
    - The test does not directly provide suggestions for model improvement, only highlighting potentially problematic
    regions.
    """

    category = "model_diagnosis"
    name = "weak_spots"
    required_inputs = ["model", "model.train_ds", "model.test_ds"]

    default_params = {
        "features_columns": None,
        # Some default values that the user should override
        "thresholds": {
            "accuracy": 0.75,
            "precision": 0.5,
            "recall": 0.5,
            "f1": 0.7,
        },
    }

    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_diagnosis",
            "visualization",
        ],
    }

    # TODO: allow configuring
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": partial(metrics.precision_score, zero_division=0),
        "recall": partial(metrics.recall_score, zero_division=0),
        "f1": partial(metrics.f1_score, zero_division=0),
    }

    def run(self):
        thresholds = self.params["thresholds"]

        # Ensure there is a threshold for each metric
        for metric in self.default_metrics.keys():
            if metric not in thresholds:
                raise ValueError(f"Threshold for metric {metric} is missing")

        if self.params["features_columns"] is None:
            features_list = self.model.train_ds.get_features_columns()
        else:
            features_list = self.params["features_columns"]

        if self.model.train_ds.text_column in features_list:
            raise ValueError(
                "Skiping Weakspots Diagnosis test for the dataset with text column"
            )

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.model.train_ds.get_features_columns() for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with "
                + "training dataset feature columns"
            )

        target_column = self.model.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        train_df = self.model.train_ds.df.copy()
        train_class_pred = self.model.y_train_predict
        train_df[prediction_column] = train_class_pred

        test_df = self.model.test_ds.df.copy()
        test_class_pred = self.model.y_test_predict
        test_df[prediction_column] = test_class_pred

        test_results = []
        test_figures = []
        results_headers = ["slice", "shape", "feature"]
        results_headers.extend(self.default_metrics.keys())
        for feature in features_list:
            bins = 10
            if feature in self.model.train_ds.get_categorical_features_columns():
                bins = len(train_df[feature].unique())
            train_df["bin"] = pd.cut(train_df[feature], bins=bins)

            results_train = {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby("bin"):
                self._compute_metrics(
                    results_train,
                    region,
                    df_region,
                    target_column,
                    prediction_column,
                    feature,
                )
                df_test_region = test_df[
                    (test_df[feature] > region.left)
                    & (test_df[feature] <= region.right)
                ]
                self._compute_metrics(
                    results_test,
                    region,
                    df_test_region,
                    target_column,
                    prediction_column,
                    feature,
                )

            # Make one plot per metric
            for metric in self.default_metrics.keys():
                fig, df = self._plot_weak_spots(
                    results_train,
                    results_test,
                    feature,
                    metric=metric,
                    threshold=thresholds[metric],
                )

                test_figures.append(
                    Figure(
                        for_object=self,
                        key=f"{self.name}:{metric}:{feature}",
                        figure=fig,
                        metadata={
                            "metric": metric,
                            "threshold": thresholds[metric],
                            "feature": feature,
                        },
                    )
                )

            # For simplicity, test has failed if any of the metrics is below the threshold. We will
            # rely on visual assessment for this test for now.
            results_passed = df[df[list(thresholds.keys())].lt(thresholds).any(axis=1)]
            passed = results_passed.empty

            test_results.append(
                ThresholdTestResult(
                    test_name="accuracy",
                    column=feature,
                    passed=passed,
                    values={"records": df.to_dict("records")},
                )
            )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        results_table = [
            record for result in results for record in result.values["records"]
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Weakspots Test"),
                )
            ]
        )

    def _compute_metrics(
        self,
        results: dict,
        region: str,
        df_region: pd.DataFrame,
        target_column: str,
        prediction_column: str,
        feature_column: str,
    ) -> None:
        """
        Computes and appends the default metrics for a given DataFrame slice to the results dictionary.
        Args:
            results (dict): A dictionary to which the computed metrics will be appended.
            region (str): A string identifier for the DataFrame slice being evaluated.
            df_region (pd.DataFrame): A pandas DataFrame slice containing the data to evaluate.
            target_column (str): The name of the target column to use for computing the metrics.
            prediction_column (str): The name of the prediction column to use for computing the metrics.
        Returns:
            None: The computed metrics are appended to the `results` dictionary in-place.
        """
        results["slice"].append(str(region))
        results["shape"].append(df_region.shape[0])
        results["feature"].append(feature_column)

        # Check if df_region is an empty dataframe and if so, append 0 to all metrics
        if df_region.empty:
            for metric in self.default_metrics.keys():
                results[metric].append(0)
            return

        y_true = df_region[target_column].values
        y_prediction = (
            df_region[prediction_column].astype(df_region[target_column].dtypes).values
        )

        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true, y_prediction))

    def _plot_weak_spots(
        self, results_train, results_test, feature_column, metric, threshold
    ):
        """
        Plots the metric of the training and test datasets for each region in a given feature column,
        and highlights regions where the score is below a specified threshold.
        Args:
            results_train (list of dict): The results of the model on the training dataset, as a list of dictionaries.
            results_test (list of dict): The results of the model on the test dataset, as a list of dictionaries.
            feature_column (str): The name of the feature column being analyzed.
            metric (str): The name of the metric to plot.
            threshold (float): The minimum accuracy threshold to be highlighted on the plot.
        Returns:
            fig (matplotlib.figure.Figure): The figure object containing the plot.
            df (pandas.DataFrame): The concatenated dataframe containing the training and test results.
        """
        # Concat training and test datasets
        results_train = pd.DataFrame(results_train)
        results_test = pd.DataFrame(results_test)
        dataset_type_column = "Dataset Type"
        results_train[dataset_type_column] = "Training"
        results_test[dataset_type_column] = "Test"
        df = pd.concat([results_train, results_test])

        # Create a bar plot using seaborn library
        fig, ax = plt.subplots()
        barplot = sns.barplot(
            data=df,
            x="slice",
            y=metric,
            hue=dataset_type_column,
            edgecolor="black",
            ax=ax,
        )
        ax.tick_params(axis="x", rotation=90)
        for p in ax.patches:
            t = ax.annotate(
                str("{:.2f}%".format(p.get_height())),
                xy=(p.get_x() + 0.03, p.get_height() + 1),
            )
            t.set(color="black", size=14)

        axhline = ax.axhline(
            y=threshold,
            color="red",
            linestyle="--",
            linewidth=3,
            label=f"Threshold: {threshold}",
        )
        ax.set_ylabel(metric.capitalize(), weight="bold", fontsize=18)
        ax.set_xlabel("Slice/Segments", weight="bold", fontsize=18)
        ax.set_title(
            f"Weak regions in feature column: {feature_column}",
            weight="bold",
            fontsize=20,
            wrap=True,
        )

        # Get the legend handles and labels from the barplot
        handles, labels = barplot.get_legend_handles_labels()

        # Append the axhline handle and label
        handles.append(axhline)
        labels.append(axhline.get_label())

        # Create a legend with both hue and axhline labels, the threshold line
        # will show up twice so remove the first element
        # barplot.legend(handles=handles[:-1], labels=labels, loc="upper right")
        barplot.legend(
            handles=handles[:-1],
            labels=labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.1),
            ncol=len(handles),
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return fig, df
