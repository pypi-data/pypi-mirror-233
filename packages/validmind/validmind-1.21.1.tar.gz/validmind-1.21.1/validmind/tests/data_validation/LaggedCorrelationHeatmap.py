# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from validmind.vm_models import Figure, Metric

# Define the 'coolwarm' color scale manually
COOLWARM = [[0, "rgb(95,5,255)"], [0.5, "rgb(255,255,255)"], [1, "rgb(255,5,0)"]]


class LaggedCorrelationHeatmap(Metric):
    """
    **Purpose**: This LaggedCorrelationHeatmap metric is designed to evaluate and visualize the correlation between the
    target variable and certain delayed copies (lags) of independent variables in a time-series based dataset. This
    metric aids in uncovering relationships in time-series data where the influence of an input feature on the target
    variable may not be immediate but occurs after a certain period (lags).

    **Test Mechanism**: Python's Pandas library is used in conjunction with Plotly to perform computations and generate
    the heatmap. The target variable and corresponding independent variables are taken from the dataset. Subsequently,
    lags of independent variables are generated and the correlation between these lagged variables and the target are
    calculated. The calculated correlations are stored in a matrix that has variables on one axis and the number of
    lags on the other. This correlation matrix is then visualized as a heatmap, where different color intensities
    represent the strength of the correlation, making patterns easier to spot.

    **Signs of High Risk**: High risk associated with this metric may be indicated by insignificant correlations
    throughout the heatmap or by correlations that break intuition or prior knowledge, indicating potential issues with
    the data or model.

    **Strengths**: This metric offers an excellent way to explore and visualize the time-dependent relationships
    between features and the target variable in a time-series dataset. By looking at correlations with lagged features,
    it is possible to identify delayed effects that may go unnoticed with more traditional correlation measures. As
    it's visually represented, the heatmaps are a very intuitive way to present time dependent correlations and
    influence.

    **Limitations**: The LaggedCorrelationHeatmap metric has a few limitations. It assumes linear relationships between
    the variables, meaning relationships that aren't linear may go undetected. As it only considers linear correlation,
    it may miss out on complex nonlinear interactions. This metric works only with time-series data and would not be
    applicable for other types of data. Also, the choice of number of lags used can also affect the results; whilst too
    many lags can make the heatmap hard to interpret and less useful, too few might miss delayed effects. Furthermore,
    this metric does not consider any causal relationship, it merely presents the correlation.
    """

    name = "lagged_correlation_heatmap"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "visualization"],
    }

    def _compute_correlations(self, df, target_col, independent_vars, num_lags):
        correlations = np.zeros((len(independent_vars), num_lags + 1))

        for i, ind_var_col in enumerate(independent_vars):
            for lag in range(num_lags + 1):
                temp_df = pd.DataFrame(
                    {
                        target_col: df[target_col],
                        f"{ind_var_col}_lag{lag}": df[ind_var_col].shift(lag),
                    }
                )

                temp_df = temp_df.dropna()

                corr = temp_df[target_col].corr(temp_df[f"{ind_var_col}_lag{lag}"])

                correlations[i, lag] = corr

        return correlations

    def _plot_heatmap(self, correlations, independent_vars, target_col, num_lags):
        correlation_df = pd.DataFrame(
            correlations,
            columns=[f"{i}" for i in range(num_lags + 1)],
            index=independent_vars,
        )

        # Create heatmap using Plotly
        fig = ff.create_annotated_heatmap(
            z=correlation_df.values,
            x=list(correlation_df.columns),
            y=list(correlation_df.index),
            colorscale=COOLWARM,
            annotation_text=correlation_df.round(2).values,
            showscale=True,
        )

        fig.update_layout(
            title={
                "text": f"Correlations between {target_col} and Lags of Features",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(size=14),
            xaxis_title="Lags",
        )

        return fig

    def run(self):
        if isinstance(self.dataset.target_column, list):
            target_col = self.dataset.target_column[
                0
            ]  # take the first item from the list
        else:
            target_col = self.dataset.target_column

        independent_vars = list(self.dataset.get_features_columns())
        num_lags = self.params.get("num_lags", 10)

        if isinstance(target_col, list) and len(target_col) == 1:
            target_col = target_col[0]

        if not isinstance(target_col, str):
            raise ValueError(
                "The 'target_col' must be a single string or a list containing a single string"
            )

        df = self.dataset.df

        correlations = self._compute_correlations(
            df, target_col, independent_vars, num_lags
        )
        fig = self._plot_heatmap(correlations, independent_vars, target_col, num_lags)

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        return self.cache_results(
            figures=figures,
        )
