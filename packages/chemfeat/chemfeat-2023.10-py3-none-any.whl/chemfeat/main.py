#!/usr/bin/env python
'''
Command-line utility for calculating chemical features.
'''

import argparse
import contextlib
import json
import logging
import pathlib
import sys

import yaml
import pandas as pd

from chemfeat.database import FeatureDatabase
from chemfeat.features.manager import FeatureManager, import_calculators


LOGGER = logging.getLogger(__name__)


@contextlib.contextmanager
def open_file_or_stdout(path=None, log_msg=None):
    '''
    Context manager for retrieving a handle to an open file or STDOUT.

    Args:
        path:
            An optional file path. It will be created and opened if write mode
            if given.

        log_msg:
            An optional log message to log as INFO when a path is given. It
            should include a single placeholder for the file path.

    Returns:
        The open file handle or the STDOUT object.
    '''
    if path is None:
        yield sys.stdout
    else:
        path = pathlib.Path(path).resolve()
        if log_msg:
            LOGGER.info(log_msg, path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as handle:
            yield handle


def calculate_features(pargs):
    '''
    Calculate chemical features for the requested InChIs.
    '''
    LOGGER.info('Calculating chemical features.')
    inchi_column = pargs.inchi
    in_path = pargs.input.resolve()
    LOGGER.info('Loading InChIs from %s', in_path)
    inchis = pd.read_csv(in_path)[inchi_column]

    if inchis.empty:
        LOGGER.warning('No InChIs found in %s', in_path)
        return 1

    feat_specs_path = pargs.feat_spec
    with feat_specs_path.open('r', encoding='utf-8') as handle:
        feat_specs = yaml.safe_load(handle)

    feat_db_path = pargs.database.resolve()
    feat_db_path.parent.mkdir(parents=True, exist_ok=True)
    feat_db = FeatureDatabase(feat_db_path)

    out_path = pargs.output.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    feat_man = FeatureManager(feat_db, feat_specs)
    if not feat_man.feature_calculators:
        LOGGER.error('No valid features sets were configured: %s', feat_specs_path)
        return 1
    feat_man.calculate_features(inchis, output_path=out_path)
    return 0


def _descibe_lines():
    '''
    '''
    yield '# Feature Sets'
    yield ''
    for _name, calc in sorted(import_calculators().items()):
        yield from calc.get_description(level=2)


def describe_feature_sets(pargs):
    '''
    Generate descriptions of each feature set.
    '''
    LOGGER.info('Generating feature set descriptions.')
    lines = _descibe_lines()
    with open_file_or_stdout(
        path=pargs.output,
        log_msg='Saving descriptions to %s'
    ) as handle:
        for line in lines:
            handle.write(f'{line}\n')
    return 0


def _write_yaml_configuration(handle, comment=True):
    '''
    Write the YAML configuration file to an open file handle.

    Args:
        handle:
            The open file handle.

        comment:
            If True, comment all lines.
    '''
    comment_prefix = '# '
    prefix = comment_prefix if comment else ''
    for name, calc in sorted(import_calculators().items()):
        obj = calc()
        handle.write(
            f'{comment_prefix}{calc.get_short_description()}\n'
            f'{prefix}- name: {name}\n'
        )
        params = obj.parameters
        if params:
            for line in yaml.dump(params).strip().split('\n'):
                handle.write(f'{prefix}  {line}\n')
        handle.write('\n')


def _write_json_configuration(handle):
    '''
    Write the JSON configuration file to an open file handle.

    Args:
        handle:
            The open file handle.
    '''
    conf_list = []
    for name, calc in sorted(import_calculators().items()):
        obj = calc()
        entry = {
            'name': name
        }
        params = obj.parameters
        if params:
            entry.update(params)
        conf_list.append(entry)
    json.dump(conf_list, handle, indent=2)


def configure_feature_sets(pargs):
    '''
    Generate a commented feature-set configuration file.
    '''
    if pargs.json:
        pargs.no_comment = True
    with open_file_or_stdout(
        path=pargs.output,
        log_msg='Saving configuration file to %s'
    ) as handle:
        if pargs.json:
            _write_json_configuration(handle)
        else:
            _write_yaml_configuration(handle, comment=not pargs.no_comment)
    return 0


def parse_args(args=None):
    '''
    Parse command-line arguments.

    Args:
        args:
            Command-line arguments. If None, sys.argv is used.

    Returns:
        The command-line arguments parsed with argparse.

    TODO:
        Add option to configure feature calculator import paths.
    '''
    parser = argparse.ArgumentParser(
        description='Calculate chemical features.'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debugging messages.'
    )
    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='Available subcommands',
        dest='command'
    )

    # ------------------------------ calculate ------------------------------- #
    calc_parser = subparsers.add_parser(
        'calculate',
        aliases=['calc'],
        help='Calculate chemical features from InChIs.'
    )
    calc_parser.add_argument(
        'feat_spec',
        metavar='<YAML file>',
        type=pathlib.Path,
        help='A YAML file specifying the features to calculate.'
    )
    calc_parser.add_argument(
        'input',
        metavar='<CSV file>',
        type=pathlib.Path,
        help=('''
            A CSV file containing a column with the InChIs of the molecules for
            which the features should be calulated.'
        ''')
    )
    calc_parser.add_argument(
        'output',
        metavar='<CSV file>',
        type=pathlib.Path,
        help=('''
              The path to which the calculated features should be saved as a CSV
              file.
        ''')
    )
    calc_parser.add_argument(
        '-i', '--inchi',
        metavar='<InChI column name>',
        default='InChI',
        help=('''
            The name of the column containing InChI values in the input file. It
            will also be used in the output file. Default: %(default)s
        ''')
    )
    calc_parser.add_argument(
        '-d', '--database',
        metavar='<SQLite database file>',
        default='features.sqlite',
        type=pathlib.Path,
        help=('''
            The path to an SQLite database in which to cache calculated features
            for re-use. Default: %(default)s
        ''')
    )
    calc_parser.set_defaults(func=calculate_features)

    # ------------------------------ configure ------------------------------- #
    conf_parser = subparsers.add_parser(
        'configure',
        aliases=['conf'],
        help='Generate a template configuration file.'
    )
    conf_parser.add_argument(
        '--no-comment',
        action='store_true',
        help=(
            'Uncomment all options. '
            'This is useful when parsing the configuration file programmatically.'
        )
    )
    conf_parser.add_argument(
        '-j', '--json',
        action='store_true',
        help=(
            'Output JSON instead of YAML. '
            'This implies --no-comment as JSON does not support comments.'
        )
    )
    conf_parser.add_argument(
        '-o', '--output',
        metavar='<path>',
        type=pathlib.Path,
        help=(
            'Save the generated template to <path>. '
            'The default output format is YAML.'
        )
    )
    conf_parser.set_defaults(func=configure_feature_sets)

    # ------------------------------- describe ------------------------------- #
    desc_parser = subparsers.add_parser(
        'describe',
        aliases=['desc'],
        help='Describe the available chemical features.'
    )
    desc_parser.add_argument(
        '-o', '--output',
        metavar='<Markdown file>',
        type=pathlib.Path,
        help='Save the output to <Markdown file>.'
    )
    desc_parser.set_defaults(func=describe_feature_sets)


    return parser.parse_args(args=args)


def main(args=None):
    '''
    Parse command-line arguments and perform requested functions.

    Args:
        Passed through to parse_args().
    '''
    pargs = parse_args(args=args)
    logging.basicConfig(
        style='{',
        format='[{asctime}] {levelname} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=(logging.DEBUG if pargs.debug else logging.INFO)
    )
    return pargs.func(pargs)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (KeyboardInterrupt, BrokenPipeError):
        pass
