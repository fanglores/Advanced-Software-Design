import kopf
import kubernetes
import os
import time
import base64
import yaml
from kubernetes.client import (BatchV1Api, AppsV1Api, CoreV1Api, NetworkingV1Api)
from kubernetes.client.rest import ApiException

# ---------------------------------------------------------------------
# Hard-coded tokens and registry info (DEMO ONLY)
# In real setups, store in Secrets.
# ---------------------------------------------------------------------
YANDEX_OBJECT_STORAGE_TOKEN = "dummy-object-storage-token"
YANDEX_REGISTRY_TOKEN = "dummy-registry-token"
YANDEX_REGISTRY = "cr.yandex/YOUR_YANDEX_REGISTRY_NAME"
NAMESPACE = "kea-project"

# Dockerfile path in some accessible location
# Possibly you'd store your Dockerfile in a ConfigMap or fetch from Git, etc.
# We'll assume it's baked into a known path for this example:
DOCKERFILE_PATH = "/kaniko/build/Dockerfile"

# This is the container image for Kaniko itself:
KANIKO_IMAGE = "gcr.io/kaniko-project/executor:latest"

@kopf.on.create('ml.kea-project.io', 'v1alpha1', 'mlmodels')
@kopf.on.update('ml.kea-project.io', 'v1alpha1', 'mlmodels')
def build_model_image(spec, status, name, namespace, body, logger, **kwargs):
    """
    Trigger a Kaniko job to build/push the ML model image for the specified framework (TF or scikit-learn).
    On success, store the resulting image reference in an annotation.
    """
    model_name = spec.get('modelName')
    s3_path = spec.get('s3Path')
    framework = spec.get('modelFramework', 'sklearn')  # default sklearn
    if not model_name or not s3_path:
        raise kopf.TemporaryError("modelName and s3Path must be defined in MLModel spec", delay=30)

    # The final Docker image name
    image_tag = f"{YANDEX_REGISTRY}/{model_name.lower()}-{framework.lower()}:latest"

    # Check if it might already have a built image
    existing_annotations = body.get('metadata', {}).get('annotations', {})
    existing_image = existing_annotations.get('ml.kea-project.io/image')
    if existing_image == image_tag:
        logger.info(f"Image {image_tag} is already built. Skipping rebuild.")
        return {"image": image_tag}

    # Create a unique job name
    job_name = f"build-{model_name.lower()}-{int(time.time())}"

    # Docker config JSON for Yandex registry auth
    docker_config = {
        "auths": {
            YANDEX_REGISTRY.split('/')[0]: {
                "auth": base64.b64encode(f"oauth:{YANDEX_REGISTRY_TOKEN}".encode('utf-8')).decode('utf-8')
            }
        }
    }

    docker_config_b64 = base64.b64encode(yaml.dump(docker_config).encode("utf-8")).decode("utf-8")

    # Define the Kaniko Job manifest
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": job_name,
            "namespace": NAMESPACE
        },
        "spec": {
            "backoffLimit": 0,
            "template": {
                "spec": {
                    "restartPolicy": "Never",
                    "containers": [
                        {
                            "name": "kaniko",
                            "image": KANIKO_IMAGE,
                            "args": [
                                "--dockerfile=/workspace/Dockerfile",
                                f"--destination={image_tag}",
                                "--context=dir:///workspace",
                                "--build-arg=MODEL_FRAMEWORK=" + framework,
                                "--build-arg=MODEL_PATH=/tmp/model",
                                "--skip-tls-verify=true"
                            ],
                            "env": [
                                {
                                    "name": "MODEL_FRAMEWORK",
                                    "value": framework
                                },
                                {
                                    "name": "MODEL_PATH",
                                    "value": "/tmp/model"
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "name": "docker-config",
                                    "mountPath": "/kaniko/.docker/"
                                },
                                {
                                    "name": "model-data",
                                    "mountPath": "/tmp/model"
                                },
                                {
                                    "name": "build-files",
                                    "mountPath": "/kaniko/build/"
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": "docker-config",
                            "emptyDir": {}
                        },
                        {
                            "name": "model-data",
                            "emptyDir": {}
                        },
                        {
                            "name": "build-files",
                            "configMap": {
                                "name": "serving-files"
                            }
                        }
                    ]
                }
            }
        }
    }

    # Add an init container to write the Docker config
    job_manifest["spec"]["template"]["spec"]["initContainers"] = [
        {
            "name": "init-docker-config",
            "image": "busybox",
            "command": ["sh", "-c"],
            "args": [
                f"mkdir -p /kaniko/.docker && echo '{docker_config_b64}' | base64 -d > /kaniko/.docker/config.json"
            ],
            "volumeMounts": [
                {
                    "name": "docker-config",
                    "mountPath": "/kaniko/.docker/"
                }
            ],
        }
    ]

    # Add a sidecar or steps to download the model from S3
    # For simplicity, we assume the Kaniko Job can access the model via curl
    # Alternatively, use an init container to download the model

    # Define a post-start hook or use an init container to download the model
    # Here, we'll modify the job to include a script in the kaniko container

    # To download the model before building, adjust the args to run a shell script
    # Alternatively, use multi-step Docker build with the model download

    # A cleaner approach: use an init container to download the model to /tmp/model
    # Let's implement this:

    # Add an init container to download the model
    job_manifest["spec"]["template"]["spec"]["initContainers"].append(
        {
            "name": "download-model",
            "image": "curlimages/curl:latest",
            "command": ["sh", "-c"],
            "args": [
                f"mkdir -p /tmp/model && curl -H 'Authorization: Bearer {YANDEX_OBJECT_STORAGE_TOKEN}' -o /tmp/model/model_file '{s3_path}'"
            ],
            "volumeMounts": [
                {
                    "name": "model-data",
                    "mountPath": "/tmp/model"
                }
            ]
        }
    )

    # Create the Job
    batch_api = BatchV1Api()
    try:
        batch_api.create_namespaced_job(namespace=NAMESPACE, body=job_manifest)
        logger.info(f"Kaniko Job {job_name} created to build image {image_tag}.")
    except ApiException as e:
        logger.error(f"Failed to create Kaniko job: {e}")
        raise kopf.TemporaryError("Failed to create Kaniko job", delay=60)

    # Wait for job to complete or fail (simplistic blocking approach).
    # In real systems, you'd rely on asynchronous watchers, or use a separate
    # operator loop for job completions. For simplicity, let's block here:
    job_completed = False
    for _ in range(30):  # ~30 x 10s => up to 5 minutes
        time.sleep(10)
        try:
            job = batch_api.read_namespaced_job(job_name, NAMESPACE)
            if job.status.succeeded == 1:
                job_completed = True
                break
            if job.status.failed is not None and job.status.failed > 0:
                raise kopf.TemporaryError("Kaniko job failed.", delay=60)
        except ApiException as e:
            logger.error(f"Error reading job status: {e}")
            raise kopf.TemporaryError("Error reading job status.", delay=60)

    if not job_completed:
        raise kopf.TemporaryError("Kaniko job not completed in time.", delay=60)

    # If success, patch the MLModel with the final image reference
    annotations = existing_annotations
    annotations['ml.kea-project.io/image'] = image_tag

    cr_api = kubernetes.client.CustomObjectsApi()
    cr_api.patch_namespaced_custom_object(
        group="ml.kea-project.io",
        version="v1alpha1",
        namespace=namespace,
        plural="mlmodels",
        name=name,
        body={
            "metadata": {
                "annotations": annotations
            }
        }
    )
    logger.info(f"Successfully built and pushed image {image_tag}, patched MLModel {name}")

    # Clean up the job
    try:
        batch_api.delete_namespaced_job(job_name, NAMESPACE, propagation_policy="Background")
        logger.info(f"Kaniko Job {job_name} deleted.")
    except ApiException as e:
        logger.warning(f"Failed to delete Kaniko job {job_name}: {e}")

    return {"image": image_tag}


@kopf.on.create('ml.kea-project.io', 'v1alpha1', 'mldeployments')
@kopf.on.update('ml.kea-project.io', 'v1alpha1', 'mldeployments')
def create_ml_deployment(spec, name, namespace, logger, **kwargs):
    """
    Create or update a Deployment, Service, and Ingress for the ML model.
    """
    # Extract fields
    model_name = spec.get('modelName')
    replicas = spec.get('replicas', 1)
    resources = spec.get('resources', {})
    req_cpu = resources.get('requests', {}).get('cpu', '100m')
    req_mem = resources.get('requests', {}).get('memory', '128Mi')
    lim_cpu = resources.get('limits', {}).get('cpu', '500m')
    lim_mem = resources.get('limits', {}).get('memory', '512Mi')

    # Retrieve the MLModel to get the container image
    cr_api = kubernetes.client.CustomObjectsApi()
    try:
        mlmodel = cr_api.get_namespaced_custom_object(
            group="ml.kea-project.io",
            version="v1alpha1",
            namespace=namespace,
            plural="mlmodels",
            name=model_name
        )
    except ApiException as e:
        raise kopf.TemporaryError(f"Failed to get MLModel {model_name}: {e}", delay=30)

    annotations = mlmodel.get('metadata', {}).get('annotations', {})
    image_tag = annotations.get('ml.kea-project.io/image')
    if not image_tag:
        raise kopf.TemporaryError(f"MLModel {model_name} has no image reference yet; can't deploy.", delay=30)

    # Deployment
    deployment_name = f"{model_name}-deployment"
    container_name = f"{model_name}-container"

    deployment_body = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": deployment_name,
            "namespace": NAMESPACE
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": model_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": model_name
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": container_name,
                            "image": image_tag,
                            "resources": {
                                "requests": {
                                    "cpu": req_cpu,
                                    "memory": req_mem
                                },
                                "limits": {
                                    "cpu": lim_cpu,
                                    "memory": lim_mem
                                }
                            },
                            "ports": [{"containerPort": 80}]
                        }
                    ]
                }
            }
        }
    }

    apps_v1 = AppsV1Api()
    try:
        existing_dep = apps_v1.read_namespaced_deployment(deployment_name, NAMESPACE)
        # Patch if exists
        apps_v1.patch_namespaced_deployment(deployment_name, NAMESPACE, deployment_body)
        logger.info(f"Deployment {deployment_name} patched.")
    except ApiException as e:
        if e.status == 404:
            apps_v1.create_namespaced_deployment(NAMESPACE, deployment_body)
            logger.info(f"Deployment {deployment_name} created.")
        else:
            raise

    # Service
    service_name = f"{model_name}-service"
    service_body = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": service_name,
            "namespace": NAMESPACE
        },
        "spec": {
            "selector": {
                "app": model_name
            },
            "ports": [{
                "port": 80,
                "targetPort": 80
            }],
            "type": "ClusterIP"
        }
    }

    core_v1 = CoreV1Api()
    try:
        existing_svc = core_v1.read_namespaced_service(service_name, NAMESPACE)
        core_v1.patch_namespaced_service(service_name, NAMESPACE, service_body)
        logger.info(f"Service {service_name} patched.")
    except ApiException as e:
        if e.status == 404:
            core_v1.create_namespaced_service(NAMESPACE, service_body)
            logger.info(f"Service {service_name} created.")
        else:
            raise

    # Ingress
    ingress_name = f"{model_name}-ingress"
    ingress_path = f"/kea-project/{model_name}"
    ingress_body = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": ingress_name,
            "namespace": NAMESPACE,
            "annotations": {
                "kubernetes.io/ingress.class": "nginx"
            }
        },
        "spec": {
            "rules": [
                {
                    "http": {
                        "paths": [
                            {
                                "path": ingress_path,
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": service_name,
                                        "port": {
                                            "number": 80
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }

    net_v1 = NetworkingV1Api()
    try:
        existing_ing = net_v1.read_namespaced_ingress(ingress_name, NAMESPACE)
        net_v1.patch_namespaced_ingress(ingress_name, NAMESPACE, ingress_body)
        logger.info(f"Ingress {ingress_name} patched.")
    except ApiException as e:
        if e.status == 404:
            net_v1.create_namespaced_ingress(NAMESPACE, ingress_body)
            logger.info(f"Ingress {ingress_name} created.")
        else:
            raise

    return {
        "deployment": deployment_name,
        "service": service_name,
        "ingress": ingress_name
    }
