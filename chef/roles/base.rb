name "base"
description "Base role applied to all nodes."
run_list(
  "recipe[apt]",
  "recipe[zsh]",
  "recipe[sudo]",
  "recipe[git]",
  "recipe[build-essential]",
  "recipe[chef-client::delete_validation]",
  "recipe[runit]",
  "recipe[tmux]",
)
override_attributes(
  :authorization => {
    :sudo => {
      :groups => ["deploy"],
      :passwordless => true
    }
  }
)
