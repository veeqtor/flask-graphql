"""Base schema"""

# third party imports
import graphene

# local imports
from . import post_schema, user_schema


class Query(post_schema.Query, user_schema.Query):
	"""Query class"""

	pass


schema = graphene.Schema(query=Query)