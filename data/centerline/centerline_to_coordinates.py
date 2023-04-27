import pandas as pd


def get_coords(row):
    """
    Get coordinates from the_geom column
    """
    coords = (
        row["the_geom"].replace("MULTILINESTRING ((", "").replace("))", "").split(", ")
    )
    coords = [c.split(" ") for c in coords]
    coords = [(float(c[1]), float(c[0])) for c in coords]
    return coords


def get_centerpoint(row):
    """
    Get centerpoint of a street
    """
    coords = row["coords"]
    centerpoint = coords[len(coords) // 2]
    return centerpoint


if __name__ == "__main__":
    # Read Manhattan zipcodes
    nyc_zipcodes = pd.read_csv("./data/centerline/NYC_Zipcodes.csv")
    manhattan_zipcodes = nyc_zipcodes[
        nyc_zipcodes["Borough"] == "Manhattan"
    ].ZipCode.values

    # Read centerline data
    centerline = pd.read_csv(
        "./data/centerline/Centerline.csv", usecols=["the_geom", "L_ZIP", "R_ZIP"]
    )

    # filter out non-Manhattan streets
    centerline_manhattan = centerline[
        centerline.L_ZIP.isin(manhattan_zipcodes)
        & centerline.R_ZIP.isin(manhattan_zipcodes)
    ]

    # extract coordinates and points
    centerline_manhattan["coords"] = centerline_manhattan.apply(get_coords, axis=1)
    centerline_manhattan["points"] = centerline_manhattan.apply(get_centerpoint, axis=1)

    # write into results
    with open("./data/coordinates_manhattan.txt", "w") as f:
        for point in centerline_manhattan.points:
            f.write(f"{point[0]},{point[1]}\n")
