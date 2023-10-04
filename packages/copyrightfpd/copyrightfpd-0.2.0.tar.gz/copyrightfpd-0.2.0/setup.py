from setuptools import setup, find_packages

setup(
    name='copyrightfpd',
    version='0.2.0',
    url='https://github.com/your_username/your_package_name',
    author='Abdelrahman Jamal',
    author_email='abdelrahmanjamal5565@gmail.com',
    description="""Created as a part of the 2023 Google Summer of Code project:
     Reducing Fossology\'s False Positive Copyrights, the purpose is to be able to
     predict whether a given copyright output from the Fossology software
     is a false positive or not.""",
    packages=find_packages(where='src',),
    package_dir = {"": "src"},
    install_requires=[
        'spacy>=3.0.0',
        'joblib>=1.0.0',
        'pandas>=1.1.0',
        'scikit-learn>=1.3.0',
        # add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        # add other classifiers
    ],
    include_package_data=True,
    include_dirs=['src/copyrightfpd/models/ner_model'],
    package_data={'': ['src/copyrightfpd/models/*.pkl', 'src/copyrightfpd/models/*.']},
    python_requires='>=3.6',
)
