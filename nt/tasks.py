import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import datetime, make_aware
from notion.block import (
    TextBlock,
    DividerBlock,
    BulletedListBlock,
    ImageBlock,
    QuoteBlock,
    HeaderBlock,
    SubheaderBlock,
    SubsubheaderBlock,
    CodeBlock,
    TodoBlock,
    ColumnListBlock,
    ColumnBlock
)
from notion.client import NotionClient
from requests.exceptions import ConnectionError

from blog.models import (
    Category,
    Block as BlogBlock,
    Post,
    Tag

)
from nt.models import Block, Config

lgr = logging.getLogger(__name__)


def parse_block(child, config,children_update_run):
    save = True
    new_block_nt_block = False
    child_last_edited = make_aware(datetime.fromtimestamp(int(child.get('last_edited_time')) / 1000))

    try:
        block = BlogBlock.objects.get(nt_block__reference=child.id)
        lgr.info('parse_block existing')
        block_nt_block = block.nt_block

        block_nt_block.updated_run = children_update_run
        if block_nt_block.updated_at == child_last_edited:
            # block.save()
            # continue
            # return None
            pass

    except BlogBlock.DoesNotExist:
        block = BlogBlock()
        new_block_nt_block = True
        lgr.info('parse_block creating new')
        try:block_nt_block = Block.objects.get(reference=child.id)
        except Block.DoesNotExist:
            block_nt_block = Block()
            block_nt_block.reference = child.id
            block_nt_block.config = config

        block_nt_block.updated_run = children_update_run

    block_nt_block.updated_at = child_last_edited

    if isinstance(child, ColumnListBlock):
        block.type = BlogBlock.COLUMN_LIST_BLOCK
        # todo save config
        save = False
        block.save()
        for column_block in child.children:
            lgr.info(column_block)
            cb = parse_block(column_block, config,children_update_run)
            block.children.add(cb)

            for column_block_child in column_block.children:
                lgr.info(column_block_child)
                cbc = parse_block(column_block_child, config,children_update_run)
                cb.children.add(cbc)
    elif isinstance(child, ColumnBlock):
        block.type = BlogBlock.COLUMN_BLOCK
        # todo save config
        save = False
        block.save()
    elif isinstance(child, TextBlock):
        block.type = BlogBlock.TEXT
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, DividerBlock):
        block.config = {}
        block.type = BlogBlock.DIVIDER
    elif isinstance(child, BulletedListBlock):
        block.type = BlogBlock.BULLETED_LIST
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, ImageBlock):
        block.type = BlogBlock.IMAGE
        block.config = {}
        block.config['display_source'] = child.display_source
        block.config['file_id'] = child.file_id
        block.config['caption'] = child.caption
        block.config['full_width'] = child.full_width
        block.config['height'] = child.height
        block.config['page_width'] = child.page_width
        block.config['width'] = child.width
    elif isinstance(child, QuoteBlock):
        block.type = BlogBlock.QUOTE
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, HeaderBlock):
        block.type = BlogBlock.HEADER
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, SubheaderBlock):
        block.type = BlogBlock.SUB_HEADER
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, SubsubheaderBlock):
        block.type = BlogBlock.SUB_SUB_HEADER
        block.config = {}
        block.config['content'] = child.title
    elif isinstance(child, CodeBlock):
        block.type = BlogBlock.CODE
        block.config = {}
        block.config['content'] = child.title
        block.config['language'] = child.language
        block.config['wrap'] = child.wrap
    elif isinstance(child, TodoBlock):
        block.type = BlogBlock.TODO
        block.config = {}
        block.config['content'] = child.title
        block.config['checked'] = child.checked
    else:
        lgr.info(child)
        lgr.info('Unknown block type: {}'.format(type(child)))

    if save:
        block.save()

    if new_block_nt_block:
        block_nt_block.block = block
    block_nt_block.save()

    return block


def process_post(row, config, posts_update_run):
    lgr.info('\n\nROW - Published: {}, Id: {}'.format(row.published, row.id))

    row_last_edited = make_aware(datetime.fromtimestamp(int(row.get('last_edited_time')) / 1000))
    lgr.info('row_last_edited: {}'.format(row_last_edited))

    # registering a change callback
    # row.add_callback(changed_callback)

    try:
        post = Post.objects.get(nt_block__reference=row.id)
        lgr.info('editing existing post')
        post.is_published = row.published

        post_nt_block = post.nt_block
        post_nt_block.updated_run = posts_update_run
        post_nt_block.updated_at = row_last_edited
        post_nt_block.save()

        if not row.published or (post_nt_block.updated_at == row_last_edited):
            post.save()
            # lgr.info('skipped unpublished or un-updated')
            # continue

    except Post.DoesNotExist:
        lgr.info('creating new post')
        post = Post()
        post.is_published = row.published
        post.site_id = 1
        post.creator_id = 1

        try:
            post_nt_block = Block.objects.get(reference=row.id)
        except Block.DoesNotExist:
            post_nt_block = Block()
            post_nt_block.reference = row.id
            post_nt_block.config = config

        post_nt_block.updated_at = row_last_edited
        post_nt_block.updated_run = posts_update_run

        lgr.info('saving post: {}'.format(post))
        post.save()
        lgr.info('saved post: {}'.format(post))
        lgr.info('saving post_nt_block: {}'.format(post_nt_block))
        post_nt_block.post = post
        post_nt_block.save()
        lgr.info('saved post_nt_block: {}'.format(post_nt_block))

    post.heading = row.name
    # post.sub_heading = row.
    # post.category = category

    post.save()

    for tag_name in row.tags:
        tag, created = Tag.objects.get_or_create(name=tag_name, site_id=1)
        post.tags.add(tag)

    # Retrieving Page content
    # Blocks
    children_update_run = timezone.now()
    for child in row.children:
        block = parse_block(child, config,children_update_run)
        post.body.add(block)

    deleted = BlogBlock.objects.filter(nt_block__updated_run__lt=children_update_run).delete()
    lgr.info(deleted)
    # break # :)


@shared_task
def sync_page(url):
    site_id = 1
    config = Config.objects.get(site_id=site_id)

    try:
        client = NotionClient(
            token_v2=config.token or settings.TOKEN_V2,
            monitor=False
        )
    except ConnectionError as e:
        lgr.error(e)
        return

    post_block = client.get_block(url)
    lgr.info(post_block)
    posts_update_run = timezone.now()
    process_post(post_block, config, posts_update_run)


@shared_task
def sync_all():
    site_id = 1
    config = Config.objects.get(site_id=site_id)

    try:
        client = NotionClient(
            token_v2=config.token or settings.TOKEN_V2,
            monitor=False
        )
    except ConnectionError as e:
        lgr.error(e)
        return

    cv = client.get_collection_view(
        "https://www.notion.so/danleyb2/ef408360691a4cd0a62251e4366117d6?v=72472887ddf44307a31b20925faadb4b")

    lgr.info(cv)

    category, created = Category.objects.get_or_create(
        name='default',
        site_id=1,
        slug='default'
    )

    posts_update_run = timezone.now()
    # List all the records in the collection
    for row in cv.collection.get_rows():
        process_post(row, config, posts_update_run)

    # delete posts not existing on notion
    # todo Post.objects.filter(notion_updated_run__lt=posts_update_run).delete()
