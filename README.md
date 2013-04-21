# Events

Event aggregate for Penn.

# Development

First create `app/static/coffeescripts/config.coffee` by copying `app/static/coffeescripts/config.coffee.default` and editing as needed.

Next run `foreman start`. This will:

- watch static files for changes and recompile them when any file is updated
- start a mongo database
- start a server

# New Feature

Be able to "follow" specific events without following the creator of those events. As in, adding events to your own feed.
