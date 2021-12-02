import random
from django.http.response import JsonResponse

from django.shortcuts import render, get_object_or_404
from django import views

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from backend.models import Mailing, MailingLink, User


def filter_tag(tag: Tag, ol_number=None):
    if isinstance(tag, NavigableString):
        text = tag
        text = text.replace('<', '&#60;')
        text = text.replace('>', '&#62;')
        return text

    html = str()
    li_number = 0
    for child_tag in tag:
        if tag.name == 'ol':
            if child_tag.name == 'li':
                li_number += 1
        else:
            li_number = None

        html += filter_tag(child_tag, li_number)

    format_tags = ['strong', 'em', 'pre', 'b', 'u', 'i', 'code']
    if tag.name in format_tags:
        return f'<{tag.name}>{html}</{tag.name}>'

    if tag.name == 'a':
        return f"""<a href="{tag.get("href")}">{tag.text}</a>"""

    if tag.name == 'li':
        if ol_number:
            return f'{ol_number}. {html}'
        return f'•  {html}'

    if tag.name == 'br':
        html += '\n'

    if tag.name == 'span':
        styles = tag.get_attribute_list('style')
        if 'text-decoration: underline;' in styles:
            return f'<u>{html}</u>'

    if tag.name == 'ol' or tag.name == 'ul':
        return '\n'.join(map(lambda row: f'   {row}', html.split('\n')))

    return html


def filter_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return filter_tag(soup)


def get_random_text(body: str):
    while True:
        open_index = body.find('{')
        close_index = body.find('}')
        if open_index == -1 or close_index == -1:
            break

        pattern = body[open_index+1:close_index]
        word = random.choice(pattern.split('|')).strip()
        body = body.replace(body[open_index:close_index+1], word)

    return body


def get_random_forms(mailing: Mailing):
    forms = []
    mailing_links = list(mailing.links.all())
    random.shuffle(mailing_links)
    for i in range(min(mailing.forms_count, mailing.links.count())):
        body = get_random_text(mailing.body)
        mailing_link = mailing_links[i]
        forms.append({
            'body': body,
            'filtered_body': filter_html(body),
            'mailing_link': mailing_link,
        })

    return forms


class IndexView(views.View):
    template_name = 'index.html'

    def get(self, request, title):
        mailing = get_object_or_404(Mailing, title=title)
        mailing_forms = get_random_forms(mailing)
        return render(request, self.template_name, {
            'mailing_forms': mailing_forms,
        })

    def post(self, request, title):
        try:
            text = request.POST.get('text', None)
            link_id = request.POST.get('link_id', None)
            screenshot_link = request.POST.get('screenshot_link', None)
            mailing_link = MailingLink.objects.get(id=link_id)
            User.objects.create(
                mailing_link=mailing_link.link,
                screenshot_link=screenshot_link,
                text=text,
            )
            if mailing_link.must_deleted:
                mailing_link.delete()

        except:
            return JsonResponse({'sucess': False})
        else:
            return JsonResponse({'sucess': True})
