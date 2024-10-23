# Use cases

## 1. Request Routing  
* Actors:  
   * API Consumer
* Preconditions:
   * API endpoint is defined.
   * Kubernetes services are running.
* Main Success Scenario:
   1. API Consumer sends a request to the API Gateway.
   2. The API Gateway forwards the request to the appropriate Kubernetes service.
   3. The Kubernetes service processes the request and returns the response to the API Gateway.
   4. The API Gateway sends the response back to the API Consumer.
* Postconditions:
   * The request is routed correctly, and a response is delivered to the API Consumer.
* Failure Conditions:
   * Target service not found.
   * Network issues.
* Diagram:
![UC Request Routing](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/1_uc_request_routing.puml)

## 2. Load Balancing  
* Actors:  
	* API Consumer
	* DevOps Engineer
	* ML Engineer
* Preconditions:
	* Multiple instances of a service are running in the Kubernetes cluster.
	* Load balancing rules are configured (e.g., Round-Robin).
* Main Success Scenario:
	1. API Consumer sends a request to the API Gateway.
	2. The API Gateway distributes the request across available service instances using the predefined load balancing algorithm (e.g., Round-Robin).
	3. The selected Kubernetes service instance processes the request.
	4. The service sends the response back to the API Gateway.
	5. The API Gateway returns the response to the API Consumer.
* Postconditions:
	* Requests are balanced across multiple service instances, and responses are successfully delivered to the API Consumer.
* Failure Conditions:
	* No healthy service instances are available.
	* Misconfiguration in load balancing rules.
* Diagram:
![UC Load Balancing](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/2_uc_load_balancing.puml)

## 3. Audit and Logging  
* Actors:  
	* Security Specialist
	* DevOps Engineer
* Preconditions:
	* The API Gateway is configured to log incoming requests and outgoing responses.
* Main Success Scenario:
	1. A request enters the API Gateway.
	2. The API Gateway logs relevant information, such as request details, response time, and any errors.
	3. Logs are collected and pushed to an external system (e.g., ELK stack) for further analysis by Security Specialists and DevOps Engineers.
* Postconditions:
	* Logs are securely stored and available for audit and monitoring purposes.
* Failure Conditions:
	* The logging system is not accessible.
	* Log data is corrupted or incomplete.
* Diagram:
![UC Audit and Logging](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/3_uc_logging.puml)

## 4. SSO (Single Sign-On) and Authorization
* Actors:
    * API Consumer
    * Security Specialist
* Preconditions:
    * The SSO system is integrated with the API Gateway.
    * User credentials and authorization tokens (e.g., JWT, OAuth) are stored.
* Main Success Scenario:
    1. API Consumer sends a request to access a protected resource.
    2. The API Gateway checks the authorization token (JWT/OAuth) associated with the request.
    3. If the token is valid, the gateway forwards the authorized request to the appropriate service.
    4. If the token is invalid or expired, the user is redirected to the SSO login page.
    5. Upon successful login, the session is stored for future requests.
* Postconditions:
    * The user is authenticated and authorized, and the session is maintained for subsequent requests.
* Failure Conditions:
    * The authorization token has expired or is invalid.
    * Unauthorized access is attempted without a valid session or token.
* Diagram:
![UC Authorization](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/4_uc_auth.puml)

## 5. Request Validation
* Actors:
    * API Consumer
    * DevOps Engineer
* Preconditions:
    * An OpenAPI schema is generated and integrated with the API Gateway for request validation.
* Main Success Scenario:
    1. API Consumer sends a request to the API Gateway.
    2. The API Gateway validates the request against the OpenAPI schema.
    3. If the request conforms to the schema, it is forwarded to the appropriate Kubernetes service.
    4. If the request is invalid, the API Gateway returns an error response to the API Consumer.
* Postconditions:
    * Only valid requests are forwarded to the services in the Kubernetes cluster.
* Failure Conditions:
    * The request does not conform to the OpenAPI schema, and an error response is generated.
