from typing import Optional, List
import importlib

import uuid

from firebird import zkdb
from firebird.libs.k8 import K8Accessor
from firebird.rabbitmq import get_connection, RabbitMQ

from firebird.base import Pipeline, PipelineRegistry, PortType, StartupResource, ShutdownResource

class CoreAPIException(Exception):
    pass

class CoreAPIInvalidArguments(CoreAPIException):
    pass

class CoreAPIs:
    k8_accessor: K8Accessor
    zk_config: dict
    rabbitmq_config: Optional[dict]

    def __init__(self, *, zk_config:dict, k8_accessor:K8Accessor, rabbitmq_config:Optional[dict]=None):
        self.zk_config = zk_config
        self.k8_accessor = k8_accessor
        self.rabbitmq_config = rabbitmq_config
    
    def list_pipelines(self) -> List[PipelineRegistry]:
        with zkdb(**self.zk_config) as db:
            return db.get_pipelines()

    def get_pipeline(self, id:str) -> PipelineRegistry:
        with zkdb(**self.zk_config) as db:
            return db.get_pipeline(id)


    def start_pipeline(self, id:str, replicas:int=1) -> None:
        """Start a pipeline

        Args:
            id (str): pipeline ID
        """
        with zkdb(**self.zk_config) as db:
            pipeline_registry:PipelineRegistry = db.get_pipeline(id)

            if pipeline_registry.is_running:
                raise CoreAPIInvalidArguments(f"Pipeline(id={id}) is already running!")

            for startup_resource in pipeline_registry.startup_resources:
                # TODO: replace print with logger
                # TODO: handler failure
                self.k8_accessor.apply_by_content(
                    title=startup_resource.title,
                    template_content=startup_resource.yaml,
                    context={
                        "namespace_name": pipeline_registry.namespace_name,
                        "image_name": pipeline_registry.image_name,
                        "pipeline_id": id,
                        "replicas": replicas
                    }
                )
            db.set_pipeline_is_running(id, is_running=True)

    def stop_pipeline(self, id:str) -> None:
        """Stop a pipeline

        Args:
            id (str): pipeline ID
        """
        with zkdb(**self.zk_config) as db:
            pipeline_registry = db.get_pipeline(id)

            if not pipeline_registry.is_running:
                raise CoreAPIInvalidArguments(f"Pipeline(id={id}) is already stopped!")

            for shutdown_resource in pipeline_registry.shutdown_resources:
                if shutdown_resource.type == "Statefulset":
                    self.k8_accessor.delete_statefulset(
                        namespace=pipeline_registry.namespace_name, 
                        name=shutdown_resource.name
                    )
                elif shutdown_resource.type == "Deployment":
                    self.k8_accessor.delete_deployment(
                        namespace=pipeline_registry.namespace_name, 
                        name=shutdown_resource.name
                    )
                else:
                    raise Exception(f"Unrecognized resource type: {shutdown_resource.type}")
            db.set_pipeline_is_running(id, is_running=False)

    def register_pipeline(
        self, 
        pipeline_namespace_name:str, 
        pipeline_image_name:str, 
        pipeline_module_name:str
    ) -> None:
        """Register a pipeline

        Args:
            pipeline_namespace_name (str): Namespace name of the pipeline
            pipeline_image_name (str): docker image name of the pipeline
            pipeline_module_name (str): python module name of the pipeline
        """
        pipeline:Pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
        pipeline_info = pipeline.get_info()
        startup_resources, shutdown_resources = pipeline.get_resources()

        mq = RabbitMQ(
            connection = get_connection(**self.rabbitmq_config),
            topic = pipeline.id
        )
        # create rabbitmq topic, etc
        mq.initialize()

        with zkdb(**self.zk_config) as db:
            pipeline_registry = PipelineRegistry(
                pipeline_info = pipeline_info,
                module=pipeline_module_name,
                namespace_name=pipeline_namespace_name,
                image_name=pipeline_image_name,
                is_running=False,
                startup_resources=startup_resources,
                shutdown_resources=shutdown_resources
            )
            db.register_pipeline(pipeline_registry)

    def unregister_pipeline(self, id: str) -> None:
        """Unregister a pipeline

        Args:
            id (str): id of the pipeline to be unregisterred
        """
        with zkdb(**self.zk_config) as db:
            db.unregister_pipeline(id)

        mq = RabbitMQ(
            connection = get_connection(**self.rabbitmq_config),
            topic = id
        )
        # delete queues
        mq.delete_queues()
