"""Base schema"""

# third party imports
import graphene

# local imports
from . import post_schema, user_schema


class Mutation(post_schema.Mutation):
	"""Mutation class"""

	pass


class Query(post_schema.Query, user_schema.Query):
	"""Query class"""

	pass


schema = graphene.Schema(query=Query, mutation=Mutation)
