from setuptools import setup

version = '0.16'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django >= 1.4, < 1.7',
    'django-extensions',
    'django-celery',
    'django-nose',
    'lizard-map >= 4.40',      # For Django 1.6.5 support
    'lizard-ui >= 4.40',       # For Django 1.6.5 support
    'lizard-security >= 0.7',  # For Django 1.6.5 support
    'pkginfo',
    'djangorestframework',
    ],

tests_require = [
    ]

setup(name='lizard-task',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='TODO',
      author_email='TODO@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_task'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
