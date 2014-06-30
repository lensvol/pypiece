# coding: utf-8

import click
import subprocess

@click.command()
@click.argument('req_file')
@click.argument('pip_opts', nargs=-1)
@click.option('--pip', default='pip')
def piecemeal_install(req_file, pip, pip_opts):
    u'''
    Install packages from provided requirements file piece by piece.
    If package installation fails, continue like nothing happened.

    :param req_fn: File with Python packages to install.
    :param timeout: Socket timeout for pip.
    '''

    def show_item(item):
        if item is not None:
            return click.style(item, fg="blue")

    failed_packages = []
    success_packages = []
    already_installed = []

    with open(req_file, 'r') as fp:
        # Load up requirements and filter out comments
        lines = [l.strip() for l in fp.readlines() if not l.startswith('#')]
        # Sort and normalize requirements list, skipping blank lines
        lines = filter(lambda x: x, sorted(list(set(lines))))

        with click.progressbar(lines,
                               label="Processing packages",
                               bar_template="%(label)s [%(bar)s] %(info)s",
                               item_show_func=show_item,
                               show_eta=False,
                               fill_char=click.style('#', fg='green')) as packages:
            for package in packages:
                cmd = [pip, 'install', package]
                cmd.extend(pip_opts)

                try:
                    output = subprocess.check_output(cmd)

                    if output.startswith('Requirement already satisfied'):
                        already_installed.append(package)
                    elif 'Successfully installed' in output:
                        click.echo(output)
                        success_packages.append(package)

                except subprocess.CalledProcessError as call_exc:
                    failed_packages.append(package)

    for title, color, affected in (
            ('Already installed', 'blue', already_installed),
            ('Installed', 'green', success_packages),
            ('Failed', 'red', failed_packages)):
        if affected:
            click.echo()
            click.echo(click.style('[{0}]'.format(title), fg=color))
            click.echo('\n'.join(affected))


if __name__ == '__main__':
    piecemeal_install()
