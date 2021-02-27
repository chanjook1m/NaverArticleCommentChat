# NaverArticleCommentChat

## Description
네이버 카페의 글의 댓글을 채팅 목록처럼 불러오고 댓글을 쉽게 입력 할 수 있는 프로그램

![실행화면](https://user-images.githubusercontent.com/27846824/105046989-21edb280-5aad-11eb-9e56-c95882f35229.gif)

## Dependencies
- Python 3

## Description of files
| filename | description |
| -------- | ----------- |
| README.md | Text file description of the project |
| config.py | Config data, e.g. cafeID, error messages, etc. |
| crawling.py | Crawling Worker used by thread in ./gui/board.py |
| index.py | Main starting point where login and creating gui are processed |
| naver.py | Perform functions like naver API, e.g. login, saveComments, getNewComments, etc. |
| gui | GUI form, Perform GUI events |

## Getting Started
### Installation
1. Clone the repo
```code
git clone https://github.com/chanjook1m/NaverArticleCommentChat.git
```
2. Set CLUB_ID (naver cafe ID) and ART_ID (naver cafe article ID) in _config.py_
