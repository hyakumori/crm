#!/usr/bin/env python3
import os
import pickle
import sys
from pathlib import Path

import click
import pandas as pd
from dotenv import load_dotenv

from data_import.utils import cell_value

load_dotenv(Path(__file__).parent.joinpath(".env"))

EXCEL_FILE_PATH = Path(os.getenv("ORIGINAL_XLSX_PATH"))
EXCEL_PICKLE_FILE_PATH = EXCEL_FILE_PATH.parent.joinpath(
    EXCEL_FILE_PATH.name + ".pickle"
)
MASTER_DATA_PICKLE_FILE_PATH = EXCEL_FILE_PATH.parent.joinpath("master-data.pickle")


@click.group()
def cli():
    pass


@cli.command()
def xlsx_to_pickle():
    print("Importing from XLSX ... ", end="", flush=True)
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None, parse_dates=True)
    print("DONE")
    print("Writing to pickle ... ", end="", flush=True)
    pickle.dump(df, open(EXCEL_PICKLE_FILE_PATH, "wb"))
    print("DONE")


def load_data():
    if not EXCEL_PICKLE_FILE_PATH.exists():
        xlsx_to_pickle()
    else:
        print("Importing from PICKLE ... ", end="", flush=True)
        df = pickle.load(open(EXCEL_PICKLE_FILE_PATH, "rb"))
        print("DONE")

    customer = df["顧客情報一覧"]
    forest = df["森林情報一覧"]

    return dict(
        customer=customer,
        forest=forest,
    )


def import_customer(data):
    from data_import.importer.customer import CustomerImporter as Importer

    importer = Importer(data.get("customer"))
    importer.run()
    importer.validate()
    return importer


def import_forest(data):
    from data_import.importer.forest import ForestImporter as Importer

    importer = Importer(data.get("forest"))
    importer.run()
    return importer


def generate_master_pickle(forest, customer):
    if click.confirm("This will override old master file. Continue?"):
        master = dict()
        data = load_data()

        if customer:
            print("Importing Customer ... ", end="", flush=True)
            master["customer"] = import_customer(data).results
            print("OK")

        if forest:
            print("Importing Forest ... ", end="", flush=True)
            master["forest"] = import_forest(data).results
            print("OK")

        pickle.dump(master, open(MASTER_DATA_PICKLE_FILE_PATH, "wb"))


@cli.command('gen-master')
@click.option("--forest", default=False, help="import forest", type=bool)
@click.option("--customer", default=False, help="import customer", type=bool)
def command_generate_master(forest, customer):
    generate_master_pickle(forest, customer)


@cli.command()
def rm_xlsx_pickle():
    if click.confirm("Do you want to continue?"):
        if EXCEL_PICKLE_FILE_PATH.exists():
            os.remove(EXCEL_PICKLE_FILE_PATH)

        click.echo(f"Deleted {EXCEL_PICKLE_FILE_PATH}")


@cli.command()
def truncate_db():
    """
    This will truncate all related database tables. Use with caution.
    """
    if click.confirm("Do you REALLY want to continue?"):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                """
                truncate table crm_forestcustomer cascade;
                truncate table crm_customercontact cascade;
                truncate table crm_attachment cascade;
                truncate table crm_archiveforest cascade;
                truncate table crm_forest cascade;
                truncate table crm_archivecustomer cascade;
                truncate table crm_archive cascade;
                truncate table crm_contact cascade;
                truncate table crm_customer cascade;
            """
            )

        click.echo("OK")


def insert_db(forest, customer):
    from data_import.config import setup_django, setup_path

    setup_path()
    setup_django()

    data = pickle.load(open(MASTER_DATA_PICKLE_FILE_PATH, "rb"))

    if customer:
        from data_import.db_importer.customer import CustomerDbImporter
        print("INSERTING CUSTOMER")
        CustomerDbImporter.insert_db(data["customer"])
        print("DONE")

    if forest:
        from data_import.db_importer.forest import ForestDbImporter
        print("INSERTING FOREST")
        ForestDbImporter.insert_db(data["forest"])
        print("DONE")


@cli.command('insert-db')
@click.option("--forest", default=False, help="import forest", type=bool)
@click.option("--customer", default=False, help="import customer", type=bool)
def command_insert_db(forest, customer):
    insert_db(forest, customer)
    click.echo("FINISHED")


def create_link_forest_customer():
    from data_import.config import setup_django, setup_path

    setup_path()
    setup_django()

    data = pickle.load(open(MASTER_DATA_PICKLE_FILE_PATH, "rb"))
    from data_import.db_importer.relations import RelationDbImporter

    importer = RelationDbImporter(data)
    importer.search_customers()
    importer.link_forest_customer()


@cli.command('link-forest-customer')
def command_link_corest_customer():
    create_link_forest_customer()
    click.echo("DONE")


if __name__ == "__main__":
    # generate_master_pickle(True, True)
    # insert_db(forest=True, customer=False)
    # create_link_forest_customer()
    cli()
