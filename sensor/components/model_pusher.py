from sensor.predictor import ModelResolver
from sensor.entity.config_entity import DataTransformationConfig, ModelTrainerConfig, ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
from sensor.utils import load_object, save_object
import os,sys


class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
                  data_transformation_artifact:DataTransformationArtifact,
                    model_trainer_artifact:ModelTrainerArtifact):
        
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver()
        except Exception as e:
            raise SensorException(e, sys)
        
        
    def initiate_model_pusher(self,) -> ModelPusherArtifact:
        try:
            #load object
            logging.info(f"Loading transformer model and target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            
            # save models in model pusher dir
            logging.info(f"Saving model into model pusher directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            # save models in saved model dir
            ## Get all the path for transformer, model and target encoder first otherwise the folder 
            ## count will keep increasing and will be saved in differnt folder number
            
            logging.info(f"Saving model in saved model dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            model_path=self.model_resolver.get_latest_save_model_path()
            target_encoder_path=self.model_resolver.get_latest_save_target_encoder_path()
            
            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)
            
            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
            saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)