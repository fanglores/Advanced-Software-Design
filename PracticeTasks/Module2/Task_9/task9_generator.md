@startuml

class "<<root>> OpenAPI Generator" as generator {
  +id: String
  +schema: OpenApiSchema
  +crd: CRD
  +sourceCode: SourceCode
  +result_t CreateSchema()
}

class "<<resource>> OpenAPI Schema cached" as apischema {
  +id: string
}

class "<<resource>> CRD" as crd {
  +data: string
}

class "<<resource>> SourceCode" as sourceCode {
  +code: string
}

apischema "1" -up- "1" generator
crd "1" -up- "1" generator
sourceCode "1" -up- "1" generator

@enduml