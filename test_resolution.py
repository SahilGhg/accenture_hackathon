from agents.resolution_agent import recommend_resolution

if __name__ == "__main__":
    chat = "Customer says their antivirus keeps blocking the software installation."
    resolution, source = recommend_resolution(chat)
    print(resolution, f"(Source: {source})")
