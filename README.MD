orpheus
------------------
Service for searching GitHub and GitLag repositories
------------------
Links
------------------

### Before start

Need to create yaml file with config

```yaml
version: String,
debug: true, # for dev use
celery_broker_url: redis://redis:6379/12 # for dev use 
loglevel: String, #  INFO  
elastic_url: http://elastic:password@elasticsearch:9200  # for dev use 
gitlab_token: '', # String
storage_name: storage,
server_host: 0.0.0.0,  # for dev use 
server_port: 8888, # for dev use 
api_server_origins: [ "http://localhost:3000", "http://0.0.0.0:3000", ]  # for dev use 
repositories_url: List(String)
```

### Running

Elastic search

```shell
$ lets es
```

Redis

```shell
$ lets redis
```

Static

```shell
$ lets static-server
```

Api server

```shell
$ lets server  --config=<config> Set config yaml file
```

Celery beat

```shell
$ lets beat  --config=<config> Set config yaml file
```

Celery worker

```shell
$ lets worker  --config=<config> Set config yaml file
```

Build frontend

```shell
$ npm run build
```

### Todo list

- [] Create bulk in elastic
- [] Create upsert in elastic

### if elastic dont work

```shell
$ docker-compose down -v  
$ docker volume prune -f
$ sudo rm -f esdata
$ mkdir esdata
$ sudo chmod 777 esdata
```






