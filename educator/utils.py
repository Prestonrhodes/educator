def safe_exec(code):
    try:
        exec(code)
        return "Executed successfully!"
    except Exception as e:
        return f"Error: {e}"
