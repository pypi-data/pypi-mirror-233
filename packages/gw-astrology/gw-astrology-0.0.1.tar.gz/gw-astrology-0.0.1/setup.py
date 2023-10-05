import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

install_requires = [
	"igwn-alert",
	"hop-client",
	"lalsuite"
]

setuptools.setup(
    name="gw-astrology",
    description="Gravitational Wave Astrology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="Becca Ewing",
    author_email="rebecca.ewing@ligo.org",
    url="https://git.ligo.org/rebecca.ewing/gw-astrology.git",
    license="MIT",
    packages=["gw", "gw.astrology"],
    entry_points={
        "console_scripts": [
            "igwn-alert-listener=gw.astrology.igwn_alert_listener:main",
        ],
    },
    python_requires=">=3.6",
    install_requires=install_requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
)

