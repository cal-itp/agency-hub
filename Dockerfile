# build client
FROM node:16.15-alpine3.15 AS client

WORKDIR /client
COPY client/package.json client/yarn.lock ./
RUN yarn install --frozen-lockfile

COPY client/ ./
RUN yarn run build

# build server
FROM python:3.10 AS server

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./

ENTRYPOINT [ "/server/entrypoint.sh" ]

# build composite
FROM server AS composite

COPY --from=client /client/dist /server/static
