import letsql


def test_connect(data_dir):
    con = letsql.connect(
        config={"table": data_dir / "parquet" / "functional_alltypes.parquet"}
    )
    yellow_trips = con.table("table")

    assert yellow_trips.head().to_pandas() is not None


def test_interactive(data_dir):
    con = letsql.connect()
    t = con.read_parquet(data_dir / "parquet" / "functional_alltypes.parquet")
    res = t.group_by(["id"]).agg(letsql._.count())

    assert res is not None


def test_connect_to_postgresql():
    conn = letsql.connect()
    t = conn.register("postgresql://user:pass@localhost:5432/cars", "cars")
    assert t.head().execute() is not None


def test_join_over_multiple_data_sources(data_dir):
    con = letsql.connect()
    all_types = con.register(
        data_dir / "parquet" / "functional_alltypes.parquet", "all_types"
    )
    cars = con.register("postgresql://user:pass@localhost:5432/cars", "cars")
    res = (
        all_types.join(cars, all_types["smallint_col"] == cars["company_id"])
        .head()
        .to_pandas()
    )
    assert res is not None
