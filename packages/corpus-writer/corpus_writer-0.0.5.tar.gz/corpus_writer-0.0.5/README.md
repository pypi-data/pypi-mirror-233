# corpus-writer

![Github CI](https://github.com/justmars/corpus-writer/actions/workflows/main.yml/badge.svg)

Update pre-existing opinion file (in markdown front-matter) with statutes, citations, short title.

The _decisions_ / _statutes_ directories needs to be configured via an `.env` file, see `just dumpenv` for an

## Steps

1. Delete the statutes database since this may have been previously updated via their original yaml files
2. The lack of a statutes database will cause a rebuild of the same

Run the following python command:

```py
from corpus_writer import get_opinion_files_by_year, update_markdown_opinion_file

for i in range(1900, 1946):
    for file in get_opinion_files_by_year(year=i):
        update_markdown_opinion_file(file=file)
```

Note that for cases like `am/97-9-282-rtc/1998-04-22/main-123.md` where it takes too long to determine citations (likely a recursive regex error), a timer of 5 seconds is used by `update_markdown_opinion_file`.
