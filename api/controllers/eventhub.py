from azure.eventhub import EventHubProducerClient, EventData
from ..config.config import configuration
import json


def enviar_json_ao_eventhub(data):
    eventhub_endpoint = configuration["development"].EVENTHUB_ENDPOINT
    eventhub_name = configuration["development"].EVENTHUB_NAME

    try:
        producer_client = EventHubProducerClient.from_connection_string(
            conn_str=eventhub_endpoint, eventhub_name=eventhub_name
        )

        event_data_batch = producer_client.create_batch()
        s = json.dumps(data)

        event_data_batch.add(EventData(s))

        producer_client.send_batch(event_data_batch)

        producer_client.close()

        return "ok"

    except Exception as e:
        return type(e).__name__
