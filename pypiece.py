# coding: utf-8

import click
import subprocess

@click.command()
@click.argument('req_file')
@click.option('--timeout', default=45, help="Set pip socket timeout.")
@click.option('--retries', default=3, help="Set number of retries before giving up.")
def piecemeal_install(req_file, timeout, retries):
    u'''
    Install packages from provided requirements file piece by piece.
    If package installation fails, continue like nothing happened.

    :param req_fn: File with Python packages to install.
    :param timeout: Socket timeout for pip.
    :param retries: Times to retry installing package before giving up.
    '''

    def show_item(item):
        if item is not None:
            return click.style(item, fg="blue")

    failed_packages = []

    with open(req_file, 'r') as fp:
        # Load up requirements and filter out comments
        lines = [l.strip() for l in fp.readlines() if not l.startswith('#')]
        # Sort and normalize requirements list, skipping blank lines
        lines = filter(lambda x: x, sorted(list(set(lines))))

        with click.progressbar(lines,
                               label="Installing packages",
                               bar_template="%(label)s [%(bar)s] %(info)s",
                               item_show_func=show_item,
                               show_eta=False,
                               fill_char=click.style('#', fg='green')) as packages:
            for package in packages:
                cmd = ['pip', 'install', package,
                       '--timeout', unicode(timeout)]

                try:
                    output = subprocess.check_output(cmd)
                except subprocess.CalledProcessError as call_exc:
                    failed_packages.append(package)

    if failed_packages:
        click.echo()
        click.echo(click.style('[Failed]', fg='red'))
        click.echo('\n'.join(failed_packages))


if __name__ == '__main__':
    piecemeal_install()
