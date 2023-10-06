import typing as t
import click

LengthUnits = t.Literal["m", "cm", "mm", "in"]
ALL_LENGTH_UNITS: t.List[LengthUnits] = ["m", "cm", "mm", "in"]


@click.command
@click.option("--outdir", type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option("--verbose/--no-verbose", default=True)
@click.argument("from_units", type=click.Choice(ALL_LENGTH_UNITS), metavar="FROM_UNITS")
@click.argument("to_units", type=click.Choice(ALL_LENGTH_UNITS), metavar="TO_UNITS")
@click.argument("mesh_path", nargs=-1, type=click.Path(exists=True))
def convert_units(
    from_units: LengthUnits,
    to_units: LengthUnits,
    mesh_path: t.Tuple[str],
    outdir: t.Optional[str],
    verbose: bool,
):
    import os
    from lacecore import load_obj

    def pif(message: str) -> None:
        if verbose:
            click.echo(message, err=True)

    for this_mesh_path in mesh_path:
        if outdir is None:
            filename, extension = os.path.splitext(os.path.basename(this_mesh_path))
            output_path = f"{filename}_{to_units}{extension}"
        else:
            output_path = os.path.join(outdir, os.path.basename(this_mesh_path))

        pif(
            f"Converting {this_mesh_path} from {from_units} to {to_units}",
        )

        load_obj(this_mesh_path).units_converted(
            from_units=from_units, to_units=to_units
        ).write_obj(output_path)

        pif(f"  Wrote {output_path}")


if __name__ == "__main__":  # pragma: no cover
    convert_units()
