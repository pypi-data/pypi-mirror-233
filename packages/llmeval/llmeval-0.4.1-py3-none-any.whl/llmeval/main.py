# Copyright Log10, Inc 2023

import json
import subprocess
import sys
import click

from pathlib import Path
from llmeval.utils import copyExampleFolder, folder_name
import logging
import os
import re
import yaml
import semver
from llmeval import __version__


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--destination", default=".", help="The example folder is being copied to."
)
def init(destination):
    """
    Initialize a folder with evaluation config files.
    """
    srcFolder = f"{Path(__file__).resolve().parent}/{folder_name}"
    destFolder = f"{Path(destination).resolve()}"
    copyExampleFolder(srcFolder, destFolder)
    click.echo(
        f"1. Try out evaluating our model with the example config files in {destFolder} with:"
    )
    click.echo(click.style("  llmeval run", fg="green"))
    click.echo(
        f"2. Generate a report stored under {destFolder}/multirun/ once the evaluation is completed with:"
    )
    click.echo(click.style("  llmeval report", fg="green"))


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option("--path", default=".", help="The config folder path.")
def run(path):
    """
    Evaluate the model with the given config folder.
    """

    n_args = 1
    args = [
        "python",
        f"{Path(__file__).resolve().parent}/eval.py",
        f"--config-path={Path(path).resolve()}",
    ]
    args.extend(sys.argv[n_args + 1 :])

    cmd = f"{' '.join(args)}"

    click.echo("Running evaluation...")
    rc, out = subprocess.getstatusoutput(cmd)

    if rc:
        click.echo(f"Evaluation failed due to {out}")
    else:
        click.echo(f"Ran evaluation successfully.")
        click.echo(out)

    sys.exit(rc)


def format_output(output):
    output = output[:50] + "..." if len(output) > 50 else output

    # Surround with backticks.
    output = f"`{output.replace('`', '')}`"

    # Remove newlines and characters that would cause formatting table report.
    output = re.sub("[\n\|]", " ", output)

    return output


