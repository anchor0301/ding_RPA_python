from notion.client import NotionClient
import key
# 아래 <token_v2> 대신에 위에서 복사한 자신의 token 값을 입력한다.
client = NotionClient(token_v2=key.token_v2)

# 아래 <url>에 읽고 쓰기를 원하는 페이지 주소를 입력한다.
page = client.get_block(key.url)

# 제목 조회
print("페이지 제목", page.title)