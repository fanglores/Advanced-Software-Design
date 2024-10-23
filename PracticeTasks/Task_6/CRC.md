# Make a list of high priority Use Cases and candidate classes
Prior Use Cases:
- [Containerization](../Task_5/UseCases/8_uc_containerization.puml)
- [Service Deployment](../Task_5/UseCases/9_uc_service_deployment.puml)
- [API Documentation](../Task_5/UseCases/10_uc_documentation.puml)

Prior candidate classes:
- Request Router
- Service Deployer
- Model Containerizer
- OpenAPI Generator

# Apply a CRC role-playing method to elaborate class interactions within the system
Class interactions and responsibilities:  
| Class 		 		| Responsibilities                                              |  
|-----------------------|---------------------------------------------------------------|  
| Request Router 		| - Route incoming requests within K8s (Ingress functionality)  |  
| Service Deployer		| - Deploy model	                                            |  
| Model Containerizer	| - Enwrap model<br>-Containerize model into Docker	            |  
| OpenAPI Generator		| - Provide OpenAPI schema                                      |  


Cooperations table:  
| Use Case | Cooperation | Roles | Classes |
|----------|-------------|-------|---------|
|a|b|c|d|

# CRC Cards
![CRC Card](https://github.com/fanglores/Advanced-Software-Design/blob/master/PracticeTasks/Task_6/res/crc_k8c.png?raw=true)