# Self documenting API Gateway for ML serving in K8S

## Detailed description of the subject area

### Cloud Hosting
Any network application or service must be deployed in some infrastructure before it becomes available to the end user. The implementation of the Gateway API generally refers to the large task and subject area of hosting cloud services.
This task covers a wide range of technologies aimed at providing computing resources, storage and network services on demand over a network (this can be both the Internet and local networks within companies). The key elements of cloud infrastructure are virtualization, process automation, load balancing and high availability. This allows infrastructure developers to dynamically scale their applications and reduce the cost of operating physical servers.
In other words: it will be more profitable to assemble (or rent) a cluster of several servers in some datacenter in terms of time and resources than to allocate a physical server for each business task or service being solved. This is achieved through a set of technologies that allows you to reduce the deployment and hosting of applications to a set of simple abstractions.
Using such a cloud infrastructure allows you to separate the tasks of ensuring the operability of the "hardware" and "software" parts of the servers. It is about the "software" part that we will talk further.

### Kubernetes
One of the central technologies in this area is Kubernetes (abbreviated as K8S), a system for the orchestration of containerized applications. K8S automates the deployment, management and scaling of containers, which makes it easy to manage complex distributed systems. An important aspect of Kubernetes' work is its ability to manage resources in the form of clusters consisting of multiple nodes (virtual or physical machines). Of course, there are many other big technologies and "frameworks" for building cloud infrastructure, the general organization of which is similar, but rather indirectly related to our task.
The K8S system essentially provides a collection of several programs that are controlled using the API. The various mechanisms and components of K8S (e.g. Ingress, Service, Deployment, Pod, Job) are software abstractions, otherwise called "Resources", which have their own instances, states, parameters and configurations. They also allow you to conveniently configure, modify K8S, as well as establish integration with other large infrastructure systems (e.g. AD, Vault, Monitoring, SOC).

### Custome Resource Definition
You can define a resource using CRD, and even write your own handler, called an "Operator", for it. Example:
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myresources.example.com
spec:
group: example.com # API group for CRD
  versions:
    - name: v1 # API version
      served: true # Make the resource available
      storage: true # Use this version for storage
      schema: # Schema definition
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                name:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced # The resource belongs to the namespace (you can use "Cluster" for the cluster level)
  names:
    plural: myresources # Plural of the resource
    singular: myresource # Singular of the resource
    kind: MyResource # Name of the resource type
    shortNames:
      - mr # Short name for the kubectl command
```
After that, it will be possible to create instances of this new resource in Kubernetes by filling in the fields defined in the CRD:
```yaml
apiVersion: example.com/v1
kind: MyResource
metadata:
  name: myresource-sample
spec:
  name: "My Custom Resource"
  replicas: 3
