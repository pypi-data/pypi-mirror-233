"""Common configuration shared by all tests in this directory."""


import re
from contextlib import contextmanager
from pathlib import Path
import gzip
import shutil
import pytest

from probs_runner import (
    Datasource,
    probs_convert_data,
    probs_endpoint,
)


def pytest_addoption(parser):
   parser.addoption(
       "--print-facts", action="store_true", help="enable dumping the facts"
   )
   parser.addoption(
       "--working-dir", action="store", help="path to working directory, default temporary"
   )
   parser.addoption(
       "--keep-working-dir", action="store_true", help="don't delete temporary working directories"
   )
   parser.addoption(
       "--ontology-dir", action="store", help="path to ontology scripts, default ../.. relative to tests"
   )


@pytest.fixture(scope="class")
def tmp_path_class(request, tmp_path_factory):
    """Like build-in tmp_path fixture but scoped to class."""
    name = request.node.name
    name = re.sub(r"[\W]", "_", name)
    MAXVAL = 30
    name = name[:MAXVAL]
    return tmp_path_factory.mktemp(name, numbered=True)


@pytest.fixture(scope="session")
def script_source_dir(request):
    source_dir = request.config.getoption("--ontology-dir")
    if source_dir:
        source_dir = Path(source_dir)
    else:
        source_dir = None
    return source_dir


@pytest.fixture(scope="class")
def probs_endpoint_from_datasource(request, tmp_path_class, script_source_dir):
    """Return a function to run a set of datasources"""
    print_facts = request.config.getoption("--print-facts")
    working_dir = request.config.getoption("--working-dir") or tmp_path_class
    if working_dir:
        working_dir = Path(working_dir)
    keep_working_dir = request.config.getoption("--keep-working-dir") or (working_dir != tmp_path_class)

    # Return a more verbose function if requested by the command-line argument.
    @contextmanager
    def probs_datasource_func(datasources):
        original_filename = working_dir / "original.nt.gz"

        if isinstance(datasources, Datasource):
            datasources = [datasources]

        probs_convert_data(
            datasources,
            original_filename,
            working_dir=working_dir / "working_conversion",
            script_source_dir=script_source_dir,
        )
        #
        # Delete intermediate files, otherwise they use lots of space
        if not keep_working_dir:
            shutil.rmtree(working_dir / "working_conversion")

        with probs_endpoint(
            [original_filename],
            working_dir / "working_reasoning",
            script_source_dir=script_source_dir
        ) as rdfox:
            if print_facts:
                print()
                print("--- Dump of RDFox data: ---")
                print(rdfox.facts())
            yield rdfox

        if not keep_working_dir:
            shutil.rmtree(working_dir)

    return probs_datasource_func
