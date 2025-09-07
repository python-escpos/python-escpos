# Flask and Python-ESC/POS example

Simple example on how to use it inside a web service

```sh
docker build . -t escpos-web
docker run --network=host -p 9999:9999 escpos-web
```
