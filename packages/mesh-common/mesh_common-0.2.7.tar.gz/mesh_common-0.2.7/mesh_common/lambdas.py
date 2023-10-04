import asyncio
import inspect
import json
import os
from collections.abc import Callable
from typing import Any, cast

from nhs_context_logging import app_logger

from mesh_common import setup_app_logger
from mesh_common.aws import setup_aws_retries
from mesh_common.env_config import get_env_config


def lambda_handler(
    event,
    context,
    main: Callable,
    default_lambda_function_name: str,
    expected_errors: tuple[type] = cast(tuple[type], ()),
    env_config_prefix: str = "MESH",
) -> Any:
    service_name = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", default_lambda_function_name)
    is_async = inspect.iscoroutinefunction(main)

    log_globals = {}

    if context and hasattr(context, "function_name"):
        log_globals = {
            "lambda": {
                "function": context.function_name,
                "request_id": context.aws_request_id,
                "log_stream": context.log_stream_name,
            }
        }

    setup_aws_retries()

    async def async_wrap():
        setup_app_logger(service_name, is_async=is_async, expected_errors=expected_errors)
        cfg = get_env_config(prefix=env_config_prefix)
        log_globals["app"] = {"env": cfg.env}
        app_logger.add_app_globals(**log_globals)
        return await main(event)

    if is_async:
        return asyncio.run(async_wrap())

    setup_app_logger(service_name, is_async=is_async, expected_errors=expected_errors)
    config = get_env_config(prefix=env_config_prefix)
    log_globals["app"] = {"env": config.env}
    app_logger.add_app_globals(**log_globals)
    return main(event)


def maybe_from_eventbridge(record: dict) -> dict:
    if "detail" in record and "detail-type" not in record:
        return cast(dict, record["detail"])
    body = cast(dict, json.loads(record["body"]))
    keys = list(body.keys())
    if "detail" not in keys or "detail-type" not in keys:
        return body
    return cast(dict, body["detail"])
