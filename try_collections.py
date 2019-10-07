import os, django
from django.utils import timezone
from django.utils.timezone import datetime, make_aware
from notion.client import NotionClient

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

import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_local2")
django.setup()
from blog.models import Post, Block, Category, Tag

lgr = logging.getLogger(__name__)

lgr.addHandler(logging.StreamHandler())
lgr.setLevel(logging.DEBUG)

TOKEN_V2 = 'd0be0feb450a69966a525b76973ff1f0e46a0ed6b8f795b3cfce65025c755a1fa3288e363bcbb94de2047cdf7339aed9c41cae48e3d95571f53bc056772cc73c21c13fbeb7d9b9bfe98317097a90'

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
client = NotionClient(
    token_v2=TOKEN_V2,
    monitor=False
)

# page = client.get_block("https://www.notion.so/danleyb2/ef408360691a4cd0a62251e4366117d6")

page = client.get_block("https://www.notion.so/danleyb2/merge-a-github-pull-request-into-your-fork-cd6ae0c3e82f42dfaa946163fb0257e2")

lgr.info(page)

exit(0)

# todo use to track if updates exist
# l = page.get('last_edited_time')
# lgr.info(l)
# lgr.info(datetime.fromtimestamp(int(l/1000)))

# Access a database using the URL of the database page or the inline block
cv = client.get_collection_view(
    "https://www.notion.so/danleyb2/ef408360691a4cd0a62251e4366117d6?v=72472887ddf44307a31b20925faadb4b")


def changed_callback(record):
    lgr.info(record)


# registering a change callback on collections

# cv.add_callback(changed_callback)
'''
this is triggered when a new record get's created
however, changes to child properties doesn't trigger
'''

lgr.info(cv)

category, created = Category.objects.get_or_create(
    name='default',
    site_id=1,
    slug='default'
)


def parse_block(child):
    save = True
    child_last_edited = make_aware(datetime.fromtimestamp(int(child.get('last_edited_time')) / 1000))

    try:
        block = Block.objects.get(notion_reference=child.id)
        block.notion_updated_run = children_update_run
        if block.notion_updated_at == child_last_edited:
            # block.save()
            # continue
            # return None
            pass

    except Block.DoesNotExist:
        block = Block()
        block.notion_reference = child.id
        block.notion_updated_run = children_update_run

    block.notion_updated_at = child_last_edited

    if isinstance(child, ColumnListBlock):
        block.type = Block.COLUMN_LIST_BLOCK
        # todo save config
        save = False
        block.save()
        for column_block in child.children:
            lgr.info(column_block)
            cb = parse_block(column_block)
            block.children.add(cb)

            for column_block_child in column_block.children:
                lgr.info(column_block_child)
                cbc = parse_block(column_block_child)
                cb.children.add(cbc)

    elif isinstance(child, ColumnBlock):
        block.type = Block.COLUMN_BLOCK
        # todo save config
        save = False
        block.save()

    elif isinstance(child, TextBlock):
        block.type = Block.TEXT
        block.config['content'] = child.title

    elif isinstance(child, DividerBlock):
        block.type = Block.DIVIDER

    elif isinstance(child, BulletedListBlock):
        block.type = Block.BULLETED_LIST
        block.config['content'] = child.title
    elif isinstance(child, ImageBlock):
        block.type = Block.IMAGE
        block.config['display_source'] = child.display_source
        block.config['file_id'] = child.file_id
        block.config['caption'] = child.caption
        block.config['full_width'] = child.full_width
        block.config['height'] = child.height
        block.config['page_width'] = child.page_width
        block.config['width'] = child.width

    elif isinstance(child, QuoteBlock):
        block.type = Block.QUOTE
        block.config['content'] = child.title
    elif isinstance(child, HeaderBlock):
        block.type = Block.HEADER
        block.config['content'] = child.title
    elif isinstance(child, SubheaderBlock):
        block.type = Block.SUB_HEADER
        block.config['content'] = child.title
    elif isinstance(child, SubsubheaderBlock):
        block.type = Block.SUB_SUB_HEADER
        block.config['content'] = child.title
    elif isinstance(child, CodeBlock):
        block.type = Block.CODE
        block.config['content'] = child.title
        block.config['language'] = child.language
        block.config['wrap'] = child.wrap

    elif isinstance(child, TodoBlock):
        block.type = Block.TODO
        block.config['content'] = child.title
        block.config['checked'] = child.checked
    else:
        lgr.info(child)
        lgr.info('Unknown block type: {}'.format(type(child)))

    if save: block.save()
    return block


posts_update_run = timezone.now()
# List all the records in the collection
for row in cv.collection.get_rows():
    lgr.info('\n\nROW - Published: {}, Id: {}'.format(row.published,row.id))

    row_last_edited = make_aware(datetime.fromtimestamp(int(row.get('last_edited_time')) / 1000))
    lgr.info('row_last_edited: {}'.format(row_last_edited))

    # registering a change callback
    # row.add_callback(changed_callback)

    try:
        post = Post.objects.get(notion_reference=row.id)
        lgr.info('editing existing post')
        post.notion_updated_run = posts_update_run

        post.is_published = row.published
        post.notion_updated_at = row_last_edited

        if not row.published or (post.notion_updated_at == row_last_edited):
            post.save()
            # lgr.info('skipped unpublished or un-updated')
            # continue

    except Post.DoesNotExist:
        lgr.info('creating new post')
        post = Post()
        post.notion_reference = row.id
        post.notion_updated_run = posts_update_run

        post.is_published = row.published
        post.notion_updated_at = row_last_edited

    post.heading = row.name
    # post.sub_heading = row.

    post.site_id = 1
    post.creator_id = 1
    # post.category = category

    post.save()

    for tag_name in row.tags:
        tag, created = Tag.objects.get_or_create(name=tag_name, site_id=1)
        post.tags.add(tag)

    # Retrieving Page content
    # Blocks
    children_update_run = timezone.now()
    for child in row.children:
        block = parse_block(child)
        post.body.add(block)

    # Block.objects.filter(notion_updated_run__lt=children_update_run).delete()

    # break # :)

# delete posts not existing on notion
Post.objects.filter(notion_updated_run__lt=posts_update_run).delete()

# deprecated, kept for reference
'''
# Add a new record
row = cv.collection.add_row()
row.name = "Just some data"
row.is_confirmed = True
row.estimated_value = 399
row.files = ["https://www.birdlife.org/sites/default/files/styles/1600/public/slide.jpg"]
row.person = client.current_user
row.tags = ["A", "C"]
row.where_to = "https://learningequality.org"

# Run a filtered/sorted query using a view's default parameters
result = cv.default_query().execute()
for row in results:
    lgr.info(row)

# Run an "aggregation" query
aggregate_params = [{
    "property": "estimated_value",
    "aggregation_type": "sum",
    "id": "total_value",
}]
result = cv.build_query(aggregate=aggregate_params).execute()
lgr.info("Total estimated value:", result.get_aggregate("total_value"))

# Run a "filtered" query
filter_params = [{
    "property": "assigned_to",
    "comparator": "enum_contains",
    "value": client.current_user,
}]
result = cv.build_query(filter=filter_params).execute()
lgr.info("Things assigned to me:", result)

# Run a "sorted" query
sort_params = [{
    "direction": "descending",
    "property": "estimated_value",
}]
result = cv.build_query(sort=sort_params).execute()
lgr.info("Sorted results, showing most valuable first:", result)

'''
