from setuptools import setup

setup(name='TaarifaAPI',
      version='0.1.0',
      description='The Taarifa API for managing resources and requests',
      long_description=open('README.rst').read(),
      author='Florian Rathgeber',
      author_email='florian.rathgeber@gmail.com',
      license='Apache License, Version 2.0',
      url='http://taarifa.org',
      download_url='https://github.com/taarifa/TaarifaAPI',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      packages=['taarifa_api'],
      entry_points={"console_scripts":
                    ["taarifa_api = taarifa_api.taarifa_api:main"]},
      include_package_data=True,
      zip_safe=False,
      install_requires=['Eve==0.6.1',
                        'Eve-docs==0.1.4',
                        'Flask-Compress==1.3.0'])
