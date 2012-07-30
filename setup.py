# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0a1.dev0'
description = "Content types for OpenMultimedia projects."
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='openmultimedia.contenttypes',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity',
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/desarrollotv/openmultimedia.contenttypes',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['openmultimedia'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'openmultimedia.api',
        'plone.app.dexterity>=1.2.1',
        'plone.app.referenceablebehavior',
        'collective.nitf',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
