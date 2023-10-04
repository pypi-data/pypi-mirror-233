import sys
import asyncio

from geocollector.api import NCBI
from geocollector.logger import get_logger
from geocollector.cli import parse_args


async def _start():
    args = parse_args(sys.argv[1:])
    logger = get_logger(args.verbosity)
    
    async with NCBI(key=args.api_key, input_df=args.dataframe, logger=logger) as api:
        await api.execute()


def main() -> None:
    asyncio.run(_start())


if __name__ == '__main__':
    main()
