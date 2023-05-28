Simple example on how to use it inside a web service

```
docker build . -t escpos-web
docker run --network=host -p 9999:9999 escpos
```