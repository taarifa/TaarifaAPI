from setuptools import setup

dependency_links = ['git+https://github.com/nicolaiarocci/eve#egg=Eve-0.4-dev']
setup(name='TaarifaAPI',
      version='dev',
      description='The Taarifa API for managing resources and requests',
      long_description=open('README.rst').read(),
      author='The Taarifa Organisation',
      author_email='taarifadev@gmail.com',
      url='http://taarifa.org',
      download_url='https://github.com/taarifa/TaarifaAPI',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      packages=['taarifa_api'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['Eve==0.4-dev', 'Eve-docs==0.1.3'],
      dependency_links=dependency_links)
