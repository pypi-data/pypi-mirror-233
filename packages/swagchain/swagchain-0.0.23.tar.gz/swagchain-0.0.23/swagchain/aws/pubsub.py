import asyncio
from typing import Optional

from aiohttp import ClientSession
from boto3 import Session
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from ..lib.utils import setup_logging

logger = setup_logging(__name__)

pool = Session()
sns = pool.client("sns", region_name="us-east-1")

class SnsPayload(BaseModel):
	Type: Optional[str] = Field(default=None, alias="Type")
	MessageId: Optional[str] = Field(default=None, alias="MessageId") 
	Token: Optional[str] = Field(default=None, alias="Token")
	TopicArn: Optional[str] = Field(default=None, alias="TopicArn")
	Subject: Optional[str] = Field(default=None, alias="Subject")
	Message: str = Field(..., alias="Message")	
	SubscribeURL: Optional[str] = Field(default=None, alias="SubscribeURL")
	Timestamp: Optional[str] = Field(default=None, alias="Timestamp")
	SignatureVersion: Optional[str] = Field(default=None, alias="SignatureVersion")
	Signature: Optional[str] = Field(default=None, alias="Signature")
	SigningCertURL: Optional[str] = Field(default=None, alias="SigningCertURL")

class SNSPubSub:
	"""PubSub channel to send function call results to the client."""
	async def pub(self, topic_arn:str, data:SnsPayload):
		if data.Type == 'SubscriptionConfirmation':
			subscribe_url = data.SubscribeURL
			if subscribe_url:
				async with ClientSession() as session:
					async with session.get(subscribe_url) as resp:
						if resp.status == 200:
							logger.info("Subscribed to topic %s", subscribe_url)
						else:
							logger.error("Failed to subscribe to topic %s", subscribe_url)
			else:
				logger.error("No subscribe url in message %s", data)
		elif data.Type == 'Notification':
			logger.info("Publishing to topic %s", topic_arn)
			sns.publish(TopicArn=topic_arn, Message=data.Message)
		else:
			logger.error("Unknown message type %s", data.Type)
		return {"message": "ok"}
	
	async def sub(self, url:str, name:str):
		topic = sns.create_topic(Name=name)
		topic_arn = topic["TopicArn"]
		sns.subscribe(TopicArn=topic_arn, Protocol="http", Endpoint=url)

		async def generator():
			while True:
				messages = sns.subscribe(
					TopicArn=topic_arn, Protocol="http", Endpoint=url
				)
				for message in messages.get("Messages", []):
					yield message["Body"]
				await asyncio.sleep(300)

		return generator
		