* Diagram:
![UC Request Validation](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/5_uc_request_validation.puml)

## 6. Response Caching
* Actors:
    * API Consumer
    * DevOps Engineer
* Preconditions:
    * Caching is enabled for specific responses in the API Gateway.
* Main Success Scenario:
    1. API Consumer sends a request to the API Gateway.
    2. The API Gateway checks if a cached response for the request is available.
    3. If the response is cached, the gateway serves the cached response to the API Consumer.
    4. If the response is not cached, the request is processed by the Kubernetes service, and the response is cached for future requests.
* Postconditions:
    * Response time is reduced for future requests that hit the cache.
* Failure Conditions:
    * Cache miss (no cached data available for the request).
    * Cached data is outdated or invalid.
* Diagram:
![UC Response Caching](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/6_uc_response_caching.puml)

## 7. Modular Deployment of Models
* Actors:
    * ML Engineer
    * DevOps Engineer
* Preconditions:
    * ML models are containerized and available in the repository for deployment.
* Main Success Scenario:
    1. The ML Engineer uploads a model to the repository.
    2. The API Gateway orchestrates the deployment of the model into the Kubernetes cluster.
    3. An instance of the model is created and deployed in a Kubernetes pod, making it available for incoming requests.
* Postconditions:
    * The ML model is successfully deployed and accessible via the API Gateway.
* Failure Conditions:
    * The model is not properly containerized.
    * Deployment failure due to incorrect configuration or resource constraints.
* Diagram:
![UC Modular Deployment of Models](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/7_uc_deployment.puml)

## 8. Containerization
* Actors:
    * ML Engineer
    * DevOps Engineer
* Preconditions:
    * The model code is ready for deployment and has been pushed to the repository.
* Main Success Scenario:
    1. The ML Engineer pushes the model to the repository.
    2. The API Gateway triggers the containerization process using Docker.
    3. The model is packaged into a Docker container.
    4. The container is deployed into the Kubernetes cluster, making the model available for requests.
* Postconditions:
    * The model is successfully containerized and running as a container in the Kubernetes cluster.
* Failure Conditions:
    * Containerization fails due to code errors or missing dependencies.
* Diagram:
![UC Containerization](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/8_uc_containerization.puml)

## 9. Service Deployment
* Actors:
    * ML Engineer
    * DevOps Engineer
* Preconditions:
    * A specific version of the model is ready for deployment.
    * The Custom Resource Definition (CRD) is configured for the deployment process.
* Main Success Scenario:
    1. The ML Engineer selects a version of the model from the repository.
    2. The API Gateway automates the deployment process by creating the necessary Kubernetes services, deployments, and pods.
    3. The model is containerized and deployed into the Kubernetes cluster.
    4. Kubernetes services and endpoints are created automatically to make the model accessible.
* Postconditions:
    * The model is successfully deployed and available through an endpoint in the Kubernetes cluster.
* Failure Conditions:
    * Deployment failure due to incorrect configuration, resource constraints, or containerization issues.
* Diagram:
![UC Service Deployment](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/9_uc_service_deployment.puml)

## 10. Model Auto-Documentation
* Actors:
    * API Consumer
    * ML Engineer
* Preconditions:
    * The OpenAPI schema generation is configured in the API Gateway.
* Main Success Scenario:
    1. The ML Engineer deploys a model via the API Gateway.
    2. The API Gateway reads the model’s source code or its Custom Resource Definition (CRD).
    3. The API Gateway automatically generates an OpenAPI specification for the deployed model.
    4. API documentation is generated and made accessible for API consumers to view and interact with the model.
* Postconditions:
    * API consumers can access and view the automatically generated documentation to interact with the model via the API.
* Failure Conditions:
    * The schema generation process fails.
    * The generated documentation is not accessible or incomplete.
* Diagram:
![UC Model Auto-Documentation](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/fanglores/Advanced-Software-Design/refs/heads/master/General/UseCases/puml/10_uc_documentation.puml)
