
from distutils.core import setup
setup(
    name='aws-google-saml',
    packages=['aws_google_saml'],
    version='0.7.6',
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
)
