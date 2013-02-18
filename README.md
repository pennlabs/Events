# Events

Event aggregate for Penn.

# Setup

The quickest way to get started is just `fab run`. This will run a few commands to automatically recompile static files on change, start a mongo database, and start the server.

Behind the scenes, this is what is being executed:

```
coffee -cw app/static/scripts &
sass -w app/static/stylesheets &
mongod &
python run.py &
```
