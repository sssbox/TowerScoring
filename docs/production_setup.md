# Overview.

You will need a good computer that will plug into
* IR auto counters
* Wired to Network which is connected (wired or wireless) to
 * 4 scoring devices
 * scoring display computer(s)
* Sound system

# Additional requirements over dev:

## Celery

### Setting up the broker (RabbitMQ)

```bash
sudo apt-get install rabbitmq-server
```

Add the following to `/etc/rabbitmq/rabbitmq-env.conf`:

```bash
export RABBITMQ_NODENAME=rabbit@localhost
export RABBITMQ_NODE_IP_ADDRESS=127.0.0.1
export ERL_EPMD_ADDRESS=127.0.0.1
```

Restart rabbitmq or maybe even the computer (rabbitmq is a pain to set up, I'm still not 100% sure how to do it)

```bash
sudo rabbitmqctl add_user scoring ancoiaoncuhncaoe
sudo rabbitmqctl add_vhost scoring
sudo rabbitmqctl set_permissions -p scoring scoring ".*" ".*" ".*"
```

### Run celery (you should probably actually install it for real in daemon mode, though you could also just do this  in a few terminals... (min 2 workers, probably want 3))

```bash
python manage.py celery worker --loglevel=INFO
```

(Daemon mode: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#daemonizing)

## mplayer

You need mplayer to play match sounds

```bash
sudo apt-get install mplayer
```

