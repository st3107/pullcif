import typing
import fire


def main(output_dir: str, query: str = None, config: typing.Dict[str, typing.Any] = None) -> None:
    """Download the CIF files from the Materials Project Database.

    Parameters
    ----------
    output_dir :
        The output directory. The cif files will be saved there.
    query :
        The query for the cif files. It will be parsed and used as the filter to search in database.
    config :
        The configuration for the functionality.

    Returns
    -------
    None.
    """
    if config is None:
        config = {}
    if query is None:
        query = ""
    pass


def cli():
    """The cli interface."""
    fire.Fire(main)
