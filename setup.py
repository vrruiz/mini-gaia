import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minigaia",
    version="1.0.0",
    author="Víctor R. Ruiz",
    author_email="rvr@infoastro.com",
    description="Tools to convert and read Gaia DR2 files to binary format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vrruiz/minigaia",
    packages=['minigaia', 'minigaia.db', 'minigaia.dr2'],
    entry_points={
        'console_scripts': [
            'minigaia_convert=minigaia.convert:main',
            'minigaia_download=minigaia.download:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=True,
)
