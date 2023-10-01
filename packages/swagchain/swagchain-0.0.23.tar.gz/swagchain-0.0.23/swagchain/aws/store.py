import os

from boto3 import Session

from .odm import LazyProxy, async_io


class S3Client(LazyProxy[Session]):
	def __init__(self) -> None:
		self.session = self.__load__()
		super().__init__()

	def __load__(self) -> Session:
		return Session()

	@property
	def client(self):
		return self.session.client(service_name="s3", region_name="us-east-1") # type: ignore

	@async_io
	def put_object(self, namespace:str, filename: str, body: bytes):
		key = f"{namespace}/{filename}"
		self.client.put_object(Bucket=os.environ["AWS_S3_BUCKET"], Key=key, Body=body)
		return self.client.generate_presigned_url(
			"get_object", Params={"Bucket": os.environ["AWS_S3_BUCKET"], "Key": key}
		)	
	
	@async_io
	def get_object(self, namespace:str, filename: str):
		key = f"{namespace}/{filename}"
		return self.client.generate_presigned_url(
			"get_object", Params={"Bucket": os.environ["AWS_S3_BUCKET"], "Key": key}
		)
	