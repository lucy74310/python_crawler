from bs4 import BeautifulSoup

html = '''<td class="title">
	<div class="tit3" id="my-div">
		<a href="/movie/bi/mi/basic.nhn?code=161967" title="기생충">기생충</a>
	</div>
</td>'''


# 1. tag 조회
def ex1():
	bs = BeautifulSoup(html, 'html.parser')
	# print(bs)
	# print(type(bs))

	tag = bs.td
	# print(tag)
	# print(type(tag))

	tag = bs.a
	# print(tag)
	# print(type(tag))

	tag = bs.td.div
	# print(tag)
	# print(type(tag))

	tag = bs.td.h4
	# print(tag) 	# None
	# print(type(tag)) # <class 'NoneType'> # None도 객체임


# 2. attribute 값 가져오기
def ex2():
	bs = BeautifulSoup(html, 'html.parser')

	tag = bs.td
	print(tag['class'], type(tag['class']))

	tag = bs.div
	print(tag['id'], type(tag['id'])) # id 없음 => KeyError: 'id'

	print(tag.attrs, type(tag.attrs))


# 3. attribute로 태그 조회하기
def ex3():
	bs = BeautifulSoup(html, 'html.parser')

	# td 태그를 찾는데, class속성값이 title 인 td 태그를 찾겠다
	tag = bs.find('td', attrs={'class': 'title'})
	print(tag, type(tag))

	# 속성값에서 class 값이 tit3인 태그
	tag = bs.find(attrs={'class': 'tit3'})
	print(tag)


if __name__ == '__main__':
	# ex1()
	# ex2()
	ex3()
