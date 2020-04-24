import flask_paginate as fp


_bs4 = '<li class="page-item">\
<a class="page-link" onClick="searchRecipes({0})" aria-label="Предыдущая">\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Previous</span></a></li>'
fp.PREV_PAGES = dict(
                     bootstrap4=_bs4,
                     foundation='<li class="arrow"><a onClick="searchRecipes({0})">{1}</a></li>',
                     )

_bs4 = '<li class="page-item">\
<a class="page-link" onClick="searchRecipes({0})" aria-label="Следующая">\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Next</span></a></li>'
fp.NEXT_PAGES = dict(bootstrap4=_bs4, foundation='<li class="arrow"><a href="{0}">{1}</a></li>')

_bs4 = '<li class="page-item active"><a class="page-link">{0} \
<span class="sr-only">(current)</span></a></li>'
fp.CURRENT_PAGES = dict(bootstrap4=_bs4, foundation='<li class="current"><a>{0}</a></li>')

fp.LINK = '<li><a onClick="searchRecipes({0})" >{1}</a></li>'
fp.BS4_LINK = '<li class="page-item"><a class="page-link" onClick="searchRecipes({0})">{1}</a></li>'

_bs4 = '<li class="page-item disabled"><span class="page-link">...</span></li>'
_fa = '<li class="unavailable"><a>...</a></li>'
fp.GAP_MARKERS = dict(bootstrap4=_bs4, foundation=_fa)

_bs4 = '<li class="page-item disabled"><span class="page-link"> {0} </span></li>'
_fa = '<li class="unavailable"><a>{0}</a></li>'
fp.PREV_DISABLED_PAGES = dict(bootstrap4=_bs4, foundation=_fa)
fp.NEXT_DISABLED_PAGES = dict(bootstrap4=_bs4, foundation=_fa)
fp.DISPLAY_MSG = 'Показаны <b>{start} - {end}</b> {record_name} из <b>{total}</b>'


class MyPagination(fp.Pagination):

    def page_href(self, page):
        return page or 1
