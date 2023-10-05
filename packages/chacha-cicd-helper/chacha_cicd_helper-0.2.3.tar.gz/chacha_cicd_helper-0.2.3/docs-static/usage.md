# Usage

/// note
This helper aim to be used by pychachadummyproject template instantiation.
///

```console
/> <python_bin> -m chacha_cicd_helper -h
usage: chacha-cicd-helper [-pp PROJECTPATH] [-tc] [-ut] [-cc] [-qc] [-dg] [-pdf] [-cpc] [-h]

A bundle of cicd helper tools

optional arguments:
  -pp PROJECTPATH, --projectpath PROJECTPATH
                        path of the python project to process
  -tc, --typecheck      enable static typing check
  -ut, --unittest       enable unit-test
  -cc, --coveragecheck  enable unit-test coverage check (requires unit-test)
  -qc, --qualitycheck   enable code quality check
  -dg, --docgen         enable documentation generation using MkDoc
  -pdf, --docgenpdf     enable pdf documentation export (requires doc-gen)
  -cpc, --complexitycheck
                        enable complexity check
  -h, --help            show this help message and exit
```


Calling those commands will create a directory called `helpers-results` in `<PROJECTPATH>`  (or in the current directory).

This directory will contain some of the following subdirectory, depending on what enabled:

| Directory             | Content                                     |
|-----------------------|---------------------------------------------|
| cl_complexity_check   | code complexity measurement report          |
| cl_doc_gen            | mkdocs documentation output (html + pdf)    |
| cl_quality_check      | quality check reports                       |
| cl_quality_check      | quality check reports                       |
| cl_types_check        | type check reports                          |
| cl_unit_test          | unit test reports                           |
| cl_unit_test_coverage | unit test coverage reports                  |
| cl_unit_test_full     | full unitest report (merged)                |

/// warning
 <docgen> needs a docs-static directory in the target project root. Then one can put any .md file inside.
///
