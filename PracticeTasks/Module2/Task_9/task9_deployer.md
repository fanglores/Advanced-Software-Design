@startuml

class "<<resource>> ReplicaSet" as ReplicaSet {
  +id: string
  +replicas: uint
  +dockerImage: string
}

class "<<root>> Service Deployer" as deployer {
  +replica: ReplicaSet
  +result_t Deploy()
}

ReplicaSet "*" -up- "1" deployer

@enduml