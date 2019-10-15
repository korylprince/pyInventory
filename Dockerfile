FROM golang:1.13-alpine as builder

RUN apk add --no-cache git 

RUN git clone --branch "v1.1" --single-branch --depth 1 \
    https://github.com/korylprince/fileenv.git /go/src/github.com/korylprince/fileenv

RUN go install github.com/korylprince/fileenv


FROM alpine:3.9

ARG VERSION

RUN apk add --no-cache python2 py2-pyldap git

RUN git clone --branch "R-2.17.1" --single-branch --depth 1 \
    https://github.com/web2py/web2py.git /web2py

RUN git clone --branch "v19.04" --single-branch --depth 1 \
    https://github.com/web2py/pydal.git /web2py/gluon/packages/dal

RUN git clone --branch "$VERSION" --single-branch --depth 1 \
    https://github.com/korylprince/pyInventory.git /web2py/applications/inventory

RUN rm -rf /web2py/applications/examples /web2py/applications/welcome

# set base URL parameters
RUN echo 'routers = {"BASE": {"default_application": "inventory", "default_controller": "default"}}' > /web2py/routes.py

WORKDIR /web2py

# web2py compile app
RUN python -c 'import gluon.compileapp; gluon.compileapp.compile_application("applications/inventory")'

COPY --from=builder /go/bin/fileenv /

CMD /fileenv python web2py.py --ip=0.0.0.0 --port=8080 --password="$(cat $WEB2PY_ADMIN_PASS_FILE)"
