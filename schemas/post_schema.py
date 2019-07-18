"""User schema"""

import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from database.models import Post, User, db
from input_schemas.post_input import (DeletePostInput, CreatePostInput,
                                      UpdatePostInput)


class PostType(SQLAlchemyObjectType):
	"""Post schema object"""
	
	class Meta:
		"""Meta class"""
		
		model = Post
		interfaces = (graphene.relay.Node,)


class CreatePosts(graphene.Mutation):
	"""Mutation class for adding posts
	
	Example:
		mutation createPost($data: CreatePostInput!) {
			createPost(data: $data) {
				post {
					title
					body
					author {
						username
					}
				}
			}
		}
	"""
	
	post = graphene.Field(PostType)
	
	class Arguments:
		"""Argument class"""
		
		data = CreatePostInput(required=True)
	
	def mutate(self, info, data):
		"""Mutate method."""
		
		user = User.query.filter_by(username=data['username']).first()
		
		if user is None:
			raise GraphQLError('User not found.')
		
		post = Post(title=data['title'], body=data['body'])
		post.author = user
		db.session.add(post)
		db.session.commit()
		
		return CreatePosts(post=post)


class UpdatePost(graphene.Mutation):
	"""Mutation class for updating posts
	
	Example:
		mutation updatePost($data: UpdatePostInput!) {
			updatePost(data: $data) {
				post {
					title
					body
				}
			}
		}
	"""
	
	post = graphene.Field(PostType)
	
	class Arguments:
		"""Argument class"""
		
		data = UpdatePostInput(required=True)
	
	def mutate(self, info, data):
		"""Mutate method."""
		
		id = data.pop('id')
		
		post = Post.query.filter_by(uuid=id).first()
		
		if post is None:
			raise GraphQLError('Post not found.')
		
		for field, value in data.items():
			setattr(post, field, value)
		
		db.session.commit()
		
		return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
	"""Mutation class to delete a post"""
	
	deleted = graphene.Boolean(description="Post deleted")
	
	class Arguments:
		"""Argument class"""
		
		input = DeletePostInput(required=True)
	
	def mutate(self, info, input):
		
		"""Method to mutate """
		
		id = input.get('id')
		post = Post.query.filter_by(uuid=id).first()
		
		if post is None:
			raise GraphQLError('Post not found.')
		
		db.session.delete(post)
		db.session.commit()
		
		return DeletePost(deleted=True)


class Mutation(graphene.ObjectType):
	"""Mutation class"""
	
	create_post = CreatePosts.Field()
	update_post = UpdatePost.Field()
	delete_post = DeletePost.Field()


class Query(graphene.ObjectType):
	"""Query class"""
	
	node = graphene.relay.Node.Field()
	
	posts = graphene.List(PostType)
	post = graphene.Field(PostType, uuid=graphene.Int(), required=True)
	
	# with pagination capabilities
	all_posts = SQLAlchemyConnectionField(PostType,
	                                      sort=PostType.sort_argument())
	
	def resolve_posts(self, info, **kwargs):
		"""Query for all posts
		
		Example:
			query getAllPosts($limit: Int, $nextCursor: String) {
				allPosts(first: $limit, after: $nextCursor){
					pageInfo{
						hasNextPage,
						hasPreviousPage,
						startCursor,
						endCursor
					}
					edges{
						cursor
						node{
							title
							body
							author {
								username
							}
						}
					}
				}
			}
		"""
		
		return Post.query.all()
	
	def resolve_post(self, info, **kwargs):
		"""Querying a single post
		
		Example:
			query getAPost($uuid: Int!){
				post(uuid: $uuid){
					uuid
					title
					body
				}
			}
		"""
		
		id = kwargs.get('uuid', None)
		return Post.query.filter_by(uuid=id).first()
