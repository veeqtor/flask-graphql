"""User schema"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import User


class UserObject(SQLAlchemyObjectType):
	"""User schema object"""

	class Meta:
		"""Meta class"""

		model = User
		interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
	"""Query class"""

	node = graphene.relay.Node.Field()
	all_users = SQLAlchemyConnectionField(UserObject)
