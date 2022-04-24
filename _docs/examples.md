# Examples

## Generating an example Certificate

```shell
# Create both the private key and CSR with a single command
$ openssl req -newkey rsa:2048 -nodes -keyout domain.key -out domain.csr

# Create a self-signed certificate (domain.crt) valid for 30 days with our existing private key and CSR
$ openssl x509 -signkey domain.key -in domain.csr -req -days 30 -out domain.crt

# View the contents of our certificate in plain text
$ openssl x509 -text -noout -in domain.crt
```

You can upload `domain.crt` to your app registration / service principal

See

- [Creating a Self-Signed Certificate With OpenSSL](https://www.baeldung.com/openssl-self-signed-cert)
- [Create a self-signed public certificate to authenticate your application](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-self-signed-certificate)
