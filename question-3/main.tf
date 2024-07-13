resource "github_membership" "this" {
  for_each = { for user in local.resources_users : user => user }
  username = each.key
  role     = "member"
}

resource "github_team" "this" {
  for_each    = local.resources_github
  name        = each.value.name
  description = "team ${each.key}"
  privacy     = "closed"
}
resource "github_team_membership" "member" {
  for_each = toset(local.team_members)
  team_id  = github_team.this[split(":", each.value)[0]].id
  username = split(":", each.value)[1]
  role     = "member"
}
resource "github_team_membership" "maintainer" {
  for_each = toset(local.team_maintainers)
  team_id  = github_team.this[split(":", each.value)[0]].id
  username = split(":", each.value)[1]
  role     = "maintainer"
}