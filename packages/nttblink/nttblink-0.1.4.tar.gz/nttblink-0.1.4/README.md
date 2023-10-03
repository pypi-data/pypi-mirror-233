# NTTBlink: An Elegant Solution for Secrets and Documents Management

NTTBlink Python is a sophisticated Python module that presents a seamless way to handle automation secrets and documents

## Installation

The installation of NTTBlink is a walk in the park, facilitated by pip:

```bash
pip install nttblink

```

Now, NTTBlink stands ready for your command.

Usage

The charm of Python lies in its simplicity and power, traits that NTTBlink embodies fully. Here's a step-by-step guide on how to wield this power:

## Import the Package
Start your journey by invoking the magic of NTTBlink.

```python
from nttblink import Blink
blink = Blink()
```

## Set Environment Variables for Secrets
With a single command, normalize your secrets - remove spaces, transform to uppercase, and set them as environment variables.  This is a easy one liner to get your secrets into your environment.

```python
blink.secret_set_to_env()
```

## Create a New Secret
Creating a new secret is as easy as whispering to a trusted friend. Provide the key, a description, and the secret itself as a dictionary.

```python
new_secret = blink.secret_create('secretname', 'secret description', {'key': 'value'})
```

## List All Secrets
Summon the catalogue of all secrets at your disposal.

```python
secrets = blink.secret_list()
for secret in secrets:
    print(secret)
```
## Unveil Secret Details
Peek into the contents of each secret, illuminating the hidden truth.

``` python
for secret in secrets:
    secret_details = blink.secret_get(secret['id'])
    print(secret_details)
```    
## Enumerate All Documents
With NTTBlink, documents are at your fingertips. List them with ease.

``` python

documents = blink.document_list()
for document in documents:
    print(document)
```

## Store Each Document
Let no document be left unread. NTTBlink empowers you to retrieve each document and save it to your local directory.

``` python
for document in documents:
    blink.document_download(document['id'],document['name'])
```   

## Upload a New Document
With NTTBlink, you can upload a new document to your project. Simply provide the path to the document and the name you wish to give it.

``` python
blink.document_upload('path/to/document', 'documentname.txt')
```

With NTTBlink, you have a versatile tool to manage secrets and documents effortlessly. Enjoy this power responsibly.

# Environment Variables

To breathe life into NTTBlink, we need to supply it with the correct environment variables. These variables serve as the keys to the realm, enabling interactions with the Blink project.

To establish these variables, you'll need to venture to the developer panel on your project page in Blink and collect the correct values. As a guiding beacon, we provide a sample environment file for testing your Python scripts:

```bash
# Sample .env file

BLINK_PROJECT_ID = "622a1fab001900435372fecfb8fd8a13"
BLINK_TOKEN = "qwk23q8aaskqwu2iqasmasdf"
BLINK_BASE_URL = "https://am-automate.nttltd.global.ntt"
BLINK_AUTOMATION_ID = 9
```
Here's a brief explanation of each variable:

BLINK_PROJECT_ID: This is the unique identifier of your Blink project. It tells NTTBlink which project it should interact with.

BLINK_TOKEN: This is your authorization token. It's like the passport for NTTBlink, granting it permission to perform operations in your Blink project.

BLINK_BASE_URL: This is the base URL for your Blink instance. It's the address that NTTBlink will visit to carry out your commands.

BLINK_AUTOMATION_ID: This is the identifier for the specific automation you are working with.
Remember to replace the values in the sample .env file with your actual data.

For safety reasons, never expose these environment variables publicly as they can provide unrestricted access to your project. Use .env files for local development, but ensure they're included in your .gitignore file. For deployment, use secure environment variables provided by your hosting service.
