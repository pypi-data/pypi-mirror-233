"""Parses Ansible JSON output and turns it into pretty Markdown output.

Reports on any failures. Optionally reports the 'diffs' for any number of 'crucial tasks'"""
from typing import List
import configargparse

import ntsbuildtools.io
from ntsbuildtools.markdown.comments import MarkdownComment
from ntsbuildtools.ansible.playbook.results import PlaybookResults


def main(args):
    # Parse the json output into a PlaybookResults object
    json_output = ntsbuildtools.io.readfile(args.src)
    results = PlaybookResults.from_json(json_output)

    markdown = render_playbook_result(
        results, args.crucial_task, args.crucial_ansible_module
    )

    with open(args.dst, "w") as dst_file:
        dst_file.write(markdown)


def render_playbook_result(
    results: PlaybookResults,
    crucial_tasks: List[str] = None,
    crucial_ansible_modules: List[str] = None,
) -> str:
    markdown = MarkdownComment()
    if results.has_failures():
        for task_result in results.failures():
            markdown.add_message(task_result.as_markdown())
    if crucial_ansible_modules:
        for ansible_module in crucial_ansible_modules:
            for task_result in results.by_ansible_module(ansible_module):
                if not task_result.has_been_displayed():
                    markdown.add_message(task_result.as_markdown())
    if crucial_tasks:
        for task_name in crucial_tasks:
            for task_result in results.by_task_name(task_name):
                if not task_result.has_been_displayed():
                    markdown.add_message(task_result.as_markdown())
    return str(markdown)


def config_parser(parser: configargparse.ArgParser):
    parser.add_argument(
        "src",
        help="""Path to a Ansible JSON output file. This JSON file should be generated 
                using the "ansible.posix.json" Callback Plugin. (https://docs.ansible.com/ansible/latest/collections/ansible/posix/json_callback.html)""",
    )
    parser.add_argument(
        "dst",
        help="""Path to a file where the output should be saved. 
                NOTE: If the file exists, it's contents will be overwritten.""",
    )
    parser.add_argument(
        '--crucial-task', 
        action='append',
        help="Any particular Ansible Task(s) that should ALWAYS be reported on. Provide the full name of that Ansible Task."
    )
    parser.add_argument(
        "--crucial-ansible-module",
        action="append",
        help="""Select some particular Ansible Module(s) that you'd like to see the results of. E.g. junos_config""",
    )
