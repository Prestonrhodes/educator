def load_topic(topic):
    try:
        module = __import__(f"topics.{topic.replace(' ', '_')}", fromlist=["Topic"])
        return module.Topic()
    except ImportError:
        return None
