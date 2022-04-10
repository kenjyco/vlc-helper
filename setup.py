from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

with open('requirements.txt', 'r') as fp:
    requirements = fp.read().splitlines()

setup(
    name='vlc-helper',
    version='0.1.7',
    description='CLI helpers for VLC media player',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/vlc-helper',
    download_url='https://github.com/kenjyco/vlc-helper/tarball/v0.1.7',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '': ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'myvlc=vlc_helper.scripts.myvlc:main',
            'vlc-repl=vlc_helper.scripts.repl:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    keywords=['vlc', 'video', 'video player', 'cli', 'command-line', 'repl', 'dbus', 'screenshots', 'annotations', 'helper', 'kenjyco']
)
