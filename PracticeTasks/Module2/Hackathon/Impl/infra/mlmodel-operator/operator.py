def build_and_push_image_with_kaniko(context_path, dockerfile_path, image_name, namespace):
    kaniko_pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": f"kaniko-build-{image_name.replace(':', '-')}",
            "namespace": namespace
        },
        "spec": {
            "containers": [{
                "name": "kaniko",
                "image": "gcr.io/kaniko-project/executor:latest",
                "args": [
                    f"--dockerfile={dockerfile_path}",
                    f"--destination={image_name}",
                    "--context=/workspace",
                    "--insecure",
                    "--skip-tls-verify"
                ],
                "volumeMounts": [
                    {
                        "name": "build-context",
                        "mountPath": "/workspace"
                    },
                    {
                        "name": "docker-config",
                        "mountPath": "/kaniko/.docker/"
                    }
                ]
            }],
            "restartPolicy": "Never",
            "volumes": [
                {
                    "name": "build-context",
                    "configMap": {
                        "name": "build-context"
                    }
                },
                {
                    "name": "docker-config",
                    "secret": {
                        "secretName": "registry-secret"
                    }
                }
            ]
        }
    }
    # Создание Pod с Kaniko
    core_api = kubernetes.client.CoreV1Api()
    core_api.create_namespaced_pod(namespace=namespace, body=kaniko_pod_manifest)
    # Ожидание завершения Pod и обработка статуса
    # Реализация логики ожидания и обработки ошибок
