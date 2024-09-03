## Team "K8C"
### Team members:
- Dandamaev Gadji
- Smolkin Mikhail
- Tsaturyan Konstantin
- Tsurkan Daniel

## Product requirements:
#### Self-documenting API gateway
A typical ingress implementation in k8s forwards incoming traffic to a particular application. An improved API Gateway would integrate Single Sign-On, automatic OpenAPI schema generation, request validation and response caching. The goal of the project is to develop such a Kubernetes operator to extend existing ingress implementations to API Gateway. The project should provide means to define API schema using Custom Resource Definitions in K8s directly and generate them from the source code following a set of conventions.

#### Stakeholders
- Anton Sergeevich Kheintankov
- Kaspersky Lab
- Yandex

#### Features
- Ingress reverse proxy
- Traffic logging
- Load balancing
- Single Sing-On
- OpenAPI scheme generation
- Request Validation
- Response Caching

#### Constrains/Implementation rules/Non-functional requirements
- Custom Resource Definition (with yaml configuration)
- HTTP IPv4 network stack
- Session ticket usage
- Response timeout: 5s
- Cache expiration time: 2h
- Session expiration: 8h 
