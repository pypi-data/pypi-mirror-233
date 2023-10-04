from collections.abc import Generator

import pytest
from mypy_boto3_dynamodb.service_resource import Table
from nhs_aws_helpers.fixtures import temp_dynamodb_table


@pytest.fixture(scope="session")
def session_temp_mesh_table() -> Generator[Table, None, None]:
    yield from temp_dynamodb_table("local-mesh")


@pytest.fixture()
def temp_mesh_table(session_temp_mesh_table: Table) -> Table:
    table = session_temp_mesh_table
    result = table.scan(ProjectionExpression="pk, sk", ConsistentRead=True)
    with table.batch_writer(["pk", "sk"]) as writer:
        while True:
            items = result.get("Items", [])
            if not items:
                break
            for item in items:
                writer.delete_item({"pk": item["pk"], "sk": item["sk"]})
            if len(writer._items_buffer) > 0:  # type: ignore[attr-defined]
                writer._flush()  # type: ignore[attr-defined]
            if not result.get("LastEvaluatedKey"):
                break
            result = session_temp_mesh_table.scan(
                ProjectionExpression="pk, sk",
                ConsistentRead=True,
                ExclusiveStartKey=result.get("LastEvaluatedKey"),  # type: ignore[arg-type]
            )

    return table
