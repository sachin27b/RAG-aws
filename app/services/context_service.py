def build_context(results):
    parts = []
    for r in results:
        c = r["content"]
        if c["type"] == "TEXT":
            parts.append(c["text"])
        elif c["type"] == "IMAGE":
            parts.append(r["metadata"]["x-amz-bedrock-kb-description"])
    return "\n\n".join(parts)
