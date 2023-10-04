import censusdis.data as ced
from censusdis.states import NY


def ny_water():
    gdf_ny = ced.download(
        "acs/acs5", 2021, "B19013_001E", with_geometry=True, remove_water=True, state=NY
    )

    return gdf_ny


def main():
    ny_water()


if __name__ == "__main__":
    main()
