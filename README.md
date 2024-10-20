!Task 2  

## KEA (Kubernetes Empowerer via API)
<img src="product_img.jpg" alt="Product Image" width="300"/>
<sup> Kea parrot. Picture from: Kea the Clever Clown of the Alps, Milford Sound </sup>

### Self-documenting API gateway
A typical ingress implementation in k8s forwards incoming traffic to a particular application. An improved API Gateway would integrate Single Sign-On, automatic OpenAPI schema generation, request validation and response caching. The goal of the project is to develop such a Kubernetes operator to extend existing ingress implementations to API Gateway. The project should provide means to define API schema using Custom Resource Definitions in K8s directly and generate them from the source code following a set of conventions.

## Team "K8C"
### Team members:
- Dandamaev Gadji
- Smolkin Mikhail
- Tsaturyan Konstantin
- Tsurkan Daniel

### Product description
The product is a platform for deploying, managing, and scaling machine learning models in a production environment. It's primary purpose is to provide a flexible and secure environment for automating ML processes, including model versioning, request routing, and monitoring. The system integrates with Kubernetes, supports model containerization. The product is designed for developers, ML engineers, DevOps teams, and enterprises that require a stable, scalable, and resilient infrastructure for their ML projects.

### Similar systems
- Seldon Core
- KServe
- BentoML

### Stakeholders
- Anton Sergeevich Kheintankov  
- Backend Developers  
- ML Engineers
- DevOps Engineers
- Security Specialists
- API consumers
- Society
  
IT Companies that use Kubernetes, as our clients, e.g.:  
- Sber
- Yandex
- MTS
- Ozon

## Busibess requirements:
### Features
1. Request Routing  
The basic function of K8s Ingress. A reverse proxy directs external traffic to the required specific K8s services.  

2. Load Balancing  
Kubernetes handles it natively using K8s Services, but not via Ingress. Typically configured with weight-based settings.  

3. Audit, Logging  
Extension of basic Nginx logging. Future integration with log storage and rotation tools like ELK Stack, Fluentd. Provides logs about sessions, requests, responses and etc.  

4. SSO, Authorization  
A non-standard Ingress feature, added by Gateway API. It allows API access control using authentication tools like OAuth or JWT. Also stores authorized session keys to provide Single Sing-On.  

5. Request Validation  
A less popular feature that verifies API requests according to the OpenAPI schema. It pairs well with auto-generating schemas.  

6. Response Caching  
Caches responses for particular responses to increase effeciency. Already implemented in a simple form in Nginx.  

7. Modular Deployment of Models  
Supports the deployment of various machine learning (ML) models written in different programming languages and using various frameworks (TensorFlow, PyTorch, Scikit-learn, etc.).  

8. Containerization  
Enables packaging of ML models into containers using Docker. Generates a class with ML functions. Configured using CRD (Custom Resource Definition).  

9. Service Deployment  
Automates the deployment of models from specialized repositories and version control systems into Kubernetes clusters using standard Kubernetes objects (Deployments, Services, Pods).  

10. Model Auto-Documentation  
Generates OpenAPI specifications for models by describing them during deployment from resource fields (CRD) or by reading the source code (class description) of the containerized application.  

### Constrains
- Support Kubernetes versions from 1.20
- OpenAPI scheme of version 3.0.0
- HTTP v1.1
- IPv4 network stack

### Implementation rules
- Kubernetes integration  
- Autonomous components 
- Predefined ML Frameworks (e.g. Tensorflow, Keras, PyTorch, etc.). For custom services API is specified via MLRun library

### Non-functional requirements
- Inner network response timeout: 5s
- Weights for load-balancing are distributed via Round-Robin algorithm in percent values
- Scalability for further system extension
- Usability: any average developer shall be able to use the system
- System should be accessable in 99% time a year
- On failure, system shall self-restored in 5 minutes
- Every function shall provide logs on enter and on exit
