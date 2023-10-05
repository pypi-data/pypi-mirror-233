
from distutils.core import setup
setup(
    name='aws-google-saml',
    packages=['aws_google_saml'],
    version='0.8.5',
    license='MIT',
    description='A user-browser driven SAML authentication tool for AWS',
    author='bengieeee',
    url='https://github.com/bengieeee/aws-google-saml',
    download_url='https://github.com/bengieeee/aws-google-saml/archive/refs/tags/0.7.1.tar.gz',
    # Keywords that define your package best
    keywords=['aws', 'aws-cli', 'saml', 'google', 'google-saml', 'google-saml-aws'],
    install_requires=[            # I get to this in a second
        'ET',
        'botocore',
        'boto3',
        'configparser',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'aws-google-saml=aws_google_saml.__main__:main',
        ],
    },
    package_data={
        'aws_google_saml': ['authed.html'],
    }
)
