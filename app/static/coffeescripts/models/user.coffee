define [], ->
  class User extends Backbone.Model
    idAttribute: "_id"
    defaults:
      email: 'yefim323@gmail.com'
      first_name: 'Geoffrey'
      last_name: 'Vedernikoff'
      logged_in: false
      events: []

    logout: ->
      @url = 'logout'
      @save(logged_in: false)

  class Users extends Backbone.Collection
    model: Users
    url: '/api/users'

  return {model: User, collection: Users}
