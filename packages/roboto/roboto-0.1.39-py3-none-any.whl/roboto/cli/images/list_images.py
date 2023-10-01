#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...image_registry import ImageRegistry
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def list_images(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    paginated_results = image_registry.list_images(
        repository_name=args.repository_name, org_id=args.org
    )
    while True:
        for image in paginated_results.items:
            print(json.dumps(image.dict(), indent=2))
        if paginated_results.next_token:
            paginated_results = image_registry.list_images(
                repository_name=args.repository_name,
                page_token=paginated_results.next_token,
                org_id=args.org,
            )
        else:
            break


def list_images_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)

    parser.add_argument(
        "--repository-name",
        dest="repository_name",
        action="store",
        help="Filter list of images by repository name.",
    )


ls_images_command = RobotoCommand(
    name="ls",
    logic=list_images,
    setup_parser=list_images_parser,
    command_kwargs={"help": "List container images hosted in Roboto's image registry."},
)
