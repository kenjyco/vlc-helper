import click
from vlc_helper import vlcstart_precise


@click.command()
@click.argument('filename', nargs=1, default='')
@click.argument('starttime', nargs=1, default='')
@click.argument('stoptime', nargs=1, default='')
def main(filename, starttime, stoptime):
    """Start filename at specific start time (and/or end at specific end time)
    """
    vlcstart_precise(filename, starttime, stoptime)


if __name__ == '__main__':
    main()
