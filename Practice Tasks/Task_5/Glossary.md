|    Definition 	|  Description  |
APIConsumer			| Represents the user interacting with the API.
Gateway     		| Manages routing, load balancing, and other features.
Service				| Target Kubernetes service that processes requests.
Request				| Data sent from the APIConsumer to the Gateway.
Response			| Data returned from the Service through the Gateway.
OpenAPISchema 		| Schema used for validating API requests.
Cache				| Stores cached responses for quick retrieval.
SSO System			| Manages Single Sign-On for APIConsumers.
AuthorizationToken 	| Token used for authenticating APIConsumers.
Logs				| Stores request and response logs for auditing.
Model				| Machine learning models containerized and deployed.
DockerContainer     | Represents the containerized format of the model.
K8sCluster			| Kubernetes environment where models are deployed.
ELK Stack			| External system used to store logs.
Repository			| Storage for containerized models.
ML Engineer			| Actor responsible for deploying models.
DevOps Engineer		| Actor responsible for managing infrastructure and logs.