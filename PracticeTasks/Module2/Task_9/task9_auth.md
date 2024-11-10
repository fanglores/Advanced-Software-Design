@startuml

class "<<root>> Authentication Provider" as auth {
  +rbacRules: String[] 
  +cache: SSOToken[]
  +result_t Authenticate(token: String)
}

class "<<resource>> SSO Token" as sso {
  +token: String
  +login_time: DateTime
}

auth "1" <-- "*" sso

@enduml