from setuptools import setup, find_packages


setup(
    name='vlc-helper',
    version='0.1.6',
    description='CLI helpers for VLC media player',
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/vlc-helper',
    download_url='https://github.com/kenjyco/vlc-helper/tarball/v0.1.6',
    packages=find_packages(),
    install_requires=[
        'chloop',
        'bg-helper',
        'fs-helper',
        'dbus-python',
        'click>=6.0',
    ],
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
    ],
    keywords=['vlc', 'video', 'helper', 'screenshots', 'annotations']
)
