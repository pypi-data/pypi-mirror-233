# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class TimeSeriesMissingValues(ThresholdTest):
    """
    **Purpose**:
    This test is designed to verify that the number of missing values in a historical time-series dataset is below a
    specified threshold. Since time-series models rely on continuity and temporality of data points, missing values
    could affect the model's performance. Therefore, this test intends to maintain data quality and readiness for the
    machine learning model.

    **Test Mechanism**:
    The test process begins by checking if the dataset has a datetime index; if not, an error is raised. Next, a lower
    limit threshold for missing values is set and a missing values check is run on each column of the dataset, with a
    test result object being generated whether the number of missing values is below the specified threshold. The
    percentage of missing values is also calculated alongside the raw count.

    As a visualization aid, the test generates two plots (a bar plot and a heatmap) to better illustrate the
    distribution and quantity of missing values per variable, if any exist. The test results, missing values count,
    missing values percentage, and the pass/fail status are returned in a results table.

    **Signs of High Risk**:
    If any column in the dataset contains a number of missing values exceeding the threshold, it is considered a
    failure and a high-risk scenario. This could be due to incomplete data collection, faulty sensors, or data
    preprocessing errors. A continuous visual 'streak' in the 'heatmap' might also indicate a systematic error during
    data collection.

    **Strengths**:
    This test is beneficial in promptly identifying missing values which might impact the model's performance. It is
    broadly applicable and customizable through the threshold parameter. Going beyond raw numbers to calculate the
    percentile of missing values adds a more relative understanding of data scarcity. It also includes a robust
    mechanism to visually represent data quality, facilitating quicker and friendlier misinterpretation.

    **Limitations**:
    Though the test effectively identifies missing values, it does not suggest methods to deal with them. It assumes
    that the dataset should have datetime index, limiting its use to time series analysis only. The test is sensitive
    to the 'min_threshold' parameter and might raise false alarms if it's set too strictly, or might miss problematic
    data if it's set too loosely. Lastly, the test solely focuses on 'missingness' and might overlook other aspects of
    data quality.
    """

    category = "data_quality"
    name = "time_series_missing_values"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data"],
    }

    def summary(self, results, all_passed):
        results_table = [
            {
                "Column": result.column,
                "Number of Missing Values": result.values["n_missing"],
                "Percentage of Missing Values (%)": result.values["p_missing"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Missing Values Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        df = self.dataset._df

        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        # Validate threshold parameter
        if "min_threshold" not in self.params:
            raise ValueError("min_threshold must be provided in params")
        min_threshold = self.params["min_threshold"]

        rows = df.shape[0]
        missing = df.isna().sum()
        test_results = [
            ThresholdTestResult(
                column=col,
                passed=missing[col] < min_threshold,
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        fig_barplot = self._barplot(df)
        fig_heatmap = self._heatmap(df)
        test_figures = []
        if fig_barplot is not None:
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:barplot",
                    figure=fig_barplot,
                    metadata={"type": "barplot"},
                )
            )
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:heatmap",
                    figure=fig_heatmap,
                    metadata={"type": "heatmap"},
                )
            )

        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            # Don't pass figures until we figure out how to group metric-figures for multiple
            # executions inside a single test run
            # figures=test_figures,
        )

    def _barplot(self, df):
        """
        Generate a bar plot of missing values using Plotly.
        """
        missing_values = df.isnull().sum()
        if sum(missing_values.values) != 0:
            fig = px.bar(
                missing_values,
                x=missing_values.index,
                y=missing_values.values,
                labels={"x": "", "y": "Missing Values"},
                title="Total Number of Missing Values per Variable",
                color=missing_values.values,
                color_continuous_scale="Reds",
            )
        else:
            fig = None

        return fig

    def _heatmap(self, df):
        """
        Plots a heatmap to visualize missing values using Plotly.
        """
        # Create a boolean mask for missing values
        missing_mask = df.isnull()
        z = missing_mask.T.astype(int).values  # Convert boolean to int for heatmap

        x = missing_mask.index.tolist()
        y = missing_mask.columns.tolist()

        if not x:
            fig = ff.create_annotated_heatmap(
                z=z, x=x, y=y, colorscale="Reds", showscale=False
            )
            fig.update_layout(title="Missing Values Heatmap")
        else:
            fig = None

        return fig
