name "django"
description "django application server."
run_list(
  "recipe[django]",
  "recipe[nginx]",
)
override_attributes(
  :nginx => {
    :init_style => 'runit'
  }
)
