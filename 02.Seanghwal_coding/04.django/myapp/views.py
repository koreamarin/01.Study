from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt            # csrf를 면제(exempt)하는 기능을 사용하기 위한 라이브러리.
import random

nextId = 4
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is...'},
    {'id':2, 'title':'view', 'body':'View is...'},
    {'id':3, 'title':'Model', 'body':'Model is...'}
]

def HTMLTemplate(articleTag, id=None) :
    global topics
    ol = ''
    for topic in topics :
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    contextUI = ''
    
    if id != None :
        contextUI = f"""
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value="{id}">
                    <input type="submit" value="delete">
                </form>
            </li>
            <li>
                <a href="/update/{id}/">update</a>
            </li>
        """

    return f'''
    <!DOCUMENT HTML>
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ul>
                {ol}
            </ul>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
            Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))




def read(request, id):
    global topics
    article = ''
    for topic in topics :
        if topic['id'] == int(id) :         # urls.py에서 받아오는 id값이 텍스트 형태라서 int 형변환을 했음.
            article = f'''
            <h2>{topic['title']}</h2>
                    {topic['body']}
            '''
    return HttpResponse(HTMLTemplate(article, id))




@ csrf_exempt               # csrf를 면제하는 코드.
def create(request):
    global nextId
    if request.method == 'GET' :    # request가 GET방식일 때 실행되는 함수. 

        # form으로 묶어줘야 submit을 했을 때 form 안에 묶인 모든 값이 전달 됨. form 뒤에 오는 action에 입력된 url로 값들이 전달됨
        # form 뒤에 method="post"라고 명시하지 않으면 get방식으로 데이터가 query sting으로 전달되는데, 이렇게 URL에 정보가 드러나면
        # 서버에 어떠한 정보를 주는지 보는것이 가능하기 때문에 해킹의 가능성이 매우 높아진다.
        # method를 post방식으로 두면 URL의 query string방식이 아닌, header라는 곳에 데이터를 포함해서 보내게 되어
        # 데이터를 눈에 보이지 않게 보낼 수 있다.
        article = '''
            <form action="/create/" method="post">       
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="만듦쓰"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    
    elif request.method == 'POST' :
        # print(request.POST)             # request.POST로 받은 정보를 딕셔너리 형태로 출력함. ex) 딕셔너리 데이터가 {"title":"안녕", "body":"하세요"}이라면 {"title":"안녕", "body":"하세요"} 을 출력
        # print(request.POST['title'])    # request.POST로 받은 딕셔너리 정보 중 title이란 KEY의 VALUE를 출력함. ex) 딕셔너리 데이터가 {"title":"안녕", "body":"하세요"} 이라면  안녕 을 출력
        request_post = request.POST
        title = request_post['title']
        body = request_post['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        topics.append(newTopic)
        nextId += 1
        return redirect(f"/read/{nextId}")                # url로 이동함.

@ csrf_exempt
def delete(request) :
    global topics
    if request.method == 'POST' :
        id = request.POST['id']
        newTopics = []
        for topic in topics :
            if topic['id'] != int(id) :
                newTopics.append(topic)
        topics = newTopics
        
        return redirect('/')

@ csrf_exempt
def update(request, id) :
    global topics
    if request.method == 'GET' :
        for topic in topics :
            if topic['id'] == int(id) :
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            {selectedTopic["title"]} Update
            <form action="/update/{id}/" method="post">       
                <p><input type="text" name="title" value="{selectedTopic["title"]}"></p>
                <p><textarea name="body">{selectedTopic["body"]}</textarea></p>
                <p><input type="submit" value="업데이트쓰"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))

    elif request.method == 'POST' :
        request_post = request.POST
        title = request_post['title']
        body = request_post['body']
        for topic in topics :
            if topic['id'] == int(id) :
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')