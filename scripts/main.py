#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd

from popdbgen import DATA_DIR, get_households_population_gdf, load_BAN, load_FILO


def generate_households_population_databases(
    territory: str = "france",
    dataDir: Path = DATA_DIR,
    seed: int = 1703
):
    np.random.seed(seed)

    filo: pd.DataFrame = load_FILO(dataDir=dataDir, territory=territory)
    ban: pd.DataFrame = load_BAN(dataDir=dataDir, territory=territory)

    households_output_file = dataDir / f"households_{territory}.gpkg"
    population_output_file = dataDir / f"population_{territory}.gpkg"
    logging.info(f"Exporting households to {population_output_file}")
    logging.info(f"Exporting population to {population_output_file}")

    hh_it = iter(generate_households(filo_df=filo, ban_df=ban))
    for hh in :
        .to_file(households_output_file, layer="households", driver="GPKG")
        gpd.GeoDataFrame(data=households, geometry="geometry", crs=territory_crs(territory))

        gpd.GeoDataFrame(
            data=[ind for hh in households for ind in population_generator(hh)],
            geometry="geometry",
            crs=territory_crs(territory),
        ),
        for ind in population_generator(hh):


    households, population = get_households_population_gdf(filo_df=filo, ban_df=ban)

    households.to_file(households_output_file, layer="households", driver="GPKG")
    population.to_file(population_output_file, layer="population", driver="GPKG")


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument(
        "-t",
        "--territory",
        dest="territory",
        type=str,
        default="france",
        help="""
        territory to run on (france, 974, 972)
        """,
    )
    argparser.add_argument(
        "-d",
        "--datadir",
        dest="datadir",
        type=str,
        help="""
        path to the data directory
        """,
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        default=False,
        action="store_true",
        help="""
        set logging level to DEBUG
        """,
    )
    argparser.add_argument(
        "-l",
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        dest="loglevel",
        default="INFO",
        type=str.upper,
        help="""
        set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """,
    )
    # Parse arguments
    args = argparser.parse_args()
    # Setup logging level base on -v and -l flags
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
        level="DEBUG" if args.verbose else args.loglevel,
    )

    territories = [t.strip() for t in args.territory.split(",") if t]
    # Run main loop
    for territory in territories:
        logging.info(f"Running generation on territory: {territory}...")
        generate_households_population_databases(
            territory=territory,
            dataDir=Path(args.datadir) if args.datadir else DATA_DIR,
        )
