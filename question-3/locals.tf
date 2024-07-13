locals {
  resources_github = merge([
    for resource_file in fileset(path.cwd, "matrix.yaml") : {
      for k, v in yamldecode(file(resource_file)) : v.name => v
    }
  ]...)
  # resources_users = distinct(flatten([
  #   for team in yamldecode(file("${path.cwd}/matrix.yaml")) :
  #   team.member
  # ]))
  resources_users = distinct(flatten([
    for team in yamldecode(file("${path.cwd}/matrix.yaml")) : concat(try(team.member, []), try(team.maintainer, []))
  ]))

  team_members = flatten([
    for team in local.resources_github : [
      for member in try(team.member, []) : "${team.name}:${member}"
    ]
  ])
  team_maintainers = flatten([
    for team in local.resources_github : [
      for member in try(team.maintainer, []) : "${team.name}:${member}"
    ]
  ])
}