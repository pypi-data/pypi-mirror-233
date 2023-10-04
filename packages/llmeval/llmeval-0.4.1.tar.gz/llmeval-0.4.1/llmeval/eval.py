# Copyright Log10, Inc 2023


import sys
from omegaconf import DictConfig, open_dict, OmegaConf

import hydra
from langchain.prompts import ChatPromptTemplate
from log10.llm import Log10Config, Message
from log10.openai import OpenAI
from log10.anthropic import Anthropic

import logging
import semver
from llmeval import __version__

# TODO: Define data class for prompt
# TODO: Define data class for tests


supported_models = {
    "gpt-3.5-turbo": OpenAI,
    "gpt-4": OpenAI,
    "claude-2": Anthropic,
}


@hydra.main(version_base=None, config_path=".", config_name="llmeval")
def main(cfg: DictConfig) -> None:
    if cfg.version is not None:
        config_version = semver.Version.parse(cfg.version)
        app_version = semver.Version.parse(__version__.__version__)
        logging.debug(f"config_version={config_version}")
        logging.debug(f"app_version={app_version}")

        if app_version > config_version:
            logging.warn(
                f"llmeval version {app_version} is newer than config version {config_version} and may not be compatible. Please update config files to match with llmeval version {app_version}."
            )
        elif app_version < config_version:
            logging.error(
                f"llmeval version {app_version} is older than config version {config_version} and may not be compatible. Please update llmeval cli."
            )
    else:
        logging.warn(
            "No version specified in report. Assuming using latest llmeval version"
        )

    log10_token = None
    if hasattr(cfg, "log10"):
        log10_url = cfg.log10.url
        log10_token = cfg.log10.token
        log10_org_id = cfg.log10.org_id

        # Clean up the token and org_id in the report
        del cfg.log10.token
        del cfg.log10.org_id

    for i in range(cfg.n_tries):
        # TODO: If messages is available, assume it is a chat model.
        if hasattr(cfg.prompts, "messages"):
            messages = [
                (message.role, message.content) for message in cfg.prompts.messages
            ]
            template = ChatPromptTemplate.from_messages(messages)

        metrics = cfg.prompts.tests.metrics
        variables = cfg.prompts.variables

        prompt_code = cfg.prompts.get("code", None)
        model_name = cfg.prompts.model

        test_skipped = False
        if hasattr(cfg.prompts.tests, "skip"):
            test_skipped = cfg.prompts.tests.skip

        logging.debug(metrics)
        prompt_locals = {}
        # Substitute variables in template with reference values.
        for reference in cfg.prompts.tests.references:
            # Verify reference has all expected variables.
            missing_variables = False
            for variable in variables:
                if variable.name not in reference.input:
                    logging.warn(
                        f"Variable {variable} is not in reference input. Skipping."
                    )
                    missing_variables = True
                else:
                    prompt_locals[variable.name] = reference.input[variable.name]
            if missing_variables:
                continue

            logging.debug(f"reference={reference}")

            if prompt_code:
                try:
                    format_code = prompt_code.format(**reference.input)
                    exec(format_code, None, prompt_locals)
                    response = prompt_locals["output"]
                    messages = prompt_locals.get("messages", "")
                except KeyError as e:
                    print(
                        f"Please check prompt code to ensure that {e} variables are present"
                    )
                    sys.exit(1)
            else:
                messages = template.format_messages(**reference.input)

            log10_messages = [Message(role="user", content=m.content) for m in messages]
            logging.debug(f"messages={[m.to_dict() for m in log10_messages]}")

            if prompt_code is None:
                if model_name in supported_models:
                    model = supported_models[model_name]
                else:
                    logging.warn(
                        f"Unsupported model {model_name}. Currently only support OpenAI and Anthropic models. Please reach out to us at founders@log10.io to add support"
                    )

                temperature = cfg.prompts.temperature
                hparams = {"model": model_name, "temperature": temperature}

                optional_hparams_list = [
                    "max_tokens",
                    "stop",
                    "presence_penalty",
                    "frequency_penalty",
                ]
                for hp in optional_hparams_list:
                    value = cfg.prompts.get(hp)
                    if value:
                        hparams[hp] = value

            if prompt_code is None:
                log10_config = None
                if log10_token:
                    log10_config = Log10Config(
                        url=log10_url, token=log10_token, org_id=log10_org_id
                    )

                llm = model(hparams, log10_config=log10_config)

                response = llm.chat(log10_messages, hparams=hparams)

            with open_dict(reference):
                actual = response.content
                logging.debug(f"actual={actual}")
                reference["actual"] = actual
                if log10_token and prompt_code is None:
                    reference["log_url"] = llm.last_completion_url()
                    reference["duration"] = llm.last_duration()

                for metric_spec in metrics:
                    logging.debug(f"metric={metric_spec}")
                    locals = {"prompt": str(messages), "actual": actual}

                    metric_skipped = False
                    if hasattr(metric_spec, "skip"):
                        metric_skipped = metric_spec.skip

                    if hasattr(reference, "expected"):
                        locals["expected"] = reference.expected

                    exec(metric_spec.code, None, locals)
                    metric_value = locals["metric"]
                    result = locals["result"]
                    logging.debug(f"result={result}")

                    logging.debug(f"metric.name={metric_spec.name}")
                    # Check whether value is already set.
                    if "metrics" not in reference:
                        reference["metrics"] = {}

                    # Determine whether to skip metric.
                    reference_skipped = False
                    if hasattr(reference, "skip"):
                        reference_skipped = reference.skip

                    reference["metrics"][metric_spec.name] = {
                        "metric": metric_value,
                        "result": "pass" if result else "fail",
                        "skipped": reference_skipped or metric_skipped or test_skipped,
                    }

        with open(f"report-{i}.yaml", "w") as f:
            f.write(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()
