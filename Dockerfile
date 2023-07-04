FROM golang:1-alpine as builder

RUN apk add --no-cache git 

RUN go install github.com/korylprince/fileenv@v1.1.0

RUN git clone --branch "security-fix" --single-branch --depth 1 \
    --recurse-submodules --shallow-submodules \
    https://github.com/korylprince/web2py.git /web2py

RUN rm -rf /web2py/applications/examples /web2py/applications/welcome

FROM alpine:3.9

RUN apk add --no-cache python2 py2-pyldap

COPY --from=builder /web2py /web2py

COPY . /web2py/applications/inventory

# set base URL parameters
RUN echo 'routers = {"BASE": {"default_application": "inventory", "default_controller": "default"}}' > /web2py/routes.py

WORKDIR /web2py

# web2py compile app
RUN python -c 'import gluon.compileapp; gluon.compileapp.compile_application("applications/inventory")'

COPY --from=builder /go/bin/fileenv /

CMD /fileenv python web2py.py --ip=0.0.0.0 --port=8080 --password="$(cat $WEB2PY_ADMIN_PASS_FILE)"
