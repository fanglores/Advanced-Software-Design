@startuml

class "<<root>> Request Validator" as validator {
  +schema: OpenApiSchema
  +result_t Validate(request: Request)
}

class "<<resource>> OpenAPI Schema cached" as apischema {
  +id: String
}

class "<<entity>> Request" as request {
  +data: String
}

validator "1" -- "1" apischema
validator "1" -- "1" request

@enduml