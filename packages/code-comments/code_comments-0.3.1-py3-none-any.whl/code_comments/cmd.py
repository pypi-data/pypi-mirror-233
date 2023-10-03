from __future__ import annotations

import click
import hashlib
import io
import os
import pathlib
from typing import Sequence, TextIO
import toml


def find_annonations(
    files: Sequence[str],
    comment_sytnax: Sequence[str],
    annotation: str,
    table_headers: str,
) -> io.StringIO:
    title = annotation.strip("#:")
    tmp_output = io.StringIO()

    tmp_output.write("## " + title + "\n")
    tmp_output.write("|" + table_headers + "|\n")
    tmp_output.write("|---|---|---|\n")

    for filename in files:
        try:
            with open(filename, encoding="UTF-8") as f:
                for syntax in comment_sytnax:
                    for line_number, line in enumerate(f, 1):
                        if line.startswith(syntax + annotation):
                            message = line.split(":")
                            tmp_output.write(
                                "| "
                                + filename
                                + ":"
                                + str(line_number)
                                + " |"
                                + message[1]
                                + "|"
                                + message[2].strip("\n")
                                + "|"
                                + "\n"
                            )
        except Exception as e:
            print(e)

    return tmp_output


def compare_files(output: TextIO, current: io.StringIO) -> bool:
    current_hash = hashlib.sha256(output.read().encode("utf-8")).hexdigest()
    new_hash = hashlib.sha256(current.getvalue().encode("utf-8")).hexdigest()

    if current_hash == new_hash:
        return True
    else:
        return False


def load_config(file_name: str) -> dict:
    try:
        toml_config = toml.load(file_name)
        return toml_config
    except Exception as e:
        print(e)


def filter_files(file_suffix: Sequence[str], filenames: Sequence[str]) -> Sequence[str]:
    to_process = []

    for suffix in file_suffix:
        for file in filenames:
            if file.endswith(suffix):
                to_process.append(file)

    return to_process


@click.command()
@click.option("--config", default=".code-annotations.toml", help="Config file name")
def cli(config) -> int:
    filenames = set()
    cwd = pathlib.Path(".")

    for dir_, _, files in os.walk(cwd):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, cwd)
            rel_file = os.path.join(rel_dir, file_name)
            filenames.add(rel_file)

    toml_config = load_config(config)

    try:
        output_file = open(toml_config["output_file"], "w+")
    except Exception as e:
        print(e)
        return 1

    to_process = []
    to_process = filter_files(toml_config["file_suffix"], filenames)
    new_report = io.StringIO()

    for header in toml_config["headers"]:
        new_report.write(
            find_annonations(
                to_process,
                toml_config["comment_syntax"],
                header["comment"] + ":",
                header["table_headers"],
            ).getvalue()
        )

    if not compare_files(output_file, new_report):
        output_file.write(new_report.getvalue())

    output_file.close()

    return 0
