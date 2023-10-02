import setuptools

setuptools.setup(
    name="peaqoffpeak",
    version="0.1.3",
    author="Magnus Eldén",
    description="Partial wrapper for Svk Mimer Api",
    license="CC-NC-ND",
    packages=[
        "peaqoffpeak", 
        "peaqoffpeak.models"
        ],
    install_requires=[
          'requests',
      ],
)   