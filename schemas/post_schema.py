"""User schema"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import Post


class PostObject(SQLAlchemyObjectType):
	"""Post schema object"""

	class Meta:
		"""Meta class"""

		model = Post
		interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
	"""Query class"""

	node = graphene.relay.Node.Field()
	all_posts = SQLAlchemyConnectionField(PostObject)
