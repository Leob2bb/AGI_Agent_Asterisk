import praw
import json

# 1. Reddit API 인증 정보 입력
reddit = praw.Reddit(
    client_id="CJq5xhubzTpeSM6zPImTig",
    client_secret="cB5ogfJgeYNTilBDHxy4JTewafcJdA",
    user_agent="dreaminsight-script by /u/Independent_Bad_3598"
)

# 2. 꿈 일기 올라오는 subreddit 접근
subreddit = reddit.subreddit("Dreams")

# 3. 데이터 수집
dreams = []
for submission in subreddit.hot(limit=300):  # 최신 인기글 300개 수집
    if submission.selftext.strip():  # 내용이 있는 글만 저장
        dreams.append({
            "title": submission.title,
            "content": submission.selftext,
            "created": submission.created_utc,
            "score": submission.score,
            "url": submission.url
        })

# 4. JSON 파일로 저장
with open("reddit_dreams.json", "w", encoding="utf-8") as f:
    json.dump(dreams, f, ensure_ascii=False, indent=2)

print(f"수집 완료: {len(dreams)}개의 꿈 일기 저장됨!")

