from setuptools import setup

setup(
    name = 'iterm2_colour_export',
    version = '0.0.1',
    description = 'iterm2 colour export.',
    #TODO
    # long_description = '',
    license = 'MIT',
    author = 'Warren Moore',
    author_email = 'warren@wamonite.com',
    url = 'https://github.com/wamonite/iterm2_colour_export',
    #TODO
    # classifiers = [
    # ],
    packages = ['iterm2_colour_export'],
    entry_points = dict(console_scripts = ['iterm2_colour_export=iterm2_colour_export.script:run']),
    #TODO
    # package_data = {
    # },
    # install_requires = [],
    # setup_requires = [],
    # tests_require = [],
    zip_safe = False
)
