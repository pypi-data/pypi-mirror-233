from setuptools import setup, find_packages

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.1.7'
DESCRIPTION = 'Sending emails and otp verifications is super simple with emailotp'
LONG_DESCRIPTION = 'A package that allows to send emails to specific email with super simple syntax and fast '

# Setting up
setup(
    name="emailotp",
    version=VERSION,
    author="shaik afrid",
    author_email="<afridayan01@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['email','emalilsending','emailotp','emailsending','emailsent','email-send',
    'email-otp','email_otp','email_sending','email-sending','email-','email_','verification',
    'email-verification','email_verification'
    
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)