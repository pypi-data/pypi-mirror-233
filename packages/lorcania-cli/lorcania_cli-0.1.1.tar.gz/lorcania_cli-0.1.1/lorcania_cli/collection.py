from pathlib import Path
from typing import Annotated, Optional
from rich.console import Console
from rich.table import Table
import pandas as pd
import typer
from lorcania_cli.api.lorcania import LorcaniaAPI


app = typer.Typer()


def float_formatter(f: float):
    return "{:.0f}".format(f)


@app.command()
def show(
    email: Annotated[str, typer.Argument(envvar="LORCANIA_EMAIL")],
    password: Annotated[
        str, typer.Option(prompt=True, hide_input=True, envvar="LORCANIA_PASSWORD")
    ],
    out_file: Annotated[
        Optional[Path],
        typer.Option(
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
):
    api = LorcaniaAPI(email, password)

    tabulated_collection = tabulate_collection(api)

    if out_file:
        tabulated_collection.to_excel(out_file)
    else:
        table_as_string = tabulated_collection.to_string(
            float_format=float_formatter,
            na_rep="",
        )
        console = Console()
        table = Table("collection")
        table.add_row(table_as_string)
        console.print(table)


def tabulate_collection(api: LorcaniaAPI):
    cards = api.cards()["cards"]
    cards_df = pd.DataFrame(cards)

    collection = api.collection()["collection"].values()
    collection_df = pd.DataFrame(
        [
            {"rarity": card_type, **card_data}
            for card_types in collection
            for card_type, card_data in card_types.items()
        ]
    )

    joined_collection = pd.merge(
        cards_df,
        collection_df,
        left_on="id",
        right_on="card_id",
        suffixes=("_card", "_collection"),
        how="outer",
    )

    table = joined_collection[
        ["card_set_id", "number", "name", "title", "rarity_collection", "quantity"]
    ]
    table.loc[:, ["title"]] = table.loc[:, ["title"]].fillna("")

    tabulated_collection = table.pivot(
        index=["card_set_id", "number", "name", "title"],
        columns="rarity_collection",
        values="quantity",
    )

    # remove the nan column generated via the pivot due to pivoting rows for cards which
    # are not in our collection
    tabulated_collection.dropna(axis=1, how="all", inplace=True)

    return tabulated_collection
