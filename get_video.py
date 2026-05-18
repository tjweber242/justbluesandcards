import urllib.request, re, os, sys

channel_id = "UCLzi7kR37MWuXhcYaaDhMng"

urls = [
    f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
    f"https://www.youtube.com/channel/{channel_id}/videos",
    f"https://www.youtube.com/@JustBluesandCards/videos",
]

video_id = None
for url in urls:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })
        content = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        print(f"Fetched {url}, length: {len(content)}")

        patterns = [
            r'<yt:videoId>([A-Za-z0-9_-]{11})</yt:videoId>',
            r'"videoId":"([A-Za-z0-9_-]{11})"',
            r'watch\?v=([A-Za-z0-9_-]{11})',
            r'/shorts/([A-Za-z0-9_-]{11})',
        ]
        for pat in patterns:
            m = re.search(pat, content)
            if m:
                video_id = m.group(1)
                print(f"Found video ID: {video_id} using pattern: {pat}")
                break
        if video_id:
            break
    except Exception as e:
        print(f"Error fetching {url}: {e}")

if not video_id:
    print("ERROR: Could not find video ID")
    sys.exit(1)

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"video_id={video_id}\n")
