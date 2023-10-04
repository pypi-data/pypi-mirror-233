lorcania-cli is an unofficial CLI to work with [Lorcania](https://lorcania.com/), a website to collect your [Lorcana](https://www.disneylorcana.com/) cards.
Lorcania provides a valuable service for the community and this utility is not ment to replace it, but rather to allow (currently: me) to obtain a local backup for my collection.

It currently only allows to:

- Get your collection of Lorcana cards.

# Installation

```
pip install lorcania-cli
```

# Usage

To get your collection at the command line

```bash
$ lorcania-cli collection show "<e-mail address used for Lorcania>"
Password: "<Lorcania password>"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ collection                                                                                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ rarity_collection                                                           foil  op  regular │
│ card_set_id number name                        title                                          │
│ 1           1      Mickey Mouse                Brave Little Tailor                            │
...
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

You can also use environment variables or an .env file to store your credentials:

```bash
LORCANIA_EMAIL="<e-mail address used for Lorcania>"
LORCANIA_PASSWORD="<Lorcania password>"
```

Then, you can directly use

```
lorcania-cli
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ collection                                                                                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ rarity_collection                                                           foil  op  regular │
│ card_set_id number name                        title                                          │
│ 1           1      Mickey Mouse                Brave Little Tailor                            │
...
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

Please always remember, that your credentials are secrets and should not be stored in version control.

To get your collection as an excel file (here: `my-collection.xlsx`), use

```
$ lorcania-cli collection show --out-file my-collection.xlsx
```

# Test

To test lorcania-cli, use `pytest`.
In order to don't waste Lorcania resources, a vcr.py suite is included for an account with the following collection:

- _Mickey Mouse Detective_ (Promo): 1x
- _Ariel - On Human Legs_ (The First Chapter): 2x (regular)
- _Cinderella - Gentle and Kind_ (The First Chapter): 1x (regular), 2x (foil)

If you want to extend lorcania-cli and need to run tests against real Lorcania, I recommend to

- create a lorcania account for this purpose
- add the above cards
- add any other cards as required for your use case
- delete the vcr.py cassettes at `tests/cassettes`
- make the credentials to your lorcania test account available in `.env.tests` (which is ignored via .gitignore)
- rerun `pytest`
