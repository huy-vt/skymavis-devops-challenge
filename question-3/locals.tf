locals {
  resources_github = merge([
    for resource_file in fileset(path.cwd, "matrix.yaml") : {
      for k, v in yamldecode(file(resource_file)) : v.name => v
    }
  ]...)
  resources_users = distinct(flatten([
    for team in yamldecode(file("${path.cwd}/matrix.yaml")) :
    team.member
  ]))
  team_members = flatten([
    for team in local.resources_github : [
      for member in team.member : "${team.name}:${member}"
    ]
  ])
  team_maintainers = flatten([
    for team in local.resources_github : [
      for member in team.maintainer : "${team.name}:${member}"
    ]
  ])
}