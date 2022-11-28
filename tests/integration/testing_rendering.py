# this is the section that we will be doing the rendering testing. So that we can set breakpoints
import os

import pytest

import great_expectations as ge
from great_expectations import DataContext
from great_expectations.checkpoint import Checkpoint
from great_expectations.data_context.util import file_relative_path


@pytest.fixture(scope="function")
def test_db_data_context(
    tmp_path,
) -> DataContext:
    project_path = file_relative_path(
        __file__, "../test_fixtures/configuration_for_testing_v2_v3_migration/sqlite/v3"
    )
    db_path = file_relative_path(__file__, "../test_sets/metrics_test.db")
    project_path = str(project_path)
    context = ge.data_context.DataContext.create(project_path)
    context_path = os.path.join(project_path, "great_expectations")
    asset_config_path = os.path.join(context_path, "expectations")
    os.makedirs(asset_config_path, exist_ok=True)
    return context


# @mock.patch(
#     "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
# )
def test_checkpoint(test_db_data_context, caplog, capsys):
    context: DataContext = test_db_data_context
    batch_request: dict = {
        "datasource_name": "my_test_datasource",
        "data_connector_name": "my_sql_data_connector",
        "data_asset_name": "my_asset",
    }
    checkpoint: Checkpoint = Checkpoint(
        name="my_checkpoint",
        data_context=context,
        config_version=1,
        run_name_template="%Y-%M-foo-bar-template",
        expectation_suite_name="animal_names_exp",
        action_list=[
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction",
                },
            },
            {
                "name": "store_evaluation_params",
                "action": {
                    "class_name": "StoreEvaluationParametersAction",
                },
            },
            {
                "name": "update_data_docs",
                "action": {
                    "class_name": "UpdateDataDocsAction",
                },
            },
        ],
        validations=[{"batch_request": batch_request}],
    )
    # TODO: this is not respected
    # should be in Expectation Level?
    # how do you respect unexpected_index_column_names
    # could we support this?

    # what needs to happen? we need a way to thread the unexpected column name

    result = checkpoint.run(
        result_format={
            "result_format": "COMPLETE",
            "unexpected_index_column_names": ["key_1"],
        }
    )


# @pytest.fixture(scope="function")
# def sql_data_context(
# ) -> DataContext:
#     """
#
#     """
#     project_path = tmp_path / "titanic_data_context"
#     project_path.mkdir()
#     project_path = str(project_path)
#     context_path = os.path.join(project_path, "great_expectations")
#     os.makedirs(os.path.join(context_path, "expectations"), exist_ok=True)
#     data_path = os.path.join(context_path, "..", "data", "titanic")
#     os.makedirs(os.path.join(data_path), exist_ok=True)
#     shutil.copy(
#         file_relative_path(__file__, "../test_fixtures/great_expectations_titanic.yml"),
#         str(os.path.join(context_path, "great_expectations.yml")),
#     )
#     shutil.copy(
#         file_relative_path(__file__, "../test_sets/Titanic.csv"),
#         str(os.path.join(context_path, "..", "data", "titanic", "Titanic_1911.csv")),
#     )
#     shutil.copy(
#         file_relative_path(__file__, "../test_sets/Titanic.csv"),
#         str(os.path.join(context_path, "..", "data", "titanic", "Titanic_1912.csv")),
#     )
#     return ge.data_context.DataContext(context_path)