```

### Routing network traffic
One of the key tasks in organizing cloud clusters is routing network traffic. In K8S, this task is solved using built-in [mechanisms](https://kubernetes.io/docs/concepts/services-networking), such as Ingress controllers and services that provide routing of external requests to the necessary containers within the cluster. Proper routing and balancing of traffic is vital to ensure high performance and availability of cloud applications. This also includes tasks such as:
* Load balancing between different application instances for optimal distribution of requests. This task is solved by resources, the same Ingress, LoadBalancer, Service.
* Traffic management to manage routing based on rules and policies, such as filtering requests, checking service availability, and restricting access. In the context of this task, in particular, SSO and caching are used. This task is solved using resources like Ingress, NetworkPolicy. Software deployed directly inside the cluster is also used: Redis/Firefly, External-Auth-Server.
* Ensuring network security through the use of traffic encryption and management of interservice communications. And again Ingress, NetworkPolicy.

K8S Ingress is the most basic resource for routing traffic from outside the cluster to K8S services inside it. This resource is based on the basic nginx image and allows you to solve a simple task: to link a certain path to a certain service. Performs as L4 (TCP/UDP) so is L7 (HTTP) routing.
It is easy to see that there are a lot of tasks to be solved for traffic routing, but they are all extremely standard. Therefore, for K8S, there are many solutions developed by third parties to solve these tasks, one of which is the Gateway API - a large resource of K8S, designed not to replace, but very qualitatively complement the standard set of network resources of the system. Each [implementation](https://gateway-api.sigs.k8s.io/implementations /) has its pros and cons, a set of functions, parameters and configurations. Therefore, the desired implementation of the Gateway API is chosen based on the task that the Kubernetes cluster solves: a simple site, a service with a complex API, a file exchanger, a streaming service, etc.

### ML-Serving
As it turned out, the Self Documenting API Gateway will be used to solve the problem of servicing machine learning models.
The task of serving machine learning models (ML serving) is to provide a ready-made trained model (for example, a Python class assembled into a binary file) for processing requests in real time or batch mode. This is the final stage of the ML pipeline, where the model is integrated into an application to solve business problems.
This is a critical stage where the trained model is deployed in a production environment and begins to accept requests from external systems to generate predictions. The main tasks of this layer are:
* API integration: The model is wrapped in an interface that allows external systems to send requests and receive predictions. This interface can be:
* Python-an application that provides an API (FastAPI, Flask) and a library (Torch, TensorFlow, LLM) for working with the model. This method is the most difficult to implement, but retains all the functions for the work of model development (e.g. additional training, data filtering).
  * An application that provides API and ML model serving tools (MLRun). This method is simpler and in addition allows you to work with a wide range of models, including from other languages, but lacks some functions for model development.
  * External ML-model serving tool (KServe, Seldon Core, BentoML). Such tools have extensive integration with cloud tools (e.g. the same K8S Gateway API, or repositories for storing and versioning models) and allow you to speed up the deployment of models. Most often, they assume only the launch of models, trying to comply with the principle of "Do one thing and do it right", offering an API for other services that can combine its calls with other functions.
* Scalability: Models must effectively handle both single requests and high traffic volumes, for which automatic scaling tools are used.
* Low latency: It is important to minimize the response time of the model in order to ensure fast processing of requests in real time.
* Model updates: Regular replacement of outdated models with new versions without interrupting the system.

Based on the two previous paragraphs, ML-serving is almost a reference task for implementation in Kubernetes. And the API Gateway, together with the mentioned standard tools, would help provide access to the API of ML models and services that use them.
The described Kubernetes-based approach allows you to implement a cloud with a wide range of functions and API calls, and a gram-based ML-Ops team will speed up the development processes of the models themselves, as well as ML services. But for internal and external users of the ML services API, its description is required in order to switch to new versions in a timely manner.

### OpenAPI
OpenAPI is a specification that allows you to describe the RESTful API in a machine—readable format. It standardizes the way APIs are presented, providing API developers and users with a unified way to document, interact, and generate code for client and server applications.
The main aspects of OpenAPI:
1. API Description format: OpenAPI provides a specification in YAML or JSON format that describes the API structure: available endpoints, HTTP methods (GET, POST, PUT, DELETE, etc.), types of requests and responses, parameters, headers and response codes. This allows you to create a standardized and detailed description of the API interfaces.
2. Machine-readable: Since OpenAPI is presented as a data structure, developers can easily automate the generation of client and server code, tests, documentation, and API validation tools. For example, you can use tools to generate client libraries in different programming languages.
3. Documentation: One of the key goals of OpenAPI is to simplify API documentation. The API description includes not only information about available resources, but also examples of requests and responses, which makes the documentation understandable for both developers and users.
4. Interactive testing: With OpenAPI, you can automatically create interfaces for interactive API testing. Tools like Swagger UI or ReDoc allow users to send API requests and see the results directly in the browser. This helps you quickly understand how the API works and test its functionality without writing code.

There are several key sections in the OpenAPI specification:
1. Info: Contains general information about the API, such as name, description, version, and contact information.
2. Paths: Describes all available API routes (endpoints) and associated HTTP methods (e.g. GET/users, POST/users/{id}).
3. Components: Contains reusable components such as data schemas, request/response type definitions, parameters, and error codes.
4. Security: Describes authorization mechanisms such as OAuth2, JWT, API keys, etc.
5. Servers: Describes the basic URLs for accessing the API.
6. Tags: Used to group and organize API methods.
Example:
```yaml
openapi: 3.0.0
info:
title: Simple API
  description: A simple API to demonstrate OpenAPI
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: A list of users
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
```
The OpenAPI schema is often provided via a special API endpoint URL (/openapi.json or /swagger.json). This endpoint usually returns an OpenAPI schema in JSON format. It can be linked to a version (/v1/openapi.json).
Many API developers implement interactive documentation, such as Swagger UI or ReDoc, where users can interact with the API and view the OpenAPI schema. For example, on the API documentation page (e.g. https://api.example.com/docs ) Swagger UI can be embedded. The user can see not only the API description, but also download the schema using the Swagger UI (in the "Export" or "Download" section).
Specialized API management platforms such as Kong, Apigee, AWS API Gateway, or Azure API Management allow you to automate the publication of an OpenAPI schema. These services can automatically generate and provide a schema through user-friendly interfaces or integrations.