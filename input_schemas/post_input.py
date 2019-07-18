"""Module for post input"""

import graphene


class DeletePostInput(graphene.InputObjectType):
	"""Input objects"""

	id = graphene.Int(required=True, description="Id of the Post.")


class CreatePostInput(graphene.InputObjectType):
	"""Input objects"""

	title = graphene.String(required=True, description="Post title")
	body = graphene.String(required=True, description="Post body")
	username = graphene.String(required=True, description="Author's username")


class UpdatePostInput(graphene.InputObjectType):
	"""Input objects"""

	id = graphene.Int(required=True, description="Id of the Post.")
	title = graphene.String(description="Post title")
	body = graphene.String(description="Post body")
