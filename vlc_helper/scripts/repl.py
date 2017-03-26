import click
import vlc_helper as vh


@click.command()
def main():
    """Start a REPL to control VLC media player"""
    vh.repl()


if __name__ == '__main__':
    main()
