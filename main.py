from black import re
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

class VideoModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   views = db.Column(db.Integer, nullable=False)
   likes = db.Column(db.Integer, nullable=False)
   
   def __repr__(self):
    return f"Video(name={name}, views={views}, likes={likes}"

#db.create_all()

names = {"bradley":{"age": 32, "gender": "male"},
        "autumn": {"age": 23, "gender": "female"}}

class YesOrNo(Resource):
  def get(self, name):
    return names[name]

  def post(self):
    return {"data": "Post"}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required.", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required.", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required.", required=True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type=str, help="Name of the video is required.")
video_patch_args.add_argument("views", type=int, help="Views of the video is required.")
video_patch_args.add_argument("likes", type=int, help="Likes on the video is required.")

resource_fields = {
  "id": fields.Integer,
  "name": fields.String,
  "views": fields.Integer,
  "likes": fields.Integer
}

def abort_if_video_id_doesnt_exist(video_id):
  video = VideoModel.query.filter_by(id=video_id).first()
  if not video:
    abort(404, message="Video ID is not valid")

# def abort_if_video_exists(video_id):
#   if video_id in videos:
#     abort(409, message="Video already exists with that Id")



class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
      # abort_if_video_id_doesnt_exist(video_id)
      result = VideoModel.query.filter_by(id=video_id).first()
      if not result:
        abort(404, message="Video not found by id")

      return result

    @marshal_with(resource_fields)
    def put(self, video_id):
      # abort_if_video_exists(video_id)
      args = video_put_args.parse_args()
      record = VideoModel.query.filter_by(id=video_id).first()

      if record:
        abort(409, message="Video id taken")
      
      video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
      db.session.add(video)
      db.session.commit()
      return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
      args = video_put_args.parse_args()
      result = VideoModel.query.filter_by(id=video_id).first()

      if not result: abort (404, "Video not found. Cannot update")

      if args['name']:
        result.name = args['name']
      if args['views']:
        result.views = args['views']
      if args['likes']:
        result.likes = args['likes']

      db.session.commit()

    def delete(self, video_id ):
      abort_if_video_id_doesnt_exist(video_id)
      VideoModel.query.filter_by(id=video_id).delete()
      return 'Video Deleted', 204

    def delete_all(self):
      db.drop_all()
      return 'Dropped database', 204


api.add_resource(Video, '/videos/<int:video_id>')
api.add_resource(YesOrNo, "/yesorno/<string:name>")
  
if __name__ == "__main__":
  app.run(debug=True)