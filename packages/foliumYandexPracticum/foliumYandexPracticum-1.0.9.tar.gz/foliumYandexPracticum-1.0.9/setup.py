from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='foliumYandexPracticum',
  version='1.0.9',
  author='data.practicum',
  author_email='data.practicum@yandex.ru',
  description='Folium library with local version of map',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://python-visualization.github.io/',
  packages = ['foliumYandexPracticum',
              'foliumYandexPracticum/templates',
              'foliumYandexPracticum/plugins'],
  include_package_data=True,
  package_data={'foliumYandexPracticum/templates':['*'],
                'foliumYandexPracticum/plugins':['*'],},
  install_requires=['branca',
                    'Jinja2',
                    'numpy',
                    'requests'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://python-visualization.github.io/folium/latest/user_guide.html'
  },
  python_requires='>=3.7'
)