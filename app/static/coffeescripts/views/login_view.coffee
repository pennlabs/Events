define ['static/javascripts/vendor/text!static/templates/login_template.html'],
  (template) ->
    class LoginView extends Backbone.View
      events:
        'click #register-button' : 'register'
        'click #login-button'    : 'login'
      submit_form: ($form, success) ->
        $.ajax(
          url: $form.attr 'action'
          method: $form.attr 'method'
          data: $form.serialize()
        ).done success
      register: (e) ->
        e.preventDefault()
        $register = $('#register-form')
        @submit_form $register, (data) =>
          # fix this on the server side
          data = $.parseJSON data
          if data._id
            @model.set data
            window.router.navigate '', {trigger: true}
      login: (e) ->
        e.preventDefault()
        $login = $('#login-form')
        @submit_form $login, (data) =>
          # fix this on the server side
          data = $.parseJSON data
          if data._id
            @model.set data
            window.router.navigate '', {trigger: true}
      render: ->
        @$el.html template
        return @
        # render all sub-views

    return {view: LoginView}