# TODO: Generate a final output per test, and per report.
# TODO: Show hyperparameters in the report.
@cli.command()
@click.option("--path", default="multirun", help="The eval results folder path.")
def report(path):
    """
    Generate a report from the evaluation results.
    """
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == "multirun.yaml":
                matches.append(dirpath)

    if len(matches) == 0:
        print("❌ No evaluations found. Please run `llmeval run` first.")
        sys.exit(1)

    total_status = True
    total_statuses = []
    for match in matches:
        print("📈 Generating report for: " + match)

        report = {}
        with open(os.path.join(match, "report.md"), "w") as file_handle:
            for dirpath, dirnames, filenames in os.walk(match):
                for file in filenames:
                    if file.startswith("report-") and file.endswith(".yaml"):
                        full_path = os.path.join(dirpath, file)

                        # Regex to get the job id, date and time.
                        group = re.search(
                            r"(\d{4}-\d{2}-\d{2})/(\d{2}-\d{2}-\d{2})/(\d*)/report-(\d*)\.yaml",
                            full_path,
                        )
                        if group:
                            eval_date = group.group(1)
                            eval_time = group.group(2)
                            job_id = group.group(3)
                            run_id = group.group(4)

                            print(
                                f"  Processing job at date: {eval_date} time: {eval_time} job id: {job_id} run id: {run_id}..."
                            )

                            # Parse yaml file and get the results.
                            eval_file = yaml.load(
                                open(full_path), Loader=yaml.FullLoader
                            )

                            if eval_file["version"] is not None:
                                config_version = semver.Version.parse(
                                    eval_file["version"]
                                )
                                app_version = semver.Version.parse(
                                    __version__.__version__
                                )
                                logging.debug(f"config_version={config_version}")
                                logging.debug(f"app_version={app_version}")

                                if app_version > config_version:
                                    logging.warn(
                                        f"llmeval version {app_version} is greater than config version {config_version} and may not be compatible. Please update report files or rerun."
                                    )
                                elif app_version < config_version:
                                    logging.error(
                                        f"llmeval version {app_version} is less than config version {config_version} and may not be compatible. Please update llmeval."
                                    )
                            else:
                                logging.warn(
                                    "No version specified in report. Assuming using latest llmeval version"
                                )

                            test_name = eval_file["prompts"]["name"]

                            if eval_date not in report:
                                report[eval_date] = {}
                            if eval_time not in report[eval_date]:
                                report[eval_date][eval_time] = {}
                            if test_name not in report[eval_date][eval_time]:
                                report[eval_date][eval_time][test_name] = []
                            report[eval_date][eval_time][test_name].append(eval_file)

            # Process report
            for eval_date in report:
                for eval_time in report[eval_date]:
                    report_output = ""
                    report_statuses = []
                    log_url_num = 0
                    log10_url = None
                    duration = None

                    report_output += (
                        f"**Date** {eval_date} {eval_time.replace('-', ':')}\n"
                    )

                    for test_name in report[eval_date][eval_time]:
                        test_output = ""
                        test_statuses = []

                        eval_files = report[eval_date][eval_time][test_name]

                        # Get variables and metrics from the first eval file.
                        eval_file = eval_files[0]

                        # Make this optional, and format with a json formatter.
                        output = eval_file["prompts"].get(
                            "messages", eval_file["prompts"].get("code", "")
                        )
                        test_output += f"```\n{output}\n```\n"

                        metrics_rollup = eval_file["prompts"]["tests"].get(
                            "metrics_rollup", None
                        )

                        if metrics_rollup is not None:
                            cols = [metrics_rollup["name"]]
                        else:
                            cols = [""]

                        # Get hyperparameters from the first eval file i.e. whatever isn't variables, name, messages, tests.
                        hyperparameters = []
                        for key in eval_file["prompts"]:
                            if key not in [
                                "variables",
                                "name",
                                "messages",
                                "code",
                                "tests",
                            ]:
                                hyperparameters.append(key)

                        cols.extend(hyperparameters)

                        for variable in eval_file["prompts"]["variables"]:
                            cols.append(variable["name"])

                        cols.append("Expected")

                        # Do n_tries times.
                        for i in range(eval_file["n_tries"]):
                            cols.append(f"Actual #{i}")
                            for metric in eval_file["prompts"]["tests"]["references"][
                                0
                            ]["metrics"]:
                                cols.append(f"{metric} (metric) #{i}")
                                cols.append(f"{metric} (pass / fail) #{i}")

                            if "log10" in eval_file:
                                duration = eval_file["prompts"]["tests"]["references"][
                                    0
                                ].get("duration", None)
                                if duration:
                                    cols.append(f"duration #{i}")

                                log10_url = eval_file["prompts"]["tests"]["references"][
                                    0
                                ].get("log_url", None)
                                if log10_url:
                                    cols.append(f"logs #{i}")
                                    log_url_num += 1

                        test_output += f"| {' | '.join(cols)} |\n"

                        separators = ["---"] * len(cols)

                        test_output += f"| {' | '.join(separators)} |\n"

                        # For a given hyperparameter and reference, find results across samples.
                        eval_files_with_consolidated_samples = {}
                        for eval_file in eval_files:
                            # Same reference means same input and expected output.
                            id_segments = []
                            for hyperparameter in hyperparameters:
                                id_segments.append(
                                    str(eval_file["prompts"][hyperparameter])
                                )
                            id = "-".join(id_segments)

                            for reference in eval_file["prompts"]["tests"][
                                "references"
                            ]:
                                current_id = (
                                    id
                                    + str(reference["input"])
                                    + str(reference.get("expected", ""))
                                )
                                if (
                                    current_id
                                    not in eval_files_with_consolidated_samples
                                ):
                                    # Ugly, but a reference doesn't have an ID so we build an ID our of the hyperparameters, input and expected output.
                                    eval_files_with_consolidated_samples[current_id] = {
                                        "eval_file": eval_file,
                                        "references": [],
                                    }

                                eval_files_with_consolidated_samples[current_id][
                                    "references"
                                ].append(reference)

                        sample_id = 0
                        for eval_file_name in eval_files_with_consolidated_samples:
                            eval_file = eval_files_with_consolidated_samples[
                                eval_file_name
                            ]["eval_file"]
                            references = eval_files_with_consolidated_samples[
                                eval_file_name
                            ]["references"]

                            row = []

                            for hyperparameter in hyperparameters:
                                row.append(str(eval_file["prompts"][hyperparameter]))

                            reference = references[0]
                            input = [str(x) for x in reference["input"].values()]
                            input = [format_output(x) for x in input]

                            row.extend(input)

                            expected = reference.get("expected", "N/A")
                            row.append(format_output(expected))

                            id = 0
                            reference_status = True
                            num_passes = 0
                            num_fails = 0
                            num_skip_passes = 0
                            num_skip_fails = 0
                            reference_statuses = []
                            for reference in references:
                                # If input is a long string, cap it at 50 characters.
                                actual = reference.get("actual", "N/A")
                                row.append(format_output(actual))

                                for metric in reference["metrics"]:
                                    row.append(
                                        str(reference["metrics"][metric]["metric"])
                                    )

                                    resultValue = reference["metrics"][metric]["result"]
                                    result = resultValue == "pass"
                                    skipped = reference["metrics"][metric].get(
                                        "skipped", False
                                    )

                                    if result:
                                        num_passes += 1
                                        test_status_icon = "✅"
                                        if skipped:
                                            num_skip_passes += 1
                                    else:
                                        num_fails += 1
                                        test_status_icon = "🛑"
                                        if skipped:  ### skipped is True
                                            num_skip_fails += 1
                                        else:
                                            reference_status = False

                                    if skipped:
                                        if metrics_rollup is not None:
                                            test_status_icon = f"{test_status_icon} (WARN: skipping ignored when custom metrics roll up is defined)"
                                        else:
                                            test_status_icon = (
                                                f"{test_status_icon} (skipping)"
                                            )

                                    if metrics_rollup is None:
                                        reference_statuses.append(reference_status)

                                    row.append(test_status_icon)
                                    if duration:
                                        log_duration = reference.get("duration", None)

                                        if log_duration is not None:
                                            row.append(f"{log_duration/1000}s")
                                        else:
                                            row.append("N/A")

                                    if log10_url:
                                        log_url = reference.get("log_url", None)
                                        urlMarkup = f"[View]({log_url})"
                                        row.append(urlMarkup)

                                id += 1

                            if (metrics_rollup is not None) and (
                                len(metrics_rollup) > 0
                            ):
                                if reference["metrics"][metric].get("skipped", False):
                                    click.echo(
                                        click.style(
                                            "Warning: The skip option is not considered with a metrics_rollup is defined.",
                                            fg="yellow",
                                        )
                                    )

                                metrics_rollup_code = metrics_rollup["code"]
                                metrics_rollup_name = metrics_rollup["name"]
                                locals = {
                                    "num_passes": num_passes,
                                    "num_fails": num_fails,
                                    "num_skip_passes": num_skip_passes,
                                    "num_skip_fails": num_skip_fails,
                                }
                                try:
                                    exec(metrics_rollup_code, None, locals)
                                except SyntaxError as e:
                                    print(
                                        f"There is a syntax error with metrics_rollup name: {metrics_rollup_name} in {eval_file['prompts']['name']} file. Please fix the error and try again."
                                    )
                                    sys.exit(1)

                                reference_statuses.append(locals["result"])

                            test_statuses.extend(reference_statuses)
                            row.insert(0, "✅" if all(reference_statuses) else "🛑")
                            test_output += f"| {' | '.join(row)} |\n"
                            sample_id += 1

                        report_statuses.extend(test_statuses)
                        test_output = (
                            f"## {'✅' if all(test_statuses) else '🛑'} {test_name}\n"
                            + test_output
                        )
                        report_output += test_output

                    total_statuses.extend(report_statuses)
                    if log_url_num == 0:
                        message = "\n\n\n 📢 Create an account on [log10.io](log10.io) to view the logs of this test when you re-run it with passing log10 credentials."
                        report_output += message
                    report_output = (
                        f"#  {'✅' if all(report_statuses) else '🛑'} llmeval report\n\n"
                        + report_output
                    )
                    file_handle.write(report_output)
                    print(f"📄 Report written to {os.path.join(match, 'report.md')}")

    if all(total_statuses):
        print("🎉🎉🎉 All tests passed 🎉🎉🎉")
    else:
        print("🛑🛑🛑 Some tests failed 🛑🛑🛑")

    sys.exit(0 if total_status else 1)


cli.add_command(init)
cli.add_command(run)
if __name__ == "__main__":
    cli()
