define [], ->
  class User extends Backbone.Model
    defaults:
      email: 'yefim323@gmail.com'
      first_name: 'Geoffrey'
      last_name: 'Vedernikoff'
      logged_in: false

  return {model: User}
