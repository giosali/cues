import pathlib
import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

requirements = []

test_requirements = [
    'codecov',
    'coverage',
    'pytest',
    'pytest-cov'
]

main = pathlib.Path(__file__).parent
about = {}
with open(main / 'cues' / '__version__.py', 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    license=about['__license__'],
    packages=setuptools.find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    keywords=['cues', 'prompts', 'questions', 'inquire',
              'enquire', 'interview', 'ask'],
    install_requires=requirements,
    tests_require=test_requirements,
    project_urls={
        'Source': 'https://github.com/GBS3/cues'
    }
)
