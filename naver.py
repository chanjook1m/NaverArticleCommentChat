import requests
import rsa
import uuid
import lzstring
import re
import time
import random
import json
import config
from urllib.parse import urlencode


session = None
prevComments = []
currComments = []
lastIdx = -1
lastPage = 1
isUpdated = False


def encrypt(naver_id, naver_pw):
    key_str = requests.get(
        'https://nid.naver.com/login/ext/keys.nhn').content.decode("utf-8")
    sessionkey, Keyname, evalue, nvalue = key_str.split(',')
    evalue, nvalue = int(evalue, 16), int(nvalue, 16)
    pubkey = rsa.PublicKey(evalue, nvalue)
    message = [sessionkey, naver_id, naver_pw]
    merge_message = ""
    for s in message:
        merge_message = merge_message + ''.join([chr(len(s)) + s])
    merge_message = merge_message.encode()
    encpw = rsa.encrypt(merge_message, pubkey).hex()
    return Keyname, encpw


def login(nid, npw):
    global session

    encnm, encpw = encrypt(nid, npw)
    bvsd_uuid = uuid.uuid4()
    o = '{"a":"' + str(bvsd_uuid) + '","b":"1.3.4","h":"1f","i":{"a":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.100.20 Safari/537.36"}}'
    encData = lzstring.LZString.compressToEncodedURIComponent(o)
    bvsd = '{"uuid":"' + str(bvsd_uuid) + '","encData":"' + encData + '"}'
    session = requests.Session()
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.100.20 Safari/537.36'
    }
    data = {
        'enctp': '1',
        'svctype': '0',
        'encnm': encnm,
        'locale': 'ko_KR',
        'url': 'www.naver.com',
        'smart_level': '1',
        'encpw': encpw,
        'bvsd': bvsd
    }
    resp = session.post('https://nid.naver.com/nidlogin.login',
                        data=data, headers=headers)
    if(resp.text.find("location") > -1):
        try:
            login_url = resp.text.split('("')[1].split('"')[0]
            session.get(login_url)
            return "로그인 성공"
        except:
            return "로그인 실패"

    else:
        return "로그인 실패"


def submitComment(articleId, comment):
    global session

    postUrl = "https://apis.naver.com/cafe-web/cafe-mobile/CommentPost.json"

    referer = "https://cafe.naver.com/ca-fe/cafes/29798500/articles/" + \
        str(articleId)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'referer': referer,
    }
    data = {'content': comment, 'cafeId': 29798500,
            'articleId': articleId, 'requestForm': 'A'}

    try:
        print("댓글 등록 중")
        session.post(url=postUrl, headers=headers, data=data)
    except:
        print("댓글 등록 중 문제 발생")
        exit()
    print("댓글 등록 완료")


def getCommentsFromPage(articleId, page):
    commentURL = "http://cafe.naver.com/CommentView.nhn?search.clubid=" + \
        str(config.CLUB_ID) + "&search.articleid=" + \
        str(articleId) + "&search.page=" + str(page)

    try:
        print("요청중: [페이지" + str(page) + "]")
        time.sleep(random.randrange(1, 4))
        requestedResult = session.get(url=commentURL)
        html = requestedResult.text
    except:
        print("요청 중 문제 발생")
        exit()

    return html


def htmlToJson(html):
    try:
        parsedResult = json.loads(html)
    except:
        print("파싱 중 문제 발생")
        exit()

    result = parsedResult.get("result")
    if result is None:
        print("파싱 결과에 문제 있음")
        exit()
    else:
        return result


def cleanHtml(html):
    cleanr = re.compile('<.*?>')
    cleanText = re.sub(cleanr, '', html)
    return cleanText


def saveComments(articleId, parsedResponse):
    global lastPage
    global lastIdx
    global isUpdated
    global prevComments
    global currComments

    totalComments = parsedResponse["totalCount"]
    commentsPerPage = parsedResponse["countPerPage"]
    totalPage = 0

    if totalComments > 0:
        totalPage = ((totalComments - 1) // commentsPerPage) + 1

    for page in range(lastPage, totalPage + 1):
        time.sleep(random.uniform(1.1, 1.5))
        parsedResponse = getParsedComments(articleId, page)

        commentsList = parsedResponse["list"]
        for idx, comment in enumerate(commentsList):
            if idx > lastIdx:
                commentId = comment["commentid"]
                commentDate = comment["writedt"]
                commentUser = comment["writernick"]
                commentContent = cleanHtml(
                    comment["content"].replace("\t", " "))
                commentIsReply = comment["refComment"]
                commentIsDeleted = comment["deleted"]

                if not commentIsDeleted:
                    commentText = commentDate + ":" + \
                        "[" + commentUser + "]" + "\t" + \
                        commentContent
                if commentIsReply:
                    commentText = "->" + commentText
                currComments.append(commentText)
                lastIdx = -1 if idx == 99 else idx
                isUpdated = True
            else:
                isUpdated = False

    lastPage = totalPage


def getNewComments():
    global prevComments
    global currComments

    prevCommentsSet = set(prevComments)
    prevComments = currComments
    newComments = [x for x in currComments if x not in prevCommentsSet]
    currComments = []
    return newComments


def getParsedComments(articleId, startPage):
    response = getCommentsFromPage(articleId, startPage)
    return htmlToJson(response)


def getComments(articleId, startPage):
    global isUpdated

    parsedResponse = getParsedComments(articleId, startPage)
    saveComments(articleId, parsedResponse)

    if isUpdated:
        return getNewComments()


def main(articleId, startPage):
    return getComments(articleId, startPage)
