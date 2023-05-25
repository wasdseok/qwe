from django.shortcuts import render


# from board.models import Market

from django.db import connection
from common.CommonUtil import dictfetchall, CommonPage

def list(request, pg):
    cursor=connection.cursor()
    sql = "select count(*) from board_board"
    cursor.execute(sql)
    totalCnt = int(cursor.fetchone()[0])
    cp = CommonPage(totalCnt, pg, 10)

    sql= f"""
        select A.postnum, A.userid, A.username, A.title,
          to_char(A.wdate, 'yyyy-mm-dd') wdate, contents, hit, num 
        from 
        (   
            select postnum, userid, username, title, wdate, contents, hit,
            row_number() over(order by postnum desc) num,
            ceil (row_number() over(order by postnum desc)/10)-1 pg
            from board_board
        ) A
        where A.pg ={pg}
    
    """
    cursor.execute(sql)
    boardList=dictfetchall(cursor)
    # print(boardList)
    return render(request, "board/board_list.html", {'boardList':boardList, 'commonPage':cp})

from board.models import Board

def views(request, postnum):
    board = Board.objects.get(postnum = postnum)
    board.hit = board.hit+1
    board.save() 
    return render(request, "board/board_view.html", {'boardItem': board})

from board.forms import BoardForm

def write(request):
    return render(request, "board/board_write.html")

from django.utils import timezone
from django.shortcuts import redirect 
from django.db.models import Max

def save(request):
    form=BoardForm(request.POST)
    board=form.save(commit=False)
    max_score = Board.objects.aggregate(max_score=Max('postnum'))['max_score']
    board.postnum = max_score + 1
    board.wdate = timezone.now()
    board.hit=0
    board.save()
    return redirect("board:list", pg=0)

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def modify(request):
    # jsonObject=jason.loads(request.body)
    result={"result": "success", "title":"title", "username":"username", "contents":"contents"}
    return JsonResponse(result, status=200)