name "django"
description "django application server."
run_list(
  "recipe[django]",
  "recipe[nginx]",
)
default_attributes({
  nginx: {
    init_style: 'runit'
  }
})
