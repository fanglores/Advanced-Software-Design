# Make a list of high priority Use Cases and candidate classes
1.1 Prior Use Cases:
- [Containerization](../Task_5/UseCases/8_uc_containerization.puml)
- [Service Deployment](../Task_5/UseCases/9_uc_service_deployment.puml)
- [API Documentation](../Task_5/UseCases/10_uc_documentation.puml)

1.2 Prior candidate classes:
- Request Router
- Service Deployer
- Model Containerizer
- OpenAPI Generator

# Apply a CRC role-playing method to elaborate class interactions within the system
2. Class interactions and responsibilities:  
| Class 		 		| Responsibilities                                              |  
|-----------------------|---------------------------------------------------------------|  
| Request Router 		| - Route incoming requests within K8s (Ingress functionality)  |  
| Service Deployer		| - Deploy model	                                            |  
| Model Containerizer	| - Enwrap model<br>-Containerize model into Docker	            |  
| OpenAPI Generator		| - Provide OpenAPI schema                                      |  


3. Cooperations table:  
| **Use Case**                   | **Cooperation Name**    | **Used Roles**                                  | **Candidate Classes**                         |
|--------------------------------|-------------------------|-------------------------------------------------|-----------------------------------------------|
| Forward Request                | Route Request           | Router, Request, Receiver                       | Request Router, Request, K8s                  |
| Load Balancing                 | Distribute Load         | Load balancer, weights, ML sevices              | Load Balancer, K8s, Pod, ML Service           |
| Authenticate                   | Validate Authentication | Request, Authenticator, SSO Keys                | Authentication Provider, SSO Key, Request     |
| Cache Response                 | Cache Responses         | Request, Response, Cache, Cache validator       | Response Cacher, Cache, Request, Response     |
| Collect Logs                   | Log System Events       | Logger, Log, ML service, API Gateway            | System Logger, Log, ML Service, API Gateway   |
| Deploy Model                   | Deploy Service          | Deployer, K8s, Pod, ML service                  | Service Deployer, Pod, K8s, ML Service        |
| Publish Model                  | Containerize Model      | Containerizer, Pod, K8s, ML model               | Model Containerizer, Pod, K8s, ML Service     |
| OpenAPI Schema Generation      | Generate API Definition | ML service, OpenAPI schema, Generator           | OpenAPI Generator, OpenAPI Schema, ML Service |

# CRC Cards
![CRC Card](https://github.com/fanglores/Advanced-Software-Design/blob/master/PracticeTasks/Task_6/res/crc_k8c.png?raw=true)