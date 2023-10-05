from pyreqmerger.console import console
from pyreqmerger.enums import Errors, MergeMethod
from pyreqmerger.merger import merge_downgrade, merge_upgrade, translate_dict_to_file
from pyreqmerger.pyreq_parser import setup_parser
from pyreqmerger.req_classes import ReqFileHandler


def main() -> None:
    arg_parser = setup_parser()
    args = arg_parser.parse_args()

    first_req = ReqFileHandler(args.first_req_file)
    sec_req = ReqFileHandler(args.second_req_file)

    output_file = ReqFileHandler(args.output)

    if output_file.valid:
        _ = output_file.self_delete

    if not first_req.valid:
        console.print(f"{Errors.INVALID_FILE_PATH}:[red]  {first_req.path}")
        return

    if not sec_req.valid:
        console.print(f"{Errors.INVALID_FILE_PATH}:[red]  {sec_req.path}")
        return

    output_dict = {}

    match args.method:
        case MergeMethod.UPGRADE:
            output_dict = merge_upgrade(
                first_req.req_content.data, sec_req.req_content.data
            )
        case MergeMethod.DOWNGRADE:
            output_dict = merge_downgrade(
                first_req.req_content.data, sec_req.req_content.data
            )
        case _:
            output_dict = merge_upgrade(
                first_req.req_content.data, sec_req.req_content.data
            )

    output_file.write(translate_dict_to_file(output_dict))
