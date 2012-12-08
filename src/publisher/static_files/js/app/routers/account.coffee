class publisher.routers.Account extends Backbone.Router
  routes:
    'account': "account"

  account: ->
    view = new publisher.forms.AccountForm(model: @page)
    $('.profile.edit').html view.render()
