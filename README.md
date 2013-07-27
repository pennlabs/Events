# Events

Event aggregate for Penn.

# Requirements

Install [MongoDB](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/).

Install CoffeeScript.

```
sudo npm install -g coffee-script
```

Install Sass.

```
gem install sass
```

Install Python requirements:

```
pip install -r requirements.txt
```

# Setup

Create `app/static/coffeescripts/config.coffee` by copying `app/static/coffeescripts/config.coffee.default` and edit as needed.

# Usage

To run, use `foreman start`. This will:

- Monitor static files and recompile updated files.
- Start a mongo database.
- Start a server.
