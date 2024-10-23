# Use cases

## 1. Request Routing
* Actors:
    * API consumer
* Preconditions: API endpoint is defined, and K8s services are running.
* Main Success Scenario:
    1.	API consumer sends a request to the gateway.
    2.	The reverse proxy identifies the target service in the Kubernetes cluster.
    3.	The proxy forwards the request to the appropriate K8s service.
    4.	The service processes the request and sends a response back to the gateway.
    5.	The gateway returns the response to the API consumer.
* Postconditions: The request is routed correctly, and a response is delivered.
* Failure Conditions: Target service not found, network issues.
* Diagram:
![UC Request Routing](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/1_uc_request_routing.puml)

## 2. Load Balancing
* Actors:
    * API consumer
* Preconditions: Multiple instances of a service are running in the cluster.
* Main Success Scenario:
    1. API consumer sends a request.
    2. The gateway distributes the request across available service instances based on predefined weight (Round-Robin).
    3. The selected instance processes the request and sends the response.
    4. The response is delivered to the API consumer.
* Postconditions: Requests are balanced across services, responses are received.
* Failure Conditions: No healthy instances available, misconfiguration in load balancing rules.
* Diagram:
![UC Load Balancing](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/2_uc_load_balancing.puml)

## 3. Audit and Logging
* Actors: Security Specialists, DevOps Engineers
* Preconditions: Gateway is configured to log requests/responses.
* Main Success Scenario:
    1. A request enters the system.
    2. The gateway logs relevant information (e.g., request details, response time, errors).
    3. Logs are pushed to an external system (e.g., ELK stack) for further analysis.
* Postconditions: Logs are stored securely for audit purposes.
* Failure Conditions: Logging system not accessible, log data corrupted.
* Diagram:
![UC Audit and Logging](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/3_uc_logging.puml)

## 4. SSO (Single Sign-On) and Authorization
* Actors: API consumers, Security Specialists
* Preconditions: SSO system is integrated with the gateway, user credentials are stored.
* Main Success Scenario:
    1. API consumer attempts to access a protected resource.
    2. The gateway checks the authorization token (JWT/OAuth).
    3. If valid, the request is processed and forwarded.
    4. If invalid, the user is redirected to the SSO login page.
    5. Upon successful login, the session is stored for future requests.
* Postconditions: User is authenticated and authorized, session maintained.
* Failure Conditions: Token expired, unauthorized access.
* Diagram:
![UC Authorization](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/4_uc_auth.puml)

## 5. Request Validation
* Actors: API consumers, DevOps Engineers
* Preconditions: OpenAPI schema is generated and integrated.
* Main Success Scenario:
    1. API consumer sends a request.
    2. The gateway validates the request against the OpenAPI schema.
    3. If valid, the request is forwarded to the service.
    4. If invalid, the gateway returns an error response.
* Postconditions: Only valid requests reach the services.
* Failure Conditions: Request does not conform to the schema.
* Diagram:
![UC Request Validation](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/5_uc_request_validation.puml)

## 6. Response Caching
* Actors: API consumers, DevOps Engineers
* Preconditions: Caching is enabled for certain responses.
* Main Success Scenario:
    1. API consumer sends a request.
    2. The gateway checks if the response is cached.
    3. If cached, the gateway serves the cached response.
    4. If not cached, the request is processed, and the response is cached for future requests.
* Postconditions: Response time is reduced for cached requests.
* Failure Conditions: Cache miss, outdated cached data.
* Diagram:
![UC Response Caching](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/6_uc_response_caching.puml)

## 7. Modular Deployment of Models
* Actors: ML Engineers, DevOps Engineers
* Preconditions: ML models are containerized and available in the repository.
* Main Success Scenario:
    1. ML engineer uploads a model to the repository.
    2. The gateway orchestrates the deployment of the model into the K8s cluster.
    3. The model is containerized and available for requests.
* Postconditions: The model is deployed and accessible.
* Failure Conditions: Model not properly containerized, deployment failure.
* Diagram:
![UC Modular Deployment of Models](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/7_uc_deployment.puml)

## 8. Containerization
* Actors: ML Engineers, DevOps Engineers
* Preconditions: Model code is ready for deployment.
* Main Success Scenario:
    1. ML engineer pushes the model to the repository.
    2. The gateway triggers the containerization process using Docker.
    3. The model is packaged into a Docker container and deployed.
* Postconditions: Model is successfully containerized and running in the K8s cluster.
* Failure Conditions: Containerization fails due to code errors or missing dependencies.
* Diagram:
![UC Containerization](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/8_uc_containerization.puml)

## 9. Service Deployment
* Actors: ML Engineers, DevOps Engineers
* Preconditions: Model version is ready, CRD is configured.
* Main Success Scenario:
    1. ML engineer selects a model version from the repository.
    2. The gateway automates the deployment into the cluster.
    3. Kubernetes services, deployments, and pods are created automatically.
* Postconditions: The model is deployed and available through an endpoint.
* Failure Conditions: Deployment fails due to configuration issues or resource limits.
* Diagram:
![UC Service Deployment](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/9_uc_service_deployment.puml)

## 10. Model Auto-Documentation
* Actors: API consumers, ML Engineers
* Preconditions: OpenAPI schema generation is configured.
* Main Success Scenario:
    1. ML engineer deploys the model via the gateway.
    2. The gateway reads the model’s source code or CRD.
    3. An OpenAPI specification is auto-generated for the model.
    4. The API documentation is available for API consumers.
* Postconditions: API consumers can view documentation to interact with the model.
* Failure Conditions: Schema generation fails, documentation not accessible.
* Diagram:
![UC Model Auto-Documentation](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/10_uc_documentation.puml)