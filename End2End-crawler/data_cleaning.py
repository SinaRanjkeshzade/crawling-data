def clean_youtube_data(raw_data):
    """
    Clean and normalize raw YouTube data.
    """
    cleaned = []
    for item in raw_data:
        # TODO: Add more cleaning steps
        if item.get('title') and item.get('url'):
            cleaned.append({
                'title': item['title'].strip(),
                'url': item['url'].strip()
            })
    return cleaned 