import datetime
import logging
import multiprocessing
import re
from collections.abc import Iterator
from pathlib import Path

import frontmatter
from citation_title import cite_title
from citation_utils import CountedCitation
from environs import Env
from statute_utils import CountedStatute, setup_local_statute_db

from .dumper import SafeDumper

env = Env()
env.read_env()

DECISIONS = Path().home().joinpath(env.str("DECISIONS_DIR"))
STATUTES = Path().home().joinpath(env.str("STATUTES_DIR"))

logging.debug("Setup statutes database forstatute_utils matching")
setup_local_statute_db(STATUTES)

LACKING_BREAKLINE = re.compile(r"\s{2}\n(?!\n)")


def get_opinion_files_by_year(year: int) -> Iterator[Path]:
    return DECISIONS.glob(f"**/{str(year)}-*/**/*.md")


def clean_text(raw_content: str):
    return LACKING_BREAKLINE.sub("\n\n", raw_content)


def get_date_string(file: Path) -> str:
    # get date string based on the path
    _, _, date_str, _ = file.parts[-4:]
    if "/opinion/" in str(file):
        _, _, date_str, _, _ = file.parts[-5:]
    return date_str


def update_opinion(file: Path):
    """The following libraries are often updated:

    1. `citation-utils`
    2. `statute-utils`
    3. `citation-title`

    When these are updated the outputted metadata will vary.

    In addition, it's possible to add functions that cleans text.

    The entire `update_opinion()` method needs to be wrapped around a process function
    since arbitrary text is involved and the complex regex patterns used by the above
    libraries might result in hanging processes.
    """
    try:
        logging.info(f"Updating opinion: {file.relative_to(DECISIONS)}")
    except ValueError:
        pass

    # convert text from file to frontmatter
    post = frontmatter.load(file)

    # prepare data dictionary, remove fields (if they exist) that will be updated
    data = {
        k: post[k] for k in post.keys() if k not in ("statutes", "citations", "short")
    }

    # if title key exists (separate opinions won't have them), create a short title
    if title := data.get("title"):
        data["short"] = cite_title(title) or title[:20]

    # generate a statute string, if statutes found
    if statutes := "; ".join(
        [
            f"{c.cat.value.lower()} {c.num.lower()}: {c.mentions}"
            for c in CountedStatute.from_source(
                text=post.content,
                document_date=datetime.date.fromisoformat(get_date_string(file)),
                context=str(file.relative_to(DECISIONS)),
            )
        ]
    ):
        data["statutes"] = statutes

    # generate a citation string, if citations found
    if citations := "; ".join(
        [repr(c) for c in CountedCitation.from_source(post.content)]
    ):
        data["citations"] = citations

    # save file with updated statutes and citations
    frontmatter.dump(
        post=frontmatter.Post(post.content, **data), fd=file, Dumper=SafeDumper
    )

    # frontmatter.dump does not include a trailing new line which is
    # a standard for markdown files, a hack is simply to add a new line manually
    # see https://github.com/eyeseast/python-frontmatter/issues/87
    # file.write_text(data=file.read_text() + "\n")


def update_markdown_opinion_file(file: Path, timeout: float = 5):
    """Time-based wrapper around `update_file()` to ensure that it doesn't exceed
    5 seconds in processing the file. If the process is still running at the 5-second
    mark, will terminate.

    Args:
        file (Path): File to update
        timeout (float, optional): Number of seconds before timeout. Defaults to 5.
    """
    process = multiprocessing.Process(target=update_opinion, args=(file,))
    process.start()
    process.join(timeout=timeout)
    if process.is_alive():
        logging.error(f"Took too long: {file=}")
        process.terminate()
        process.join()
