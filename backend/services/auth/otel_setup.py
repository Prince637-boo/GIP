from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor

def init_tracing(app, db_engine=None):
    resource = Resource.create({"service.name": "baggage-service"})
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces", insecure=True) 
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

    # instrument frameworks
    FastAPIInstrumentor.instrument_app(app)
    if db_engine:
        SQLAlchemyInstrumentor().instrument(engine=db_engine)
    AioPikaInstrumentor().instrument()
