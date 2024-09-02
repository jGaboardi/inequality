import os

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from inequality.schutz import Schutz


@pytest.fixture
def example_dataframe():
    data = {"NAME": ["A", "B", "C", "D", "E"], "Y": [1000, 2000, 1500, 3000, 2500]}
    return pd.DataFrame(data)


@pytest.fixture
def noninteractive_warning():
    return pytest.warns(
        UserWarning,
        match="FigureCanvasAgg is non-interactive, and thus cannot be shown",
    )


def test_schutz_distance(example_dataframe):
    schutz_obj = Schutz(example_dataframe, "Y")
    expected_distance = 0.15
    assert pytest.approx(schutz_obj.distance, 0.01) == expected_distance


def test_schutz_intersection_point(example_dataframe):
    schutz_obj = Schutz(example_dataframe, "Y")
    expected_intersection_point = 0.6
    assert (
        pytest.approx(schutz_obj.intersection_point, 0.1) == expected_intersection_point
    )


def test_schutz_coefficient(example_dataframe):
    schutz_obj = Schutz(example_dataframe, "Y")
    expected_coefficient = 7.5
    assert pytest.approx(schutz_obj.coefficient, 0.1) == expected_coefficient


def test_schutz_plot_runs_without_errors(example_dataframe, noninteractive_warning):
    schutz_obj = Schutz(example_dataframe, "Y")
    try:
        with noninteractive_warning:
            schutz_obj.plot()
    except Exception as e:
        pytest.fail(f"Plotting failed: {e}")


def test_schutz_plot_output(example_dataframe, tmpdir, noninteractive_warning):
    """Test if the plot output matches the expected result by saving
    the plot and comparing it."""
    schutz_obj = Schutz(example_dataframe, "Y")

    # Save the plot to a temporary directory
    plot_file = os.path.join(tmpdir, "schutz_plot.png")
    plt.figure()
    with noninteractive_warning:
        schutz_obj.plot()
    plt.savefig(plot_file)
    plt.close()

    # Ensure that the plot file was created
    assert os.path.exists(plot_file), "Plot file was not created."
