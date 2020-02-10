# CLI

The `cli` submodule of Efficacy contains the source code and functionality for the command-line application version of the Efficacy compiler.

## `run_cli`
Start the main process for the CLI application.
    
**Arguments**

- `with_args`: (Optional) The arguments to run the CLI with. Will default to `sys.argv` if no arguments have been supplied.

!!! example
    Below is an example of how the CLI can be called programmatically using `run_cli()`.
    
    ```python
    from efficacy.cli import run_cli
    from subproccess import check_call

    print(check_call(run_cli(["-i", "main.ocls", "-oT", "tokens.json"])))
    ```